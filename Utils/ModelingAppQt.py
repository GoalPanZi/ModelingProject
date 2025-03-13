
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QSurfaceFormat
from Utils.MainWindowQt import MainWindow
import sys

class ModelingAppQt(QApplication):
    def __init__(self, width, height, title):
        format = QSurfaceFormat()
        format.setSamples(4)
        QSurfaceFormat.setDefaultFormat(format)
        super().__init__(sys.argv)
        self.window = MainWindow(width, height, title)
    
    def run(self):
        self.window.show()
        super().exec()

       