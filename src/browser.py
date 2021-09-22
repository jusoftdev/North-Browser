from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class Browser(QWebEngineView):
    backpressed = pyqtSignal()
    forwardpressed = pyqtSignal()
    reloadpressed = pyqtSignal()
    viewpressed = pyqtSignal()
    inspectpressed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setContextMenuPolicy(Qt.NoContextMenu)

        self.settings().setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, True
        )
        self.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True
        )
        self.settings().setAttribute(
            QWebEngineSettings.AutoLoadImages, True)

        self.settings().setAttribute(
            QWebEngineSettings.PluginsEnabled, True)

        self.settings().setAttribute(
            QWebEngineSettings.LocalStorageEnabled, True)


    def contextMenuEvent(self, event):
        menu = QMenu()

        backAction = menu.addAction(QIcon("..\\ressources\\icons\\backward.png"), "Back")
        forwardAction = menu.addAction(QIcon("..\\ressources\\icons\\forward.png"), "Forward")
        relaodAction = menu.addAction(QIcon("..\\ressources\\icons\\reload.png"), "Reload")
        viewAction = menu.addAction("View Page Source")
        inspectAction = menu.addAction("Inspect Element")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == backAction:
            self.backpressed.emit()

        elif action == forwardAction:
            self.forwardpressed.emit()

        elif action == relaodAction:
            self.reloadpressed.emit()

        elif action == viewAction:
            self.viewpressed.emit()

        elif action == inspectAction:
            self.inspectpressed.emit()

