# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ..components.password_dialog import PassWordDialog
from ..components.control_table import ControlTable


class ControlInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.controlTable = ControlTable(self)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName("controlInterface")

        self.__initLayout()

    def __initLayout(self):
        self.layouts = QVBoxLayout(self)
        
        self.layouts.addWidget(self.controlTable)

    def verify(self):
        self.verifyDialog = PassWordDialog(self)
        if self.verifyDialog.exec():
            if not self.verifyDialog.verifyPassword():
                self.verify()

