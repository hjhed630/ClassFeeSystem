# coding: utf-8

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from qfluentwidgets import BodyLabel

from ..common.setFont import setFont, FontWeight

from ..components.publicity_table import PublicityTable
from ..components.receipt_dialog import ReceiptDialog
from app.components import receipt_dialog


class PublicityInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.titleLabel = BodyLabel(self)
        self.balanceLabel = BodyLabel(self)
        self.publicityTable = PublicityTable(self)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName("publicityInterface")

        self.titleLabel.setText("班费公示表")
        setFont(self.titleLabel, 25, FontWeight.Bold)

        self.balanceLabel.setText(
            f"班费剩余 {self.publicityTable.returnBalance():.2f} 元"
        )
        setFont(self.balanceLabel, 15, FontWeight.DemiBold)

        self.publicityTable.showReceiptSignal.connect(self.showReceipt)

        self.__initLayout()

    def __initLayout(self):
        self.layouts = QVBoxLayout(self)
        self.layouts.setContentsMargins(10, 5, 10, 5)
        self.setLayout(self.layouts)

        self.layouts.addWidget(
            self.titleLabel,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )
        self.layouts.addWidget(
            self.balanceLabel,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight,
        )
        self.layouts.addWidget(self.publicityTable)

    def reloadData(self):
        self.publicityTable.initData()
        self.balanceLabel.setText(f"班费剩余 {self.publicityTable.returnBalance():.2f} 元")

    def showReceipt(self, name):
        w = ReceiptDialog(self,name)
        if w.exec():
            print("结束查看")
        