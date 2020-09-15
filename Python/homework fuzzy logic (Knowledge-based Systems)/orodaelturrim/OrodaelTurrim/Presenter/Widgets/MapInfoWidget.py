import typing
from typing import Optional

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton

from OrodaelTurrim import UI_ROOT, ICONS_ROOT
from OrodaelTurrim.Business.Factory import BorderFactory
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import AttributeType, GameRole
from OrodaelTurrim.Structure.Position import Position


class MapInfoWidget(QWidget):
    """Widget for display information about selected tile"""

    position_axial_icon: QLabel
    position_cubic_icon: QLabel
    position_offset_icon: QLabel

    position_axial_label: QLabel
    position_cubic_label: QLabel
    position_offset_label: QLabel

    position_label: QLabel
    tile_label: QLabel
    character_widget: QWidget

    visibility_button: QPushButton
    attack_range_button: QPushButton
    move_button: QPushButton


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__selected_tile = None  # type: Optional[Position]

        Connector().subscribe('map_position_change', self.map_tile_select_slot)
        Connector().subscribe('redraw_ui', self.redraw_ui_slot)
        Connector().subscribe('game_thread_finished', self.redraw_ui_slot)
        Connector().subscribe('map_position_clear', self.map_tile_unselected_slot)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'mapInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        self.position_offset_icon = typing.cast(QLabel, self.findChild(QLabel, 'offsetIconLabel'))
        self.position_cubic_icon = typing.cast(QLabel, self.findChild(QLabel, 'cubicIconLabel'))
        self.position_axial_icon = typing.cast(QLabel, self.findChild(QLabel, 'axialIconLabel'))

        self.position_offset_label = typing.cast(QLabel, self.findChild(QLabel, 'offsetPositionLabel'))
        self.position_cubic_label = typing.cast(QLabel, self.findChild(QLabel, 'cubicPositionLabel'))
        self.position_axial_label = typing.cast(QLabel, self.findChild(QLabel, 'axialPositionLabel'))

        self.character_widget = typing.cast(QWidget, self.findChild(QWidget, 'characterWidget'))
        self.position_label = typing.cast(QLabel, self.findChild(QLabel, 'positionLabel'))
        self.tile_label = typing.cast(QLabel, self.findChild(QLabel, 'tileLabel'))

        self.visibility_button = typing.cast(QPushButton, self.findChild(QPushButton, 'visibilityButton'))
        self.attack_range_button = typing.cast(QPushButton, self.findChild(QPushButton, 'attackButton'))
        self.move_button = typing.cast(QPushButton, self.findChild(QPushButton, 'moveButton'))

        self.position_label.setContentsMargins(0, 0, 0, 60)

        self.visibility_button.setIcon(QIcon(str(ICONS_ROOT / 'eye.png')))
        self.visibility_button.clicked.connect(self.show_visibility_slot)

        self.attack_range_button.setIcon(QIcon(str(ICONS_ROOT / 'sword.png')))
        self.attack_range_button.clicked.connect(self.show_attack_range_slot)

        self.move_button.setIcon(QIcon(str(ICONS_ROOT / 'foot.png')))
        self.move_button.clicked.connect(self.show_accessible_tiles_slot)

        self.position_offset_icon.setScaledContents(True)
        self.position_offset_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'offset.png')))

        self.position_cubic_icon.setScaledContents(True)
        self.position_cubic_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'cube.png')))

        self.position_axial_icon.setScaledContents(True)
        self.position_axial_icon.setPixmap(QPixmap(str(ICONS_ROOT / 'axis.png')))


    def draw_position_info(self) -> None:
        """ Draw info about position (Offset, Cubic  and Axial Positions) """
        if self.__selected_tile:
            self.position_label.setVisible(True)

            self.position_offset_icon.setVisible(True)
            self.position_cubic_icon.setVisible(True)
            self.position_axial_icon.setVisible(True)

            self.position_offset_label.setText(self.__selected_tile.offset.string)
            self.position_cubic_label.setText(self.__selected_tile.cubic.string)
            self.position_axial_label.setText(self.__selected_tile.axial.string)

        else:
            self.position_label.setVisible(False)

            self.position_offset_icon.setVisible(False)
            self.position_cubic_icon.setVisible(False)
            self.position_axial_icon.setVisible(False)

            self.position_offset_label.setText('')
            self.position_cubic_label.setText('')
            self.position_axial_label.setText('')


    def draw_tile_info(self) -> None:
        """ Draw info about map tile """

        tile_image = typing.cast(QLabel, self.findChild(QLabel, 'tileImageLabel'))
        tile_label = typing.cast(QLabel, self.findChild(QLabel, 'tileLabel'))
        tile_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'tileInfoText'))

        if self.__selected_tile:
            tile = self.__game_engine.get_game_map()[self.__selected_tile]
            tile_type = tile.terrain_type

            img = AssetsEncoder[tile_type]

            tile_image.setVisible(True)
            tile_image.setScaledContents(True)
            tile_image.setMargin(20)
            tile_image.setPixmap(QPixmap(str(img)).scaled(150, 150, Qt.KeepAspectRatio))

            tile_text.setHtml(tile.info_text())

            tile_label.setVisible(True)
            tile_label.setText('Map tile: {}'.format(tile.__class__.__name__))
        else:
            tile_image.setVisible(False)
            tile_text.setText('')
            tile_label.setVisible(False)


    def draw_character_info(self) -> None:
        """ Draw info about character on the selected position """

        character_label = typing.cast(QLabel, self.findChild(QLabel, 'characterLabel'))
        character_image = typing.cast(QLabel, self.findChild(QLabel, 'characterImageLabel'))

        attribute_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'objectAttributesText'))
        attribute_label = typing.cast(QLabel, self.findChild(QLabel, 'objectAttributesLabel'))

        filter_label = typing.cast(QLabel, self.findChild(QLabel, 'objectFiltersLabel'))
        filter_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'objectFiltersText'))

        effect_label = typing.cast(QLabel, self.findChild(QLabel, 'objectEffectsLabel'))
        effect_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'objectEffectsText'))

        visibility_button = typing.cast(QPushButton, self.findChild(QPushButton, 'visibilityButton'))
        attack_button = typing.cast(QPushButton, self.findChild(QPushButton, 'attackButton'))
        move_button = typing.cast(QPushButton, self.findChild(QPushButton, 'moveButton'))

        display = bool(self.__selected_tile)  # Tile is selected
        display &= bool(self.__game_engine.is_position_occupied(self.__selected_tile))  # Position is occupied by object

        # Active player see that position
        visible_tiles = self.__game_engine.get_player_visible_tiles(self.__game_engine.get_game_history().active_player)
        display &= self.__selected_tile in visible_tiles

        if display:
            # Display name of the game object
            character_label.setVisible(True)
            character_label.setContentsMargins(0, 0, 0, 20)
            character_label.setText(
                'Character: {}'.format(self.__game_engine.get_object_type(self.__selected_tile).name.capitalize()))

            # Display game object image
            character_image.setVisible(True)
            img = self.__game_engine.get_object_type(self.__selected_tile)
            character_image.setPixmap(
                QPixmap(str(AssetsEncoder[img])).scaled(226, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Unit attributes
            attribute_text.setText(self.__game_engine.get_game_object(self.__selected_tile).description)
            attribute_label.setVisible(True)

            # Control buttons
            visibility_button.setVisible(True)
            attack_button.setVisible(True)
            move_button.setVisible(True)

            self.draw_characters_filters()
            self.draw_character_effects()

        else:
            character_label.setVisible(False)
            character_image.setVisible(False)

            attribute_text.setText('')
            attribute_label.setVisible(False)

            effect_label.setVisible(False)
            effect_text.setText('')

            filter_label.setVisible(False)
            filter_text.setText('')

            visibility_button.setVisible(False)
            attack_button.setVisible(False)
            move_button.setVisible(False)


    def draw_characters_filters(self) -> None:
        """ Draw info about character filters on the selected tile """

        filter_label = typing.cast(QLabel, self.findChild(QLabel, 'objectFiltersLabel'))
        filter_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'objectFiltersText'))

        if self.__game_engine.get_game_object(self.__selected_tile).role == GameRole.DEFENDER:
            attack_filters = self.__game_engine.get_game_object(self.__selected_tile).attack_filters
            text = ''
            for attack_filter in attack_filters:
                text += '{} <br>'.format(attack_filter.__class__.__name__)
            text += 'Random'
            filter_label.setVisible(True)
            filter_text.setText(text)
        else:
            filter_text.setText('')
            filter_label.setVisible(False)


    def draw_character_effects(self) -> None:
        """ Draw info about character effects on the selected tile """

        effect_text = typing.cast(QTextEdit, self.findChild(QTextEdit, 'objectEffectsText'))
        effect_label = typing.cast(QLabel, self.findChild(QLabel, 'objectEffectsLabel'))

        text = ''
        if self.__selected_tile and self.__game_engine.is_position_occupied(self.__selected_tile):
            effects = self.__game_engine.get_game_object(self.__selected_tile).active_effects
            for effect in effects:
                text += '{} ({})<br>'.format(effect.effect_type.name.capitalize(), effect.remaining_duration)

        effect_text.setText(text)
        effect_label.setVisible(True)


    @pyqtSlot()
    def redraw_ui_slot(self) -> None:
        """ Redraw whole UI of widget """
        self.draw_tile_info()
        self.draw_character_info()
        self.draw_position_info()


    @pyqtSlot(Position)
    def map_tile_select_slot(self, position: Position) -> None:
        """ Selected position change"""
        self.__selected_tile = position
        self.redraw_ui_slot()


    @pyqtSlot()
    def map_tile_unselected_slot(self) -> None:
        """ Clear selected position """
        self.__selected_tile = None
        self.redraw_ui_slot()


    @pyqtSlot()
    def show_visibility_slot(self) -> None:
        """ Display vision of the unit on the selected position """
        tiles = self.__game_engine.get_game_object(self.__selected_tile).visible_tiles

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])


    @pyqtSlot()
    def show_attack_range_slot(self) -> None:
        """ Display attack range of the unit on the selected position """
        attack_range = self.__game_engine.get_game_object(self.__selected_tile).get_attribute(
            AttributeType.ATTACK_RANGE)

        tiles = self.__game_engine.get_game_map().get_visible_tiles(self.__selected_tile, attack_range)

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])


    @pyqtSlot()
    def show_accessible_tiles_slot(self) -> None:
        """ Display accessible tiles of the unit on the selected position"""
        tiles = self.__game_engine.get_game_object(self.__selected_tile).accessible_tiles

        border_dict = BorderFactory.create(3, QColor(0, 0, 255), tiles)

        Connector().emit('display_border', border_dict, [QColor(0, 0, 255)])
