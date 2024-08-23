# coding: utf-8

from functools import partial
import json
from linecache import lazycache
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from qfluentwidgets import TableWidget, PrimaryPushButton

from ..common.setting import DATA_FILE
from ..common.json_load import jsonRewrite


class ControlTable(TableWidget):

    showReceiptSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setBorderVisible(True)
        self.setBorderRadius(5)
        self.setWordWrap(True)

        self.setColumnCount(6)
        self.verticalHeader().hide()
        self.setHorizontalHeaderLabels(
            ["日期", "摘要", "收入/支出", "签名", "收据", "操作"]
        )

        self.horizontalHeader().setSectionsMovable(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.column_ratios = [15, 15, 15, 15, 15, 25]
        self.total_ratio = sum(self.column_ratios)

        self.initData()

    def resizeEvent(self, event) -> None:
        super(ControlTable, self).resizeEvent(event)
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
            self.setRowHeight(i, 50)
            for j in range(6):
                if j != 4 and j != 5:
                    item = QTableWidgetItem(data[j])
                    self.setItem(i, j, item)
                elif j == 5:
                    deleteButton = PrimaryPushButton("删除", self)
                    deleteButton.clicked.connect(partial(self.deleteInfo, row=i))
                    deleteButton.setMinimumWidth(50)

                    self.setCellWidget(i, j, deleteButton)

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

    def deleteInfo(self, row):
        self.removeRow(row)

    def getInfo(self):
        data_list = []

        for row in range(self.rowCount()):
            row_data = []
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item is not None:
                    content = item.text()
                    row_data.append(content)

            # 将当前行的数据添加到列表中
            data_list.append(row_data)
        return data_list

    def saveInfo(self):
        datas = self.getInfo()
        jsonRewrite(datas)
