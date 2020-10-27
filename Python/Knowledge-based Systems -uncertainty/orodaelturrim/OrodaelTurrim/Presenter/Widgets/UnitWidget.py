import typing
from typing import List, Optional

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit

from OrodaelTurrim import UI_ROOT, ICONS_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.FilterDialog import FilterDialog
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.Filter.FilterPattern import FilterReference
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool
from OrodaelTurrim.Structure.Position import Position


class UnitWidget(QWidget):
    """ Widget for manual spawn of the unit"""


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None, object_type: GameObjectType = None):
        super().__init__(parent)

        self.__game_engine = game_engine
        self.__object_type = object_type
        self.__selected_position = None  # type: Optional[Position]
        self.__filters = []  # type: List[FilterReference]

        Connector().subscribe('map_position_change', self.map_tile_select_slot)
        Connector().subscribe('map_position_clear', self.map_tile_unselect_slot)
        Connector().subscribe('redraw_ui', self.redraw_ui)
        Connector().subscribe('game_thread_finished', self.redraw_ui)
        Connector().subscribe('game_over', self.game_over_slot)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'unitFrameWidget.ui')) as f:
            uic.loadUi(f, self)

        # Display unit image
        img_label = typing.cast(QLabel, self.findChild(QLabel, 'imageLabel'))
        img_label.setScaledContents(True)
        img = AssetsEncoder[self.__object_type]
        img_label.setPixmap(QPixmap(str(img)))

        # Display unit attributes
        name_label = typing.cast(QLabel, self.findChild(QLabel, 'nameLabel'))
        name_label.setText(self.__object_type.name.capitalize())

        price_label = typing.cast(QLabel, self.findChild(QLabel, 'priceLabel'))
        price_label.setText(str(GameObjectPrototypePool[self.__object_type].cost))

        img_label = typing.cast(QLabel, self.findChild(QLabel, 'priceImage'))
        img_label.setScaledContents(True)
        img_label.setPixmap(QPixmap(str(ICONS_ROOT / 'gold.png')))


        # Place unit button - default False because position is not selected
        button = typing.cast(QPushButton, self.findChild(QPushButton, 'placeButton'))
        button.setDisabled(True)

        self.findChild(QPushButton, 'placeButton').clicked.connect(self.place_unit_slot)
        self.findChild(QPushButton, 'filtersButton').clicked.connect(self.edit_filters_slot)
        self.findChild(QTextEdit, 'infoText').setText(GameObjectPrototypePool[self.__object_type].description_static)


    @pyqtSlot(Position)
    def map_tile_select_slot(self, position: Position) -> None:
        """ Save info about selected tile on map"""

        self.__selected_position = position
        self.redraw_ui()


    @pyqtSlot()
    def map_tile_unselect_slot(self):
        """ Set selected position to None """
        self.__selected_position = None
        self.redraw_ui()


    @pyqtSlot()
    def redraw_ui(self) -> None:
        """ Redraw UI of the card (disable or enable spawn button and display info why) """

        place_button = typing.cast(QPushButton, self.findChild(QPushButton, 'placeButton'))
        active_player = self.__game_engine.get_game_history().active_player

        # No position on map selected
        if self.__selected_position is None:
            place_button.setDisabled(True)
            place_button.setToolTip('No position on map selected')
            return

        # Game is in browsing mode
        if not self.__game_engine.get_game_history().in_preset:
            place_button.setDisabled(True)
            place_button.setToolTip('Cannot spawn units in browsing history mode')
            return

        # Not enough money for the unit
        player_resources = self.__game_engine.get_resources(active_player)
        if GameObjectPrototypePool[self.__object_type].cost > player_resources:
            place_button.setDisabled(True)
            place_button.setToolTip('Not enough money for this unit')
            return

        # Not have a base yet
        base_condition = self.__object_type == GameObjectType.BASE and self.__game_engine.player_have_base(
            self.__game_engine.get_game_history().active_player)
        if base_condition:
            place_button.setDisabled(True)
            place_button.setToolTip('You can have only 1 base')
            return

        # Place only on visible tiles
        if self.__selected_position not in self.__game_engine.get_player_visible_tiles(
                active_player) and self.__object_type != GameObjectType.BASE:
            place_button.setDisabled(True)
            place_button.setToolTip('You can spawn unit only on visible tiles!')
            return

        if self.__game_engine.get_game_map().position_on_edge(self.__selected_position):
            place_button.setDisabled(True)
            place_button.setToolTip('Cannot spawn units on the map edge!')
            return

        # Position is already occupied
        if self.__game_engine.is_position_occupied(self.__selected_position):
            place_button.setDisabled(True)
            place_button.setToolTip('Selected position already occupied')
            return

        # Game is over
        if Connector().get_variable('game_over'):
            place_button.setDisabled(True)
            place_button.setToolTip('Game is over')
            return

        place_button.setDisabled(False)
        place_button.setToolTip('Place this unit to selected tile')


    @pyqtSlot()
    def place_unit_slot(self) -> None:
        """ Spawn unit on the map """

        # Prepare move filters
        filter_instances = []
        for _filter in self.__filters:
            instance = FilterFactory().attack_filter(_filter.name, **_filter.arguments)
            filter_instances.append(instance)

        # Spawn unit
        player = self.__game_engine.get_game_history().active_player
        unit_info = SpawnInformation(player, self.__object_type, self.__selected_position, filter_instances, [])
        self.__game_engine.spawn_unit(unit_info)

        Connector().emit('redraw_map')
        Connector().emit('redraw_ui')


    @pyqtSlot()
    def game_over_slot(self) -> None:
        """ Disable all spawn buttons """
        self.redraw_ui()


    @pyqtSlot()
    def edit_filters_slot(self) -> None:
        """ Open dialog for edit filters of unit"""
        result, data = FilterDialog.execute_(self.__object_type, self.__filters)
        if result:
            self.__filters = data
