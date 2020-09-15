import typing
from pathlib import Path
from typing import List, Tuple, Dict, Union

import math
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRectF, pyqtSlot
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsScene, QGraphicsView, QScrollArea, QHBoxLayout, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QPushButton
from math import sqrt

from OrodaelTurrim import UI_ROOT, DEBUG, ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType
from OrodaelTurrim.Structure.Map import Border
from OrodaelTurrim.Structure.Position import Position, Point

HEXAGON_SIZE = Point(296, 148)
BORDER_OPACITY = 0.65
FOG_OF_WAR_OPACITY = 0.50


class GraphicItem(QGraphicsItem):
    """
    General graphic item for each item on map.
    Generalize position computation and overload PyQt functions
    """
    image_size = Point(296, 200)  # Size if tile image in pixels
    hexagon_size = HEXAGON_SIZE  # Size of only hexagon (without top overlay) in pixels
    hexagon_offset = Point(149, 127)

    _image_size: Point  # Real size of image based on transformation
    _size: float  # Length from hexagon center to hexagon corner
    _size_w: float  # Width of the hexagon with transformation
    _size_h: float  # Height of the hexagon with transformation


    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        super().__init__()

        self.parent = parent
        self._position = position
        self._game_engine = game_engine
        self._map_object = game_engine.get_game_map()
        self._transformation = transformation

        self.calculate_sizes()


    def calculate_sizes(self) -> None:
        """ Calculate sizes based on image size and transformation"""

        self._image_size = Point(self.image_size.x * self._transformation, self.image_size.y * self._transformation)
        self._size = self.hexagon_size.x * self._transformation / 2

        self._size_w = self.hexagon_size.x * self._transformation / 2
        self._size_h = self.hexagon_size.y * self._transformation / math.sqrt(3)


    def get_center(self) -> Point:
        """
        Get center of the tile in pixels
        :return: center point
        """
        p = self._position.axial
        x = self._size_w * (3. / 2 * p.q)
        y = self._size_h * ((sqrt(3) / 2 * p.q) + (sqrt(3) * p.r))
        return Point(x, y)


    def hex_corner_offset(self, corner: int) -> Tuple[float, float]:
        """
        Compute offset to the corner based on corner number
        |   4 - 5
        |  /     \
        | 3       0
        |  |     /
        |   2 - 1

        :param corner: number of corner, start from right corner
        :return: tuple of x and y offset to corner
        """
        angle = math.pi / 180 * (corner * 60)
        return self._size_w * math.cos(angle), self._size_h * math.sin(angle)


    def get_corners(self) -> List[Point]:
        """
        Get list of Points of corners of hexagon
        :return: list of corners points
        """
        center = self.get_center()
        corners = []
        for i in range(6):
            offset = self.hex_corner_offset(i)
            corners.append(Point(center.x + offset[0], (center.y + offset[1])))
        return corners


    def boundingRect(self) -> QRectF:
        """
        Override bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.get_center()

        image_hexagon_diff = (self.image_size.y - self.hexagon_size.y) * self._transformation
        hexagon_width = self.hexagon_size.y * self._transformation

        left_top = Point(center.x - self._size, center.y - hexagon_width / 2 - image_hexagon_diff)
        return QRectF(left_top.x,
                      left_top.y,
                      (self.image_size.x * self._transformation),
                      (self.image_size.y * self._transformation))


class MapTileGraphicsItem(GraphicItem):
    """
    Graphic item for render one map tile
    """


    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        super().__init__(parent, game_engine, position, transformation)


    def transformation_change_slot(self, transformation: float) -> None:
        """ Change transformation and recalculate sizes"""
        self._transformation = transformation
        self.calculate_sizes()
        self.update()
        self.parent.scene.update()


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """
        Override paint function. Call every time when need to be render
        :param painter: painter object
        :param option: style options of item
        :param widget: parent widget
        """

        # Get image
        image_path = self.get_tile_image(self._map_object[self._position].terrain_type)
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)

        if DEBUG:
            # Draw position numbers on tiles
            self.draw_position(painter)
            # Draw bounding rectangle
            painter.drawRect(self.boundingRect())


    def draw_position(self, painter: QPainter) -> None:
        """
        Draw offset position to each tile
        """
        font = painter.font()
        font.setPointSize(15)
        painter.setFont(font)
        painter.setPen(QColor(230, 0, 0))

        painter.drawText(self.boundingRect(),
                         Qt.AlignVCenter | Qt.AlignHCenter,
                         '{},{}'.format(self._position.offset.q, self._position.offset.r))


    def get_tile_image(self, tile_type: TerrainType) -> Path:
        """
        Get path to image based on terrain type

        :param tile_type: enum of terrain type
        :return: Path to png image
        """
        # For river determinate rotation correct rotation
        if tile_type == TerrainType.RIVER:
            river_direction = []
            out_of_map_direction = []

            for i, position in enumerate(self._position.get_all_neighbours()):
                # Select out of the map direction (River always end on the map edge
                if not self._map_object.position_on_map(position):
                    out_of_map_direction.append(i)

                # Select river neighbour
                elif self._map_object[position].terrain_type == TerrainType.RIVER:
                    river_direction.append(int(i))

            # If more than out of map position, selected position with maximum different way from on map river
            if out_of_map_direction:
                river_direction.append(
                    sorted(out_of_map_direction, key=lambda x: abs(river_direction[0] - x), reverse=True)[0])

            river_direction.sort()
            return AssetsEncoder['river_{}'.format('-'.join(map(str, river_direction)))]
        else:
            return AssetsEncoder[tile_type]


class ObjectGraphicsItem(GraphicItem):
    """ Graphic item for display units on map """


    def __init__(self, parent: "MapWidget", game_engine: GameEngine, position: Position, transformation: float = 0.3):
        super().__init__(parent, game_engine, position, transformation)


    def transformation_change_slot(self, transformation: float) -> None:
        """ Change transformation and recalculate sizes"""
        self._transformation = transformation
        self.calculate_sizes()
        self.update()
        self.parent.scene.update()


    def boundingRect(self) -> QRectF:
        """
        Over rider bounding rectangle for determinate paint event
        :return: rectangle of png image
        """
        center = self.get_center()

        rect_size = min(self._size_h, self._size_w) * 1.6

        return QRectF(center.x - rect_size / 2,
                      center.y - rect_size / 2,
                      rect_size,
                      rect_size)


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        """ Override paint function. Call every time when need to be render """

        # Check if there is object
        if self._game_engine.get_object_type(self._position) == GameObjectType.NONE:
            return

        # Check if object is visible
        if self._position not in self._game_engine.get_player_visible_tiles(
                self._game_engine.get_game_history().active_player):
            return

        image_path = AssetsEncoder[self._game_engine.get_object_type(self._position)]
        pixmap = QPixmap(str(image_path))

        painter.drawPixmap(self.boundingRect().toRect(), pixmap)


class TileBorderGraphicsItem(GraphicItem):
    """ Graphic item for draw borders of the tiles """


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        border = self.parent.borders.get(self._position, None)

        if not border:
            return

        painter.setOpacity(BORDER_OPACITY)

        colors = border.color
        borders = border.order
        corners = self.get_corners()
        for i in range(len(corners) - 1, -1, -1):
            if borders[i] != 0:
                painter.setPen(QPen(colors[i], borders[i], Qt.SolidLine))
                painter.drawLine(corners[i], corners[i - 1])


class TileVisibilityGraphicsItem(GraphicItem):
    """ Graphic item for draw fog of war"""


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
        visible = self._position in self._game_engine.get_player_visible_tiles(
            self._game_engine.get_game_history().active_player)

        if not visible:
            painter.setOpacity(FOG_OF_WAR_OPACITY)
            painter.setPen(QPen(Qt.white, 0, Qt.SolidLine))

            painter.setBrush(QBrush(QColor(70, 70, 70), Qt.SolidPattern))
            corners = self.get_corners()
            painter.drawConvexPolygon(*corners)


class MapWidget(QWidget):
    """ Widget with map canvas and control buttons"""

    scroll_area: QScrollArea  # Scroll area for map
    scene: QGraphicsScene
    view: QGraphicsView


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)
        self.__game_engine = game_engine

        self.borders = {}  # type: Dict[Position, Border]
        self.transformation = 0.4

        Connector().subscribe('redraw_map', self.redraw_map)
        Connector().subscribe('display_border', self.display_borders)
        Connector().subscribe('game_thread_finished', self.redraw_map)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'mapWidget.ui')) as f:
            uic.loadUi(f, self)

        self.scroll_area = typing.cast(QScrollArea, self.findChild(QScrollArea, 'scrollArea'))
        scroll_layout = QHBoxLayout()

        self.scene = QGraphicsScene(self.scroll_area)

        game_map = self.__game_engine.get_game_map()

        # Create graphic item for each map objects. Z order of the items is based on insertion to scene
        # Insert Map tiles and Units
        for position in game_map.tiles:
            self.scene.addItem(MapTileGraphicsItem(self, self.__game_engine, position, self.transformation))
            self.scene.addItem(ObjectGraphicsItem(self, self.__game_engine, position, self.transformation))
        # Insert Fog of war items
        for position in game_map.tiles:
            self.scene.addItem(TileVisibilityGraphicsItem(self, self.__game_engine, position, self.transformation))
        # Insert Border items
        for position in game_map.tiles:
            self.scene.addItem(TileBorderGraphicsItem(self, self.__game_engine, position, self.transformation))

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.view.setContentsMargins(0, 0, 0, 0)
        self.view.setViewportMargins(0, 0, 0, 0)

        scroll_layout.addWidget(self.view)
        self.scroll_area.setLayout(scroll_layout)

        # Setup buttons under map
        zoom_in_button = typing.cast(QPushButton, self.findChild(QPushButton, 'zoomInButton'))
        zoom_out_button = typing.cast(QPushButton, self.findChild(QPushButton, 'zoomOutButton'))
        zoom_reset_button = typing.cast(QPushButton, self.findChild(QPushButton, 'zoomResetButton'))
        clear_view_button = typing.cast(QPushButton, self.findChild(QPushButton, 'clearViewButton'))

        zoom_in_button.clicked.connect(self.zoom_in_slot)
        zoom_out_button.clicked.connect(self.zoom_out_slot)
        zoom_reset_button.clicked.connect(self.zoom_reset_slot)
        clear_view_button.clicked.connect(self.clear_view_slot)

        zoom_out_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_out.png')))
        zoom_in_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_in.png')))
        zoom_reset_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'zoom_reset.png')))
        clear_view_button.setIcon(QtGui.QIcon(str(ICONS_ROOT / 'eye_cross.png')))

        # Send click on map with transformation for correct position computation
        self.scene.mousePressEvent = lambda x: self.click_on_map(x, self.transformation)

        self.view.show()


    def clear_border_color(self, color: Union[QColor, List[QColor]]) -> None:
        """ Clear borders of given colors"""
        for k in list(self.borders):
            if self.borders[k].color[0] == color:
                del self.borders[k]


    @pyqtSlot()
    def click_on_map(self, event: QGraphicsSceneMouseEvent, transformation: float) -> None:
        """ Handle click on map - try to compute position and inform about selected tile """

        position = Position.from_pixel(event.scenePos(), transformation).offset

        if self.__game_engine.get_game_map().position_on_map(position):
            self.borders.clear()

            self.borders[position] = Border.full(3, QColor(255, 0, 0))
            Connector().emit('map_position_change', position)

        self.scene.update()


    @pyqtSlot()
    def redraw_map(self) -> None:
        """ Update scene based on redraw signal """
        if not Connector().get_variable('redraw_disable'):
            self.scene.update()


    @pyqtSlot()
    def zoom_in_slot(self):
        """ Zoom in map by 25% """
        self.view.scale(1.25, 1.25)


    @pyqtSlot()
    def zoom_out_slot(self):
        """ Zoom out map by 25% """
        self.view.scale(0.80, 0.80)


    @pyqtSlot()
    def zoom_reset_slot(self):
        """ Reset zoom to state, that whole map is visible """
        rect = QtCore.QRectF(self.scene.sceneRect())
        if not rect.isNull():
            self.view.setSceneRect(rect)

            unity = self.view.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.view.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.view.viewport().rect()
            scene_rect = self.view.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.view.scale(factor, factor)


    @pyqtSlot(dict, list)
    def display_borders(self, border_info: Dict[Position, Border], clear_colors: List[QColor] = None):
        """ Display borders on the map"""
        if clear_colors:
            if type(clear_colors) is not list:
                clear_colors = [clear_colors]

            for color in clear_colors:
                self.clear_border_color(color)

        self.borders.update(border_info)
        self.redraw_map()


    @pyqtSlot()
    def clear_view_slot(self):
        """ Clear all borders on map and clear selected position"""
        Connector().emit('map_position_clear')
        self.borders.clear()
        self.redraw_map()
