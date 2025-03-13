from PyQt6.QtWidgets import QMainWindow
from Utils.GlRendererQt import GlRenderer
from Utils.SideDockWidgetQt import SideDockWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, width, height, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)
        self.setMinimumSize(400, 300)
        self.setCentralWidget(GlRenderer(width, height))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                           SideDockWidget(self.centralWidget()))
