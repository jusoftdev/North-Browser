from PyQt5.QtCore import QObject, QThread, pyqtSignal
import keyboard

class Worker(QObject):
    finished = pyqtSignal()
    pressed = pyqtSignal()

    def run(self):
        while True:
            if keyboard.read_key() == "esc":
                self.pressed.emit()
        self.finished.emit()
        return(0)