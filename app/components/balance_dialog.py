# coding:utf-8

import os

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QFileDialog

from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    LineEdit,
    PushButton,
    CalendarPicker,
    DoubleSpinBox,
    TitleLabel,
)

from ..common.setFont import setFont, FontWeight


class BalanceDialog(MessageBoxBase):
    """Custom message box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = TitleLabel(self)

        self.dateLabel = SubtitleLabel(self)
        self.datePicker = CalendarPicker(self)

        self.descriptionLabel = SubtitleLabel(self)
        self.descriptionLineEdit = LineEdit(self)

        self.balanceLabel = SubtitleLabel(self)
        self.balanceLineEdit = DoubleSpinBox(self)

        self.nameLabel = SubtitleLabel(self)
        self.nameLineEdit = LineEdit(self)

        self.receiptLabel = SubtitleLabel(self)
        self.receiptButton = PushButton(self)
        self.receipt = "无"

        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")

        self._initWidget()

    def _initWidget(self):

        self.titleLabel.setText("添加项")
        setFont(self.titleLabel, 15, FontWeight.DemiBold)

        self.dateLabel.setText("选择时间: ")
        self.datePicker.setDate(QDate().currentDate())
        self.datePicker.setMinimumWidth(500)

        self.descriptionLabel.setText("输入摘要")
        self.descriptionLineEdit.setPlaceholderText("简短的摘要")

        self.balanceLabel.setText("金额")
        self.balanceLineEdit.setMaximum(9999999)
        self.balanceLineEdit.setMinimum(-9999999)

        self.nameLabel.setText("操作人")
        self.nameLineEdit.setPlaceholderText("姓名")

        self.receiptLabel.setText("添加收据")
        self.receiptButton.setText("选择文件")
        self.receiptButton.clicked.connect(self.selectFile)

        self._initLayout()

    def _initLayout(self):

        self.viewLayout.setContentsMargins(10, 5, 10, 5)
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.dateLabel)
        self.viewLayout.addWidget(self.datePicker)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.viewLayout.addWidget(self.descriptionLineEdit)
        self.viewLayout.addWidget(self.balanceLabel)
        self.viewLayout.addWidget(self.balanceLineEdit)
        self.viewLayout.addWidget(self.nameLabel)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.receiptLabel)
        self.viewLayout.addWidget(self.receiptButton)

    def selectFile(self):
        filters = "Image files (*.png *.jpeg *.jpg *.gif *.bmp)"
        fileName, fileType = QFileDialog.getOpenFileName(
            self, "选取文件", os.getcwd(), filters
        )
        print(fileName)
        self.receiptLabel.setText(f"已选择文件 - {fileName}")
        self.receipt = fileName

    def returnData(self):
        date = self.datePicker.text()
        description = self.descriptionLineEdit.text()
        balance = self.balanceLineEdit.value()
        name = self.nameLineEdit.text()
        receipt = self.receipt

        return [date, description, str(balance), name, receipt]
