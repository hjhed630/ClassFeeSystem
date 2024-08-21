# coding: utf-8

from functools import partial
import json
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal

from qfluentwidgets import TableWidget, PrimaryPushButton

from ..common.setting import DATA_FILE


class PublicityTable(TableWidget):

    showReceiptSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setBorderVisible(True)
        self.setBorderRadius(5)
        self.setWordWrap(True)

        self.setColumnCount(5)
        self.verticalHeader().hide()
        self.setHorizontalHeaderLabels(["日期", "摘要", "收入/支出", "签名", "收据"])

        self.horizontalHeader().setSectionsMovable(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.column_ratios = [15, 40, 15, 15, 15]
        self.total_ratio = sum(self.column_ratios)

        self.initData()

    def resizeEvent(self, event) -> None:
        super(PublicityTable, self).resizeEvent(event)
        width = self.contentsRect().width()

        for column, ratio in enumerate(self.column_ratios):
            column_width = int((width * ratio) / self.total_ratio)
            self.setColumnWidth(column, column_width)

    def initData(self):
        self.receiptButtonList = []
        buttonId = 0
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            datas = json.load(file)["data"]

        self.setRowCount(len(datas))

        for i, data in enumerate(datas):
            for j in range(5):
                if j != 4:
                    item = QTableWidgetItem(data[j])
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.setItem(i, j, item)
                else:

                    if data[j] != "无":
                        receiptButton = PrimaryPushButton("查看收据", self)
                        receiptButton.setFixedSize(
                            self.columnWidth(j) - 10, self.rowHeight(i) - 10
                        )
                        receiptButton.clicked.connect(
                            partial(self.showReceipt, id=buttonId)
                        )

                        self.receiptButtonList.append(
                            {
                                "id": buttonId,
                                "button": receiptButton,
                                "receipt": data[j],
                            }
                        )

                        self.setCellWidget(i, j, receiptButton)
                        buttonId += 1
                    else:
                        item = QTableWidgetItem("无")
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        self.setItem(i, j, item)

    def showReceipt(self, id):

        buttonInfo = self.receiptButtonList[id]
        if buttonInfo["id"] != id:
            return
        self.showReceiptSignal.emit(buttonInfo["receipt"])

    def returnBalance(self):
        balance = []
        for row in range(self.rowCount()):
            item = self.item(row, 2)
            if item is not None:

                balance.append(eval(item.text()))

        return sum(balance)
