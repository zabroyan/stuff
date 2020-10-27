import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QTreeView, QPushButton, QFileDialog, QMenu, QAction

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class LogWidget(QWidget):
    """ Widget for displaying log information"""

    log: QTreeView


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('redraw_ui', self.update_text)
        Connector().subscribe('game_thread_finished', self.update_text)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'logWidget.ui')) as f:
            uic.loadUi(f, self)

        self.log = typing.cast(QTreeView, self.findChild(QTreeView, 'treeView'))

        self.log.setContextMenuPolicy(Qt.CustomContextMenu)
        self.log.customContextMenuRequested.connect(self.open_context_menu)

        self.log.setModel(self.__game_engine.get_game_history().to_model())
        self.log.setHeaderHidden(True)

        expand_button = typing.cast(QPushButton, self.findChild(QPushButton, 'expandButton'))
        expand_button.clicked.connect(self.expand_all_slot)

        expand_button = typing.cast(QPushButton, self.findChild(QPushButton, 'collapseButton'))
        expand_button.clicked.connect(self.collapse_all_slot)

        export_html_button = typing.cast(QPushButton, self.findChild(QPushButton, 'exportHtmlButton'))
        export_html_button.clicked.connect(self.export_html_button)

        export_xml_button = typing.cast(QPushButton, self.findChild(QPushButton, 'exportXmlButton'))
        export_xml_button.clicked.connect(self.export_xml_button)


    def open_context_menu(self, position) -> None:
        """
        Open context menu after right click on item

        :param position: position of the click
        """
        menu = QMenu()

        try:
            index = self.log.selectedIndexes()[0]
        except IndexError:
            return

        item = index.model().itemData(index)

        history_action = QAction("Browse there", self)
        history_action.triggered.connect(lambda: self.history_point_slot(item))

        menu.addAction(history_action)

        menu.exec_(self.log.viewport().mapToGlobal(position))


    @pyqtSlot(object)
    def history_point_slot(self, item) -> None:
        """
        Move history to selected item

        :param item: selected item
        """
        self.__game_engine.get_game_history().to_history_point(*item[257])

        Connector().emit('redraw_map')
        Connector().emit('redraw_ui')


    @pyqtSlot()
    def update_text(self) -> None:
        """ Set text of the text edit to output from GameHistory"""
        self.log.setModel(self.__game_engine.get_game_history().to_model())


    @pyqtSlot()
    def expand_all_slot(self):
        self.log.expandAll()


    @pyqtSlot()
    def collapse_all_slot(self):
        self.log.collapseAll()


    @pyqtSlot()
    def export_xml_button(self):
        options = QFileDialog.Options()

        file_name, _ = QFileDialog.getSaveFileName(self, "Export game history to XML", "",
                                                   "XML Files (*.xml)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.__game_engine.get_game_history().to_xml())
            except IOError:
                self.error_message_slot('Export history', 'Problem with writing to target file {}'.format(file_name))


    @pyqtSlot()
    def export_html_button(self):
        options = QFileDialog.Options()

        file_name, _ = QFileDialog.getSaveFileName(self, "Export game history to HTML", "",
                                                   "HTML Files (*.html)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write(self.__game_engine.get_game_history().to_html())
            except IOError:
                self.error_message_slot('Export history', 'Problem with writing to target file {}'.format(file_name))
