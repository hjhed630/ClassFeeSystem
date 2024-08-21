# coding:utf-8

import os

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

from qfluentwidgets import (
    MessageBoxBase,
    TitleLabel,
)
from ..common.setting import IMG_FOLDER


class ReceiptDialog(MessageBoxBase):
    """Custom message box"""

    def __init__(self, parent=None, name=""):
        super().__init__(parent)
        self.titleLabel = TitleLabel(f"收据", self)

        self.imagePath = IMG_FOLDER / f"{name}"
        print(self.imagePath)
        self.pixmap = QPixmap(str(self.imagePath))

        self.receiptLabel = QLabel(self)
        self.receiptLabel.setMaximumSize(480, 270)
        self.receiptLabel.setFixedSize(480, 270)
        self.receiptLabel.setPixmap(
            self.pixmap.scaled(self.receiptLabel.width(), self.receiptLabel.height())
        )

        self.viewLayout.addWidget(
            self.titleLabel, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.viewLayout.addWidget(
            self.receiptLabel,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        self.yesButton.setText("完事")
        self.cancelButton.setText("退出")
