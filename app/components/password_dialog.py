# coding:utf-8

from cgitb import text
import os

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

from qfluentwidgets import MessageBoxBase, TitleLabel, PasswordLineEdit

from ..common.setting import ADMIN_PASSWORD


class PassWordDialog(MessageBoxBase):
    """Custom message box"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleLabel = TitleLabel(f"ADMIN验证", self)
        self.viewLayout.addWidget(
            self.titleLabel,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        self.passWordLineEdit = PasswordLineEdit(self)
        self.passWordLineEdit.setPlaceholderText("请输入ADMIN验证码")
        self.passWordLineEdit.setMinimumWidth(250)
        self.viewLayout.addWidget(self.passWordLineEdit)

        self.yesButton.setText("验证")
        self.cancelButton.hide()

    def verifyPassword(self):
        passWord = self.passWordLineEdit.text()
        if passWord == ADMIN_PASSWORD:
            return True
        else:
            return False
    
