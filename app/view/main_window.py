# coding: utf-8
import os
import shutil

from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (
    NavigationItemPosition,
    MSFluentWindow,
    SplashScreen,
    InfoBar,
    InfoBarPosition,
)
from qfluentwidgets import FluentIcon as FIF

from .setting_interface import SettingInterface
from .publicity_interface import PublicityInterface
from .control_interface import ControlInterface
from ..common.config import cfg
from ..common.icon import Icon
from ..common.setting import CLASS_NAME, IMG_FOLDER
from ..common.signal_bus import signalBus
from ..common import resource
from ..common.json_load import jsonLoad

from ..components.balance_dialog import BalanceDialog


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.changedPage = [0]

        self.settingInterface = SettingInterface(self)
        self.publicityInterface = PublicityInterface(self)
        self.controlInterface = ControlInterface(self)

        self.connectSignalToSlot()

        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):

        # publicity page
        self.addSubInterface(
            self.publicityInterface,
            FIF.PEOPLE,
            "班费公示",
            FIF.PEOPLE,
            NavigationItemPosition.TOP,
        )
        self.navigationInterface.addItem(
            "addItem",
            FIF.ADD,
            "添加项目",
            self.showDialog,
            False,
            FIF.ADD,
            NavigationItemPosition.TOP,
        )

        self.addSubInterface(
            self.controlInterface,
            FIF.COMMAND_PROMPT,
            "管理",
            FIF.COMMAND_PROMPT,
            position=NavigationItemPosition.BOTTOM,
        )

        # add custom widget to bottom
        self.addSubInterface(
            self.settingInterface,
            Icon.SETTINGS,
            "设置",
            Icon.SETTINGS_FILLED,
            NavigationItemPosition.BOTTOM,
        )
        self.stackedWidget.currentChanged.connect(self.verifyAdmin)
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(":/app/images/logo.png"))
        self.setWindowTitle(f"班费管理系统 -- {CLASS_NAME}")

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "splashScreen"):
            self.splashScreen.resize(self.size())

    def showDialog(self):
        w = BalanceDialog(self)
        if w.exec():
            data = w.returnData()
            if data[-1] != "无":
                os.path.basename(data[-1])
                shutil.copy(data[-1], IMG_FOLDER / f"{os.path.basename(data[-1])}")
                data[-1] = os.path.basename(data[-1])
            jsonLoad({"data": data})
            self.publicityInterface.reloadData()
            InfoBar.success(
                title="成功",
                content=f"班费项添加成功~\n当前剩余: {self.publicityInterface.publicityTable.returnBalance():.2f}",
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=4000,
                parent=self,
            )

    def verifyAdmin(self, pageNum):

        print(self.changedPage)
        if self.changedPage[-1] == 1:
            self.controlInterface.controlTable.saveInfo()
            self.publicityInterface.reloadData()
        if pageNum == 1:
            self.controlInterface.verify()
        self.changedPage.append(pageNum)
