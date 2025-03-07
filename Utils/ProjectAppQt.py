
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from Utils.GlRenderer import GlRenderer
import sys

class ProjectAppQt(QApplication):
    def __init__(self, width, height, title):
        super().__init__(sys.argv)
        self.window = MainWindow(width, height, title)
    
    def run(self):
        self.window.show()
        super().exec()

class MainWindow(QMainWindow):
    def __init__(self, width, height, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)

        self.setMinimumSize(400, 300)

        container = QWidget()
        layout = QHBoxLayout()
        renderer =  GlRenderer(width, height, parent = container)
        menubar = OptionWidget(renderer, parent = container)
        layout.addWidget(renderer)
        layout.addWidget(menubar)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def showEvent(self, event):
        super().showEvent(event)
        self.centralWidget().resize(self.width(), self.height())

class OptionWidget(QWidget):
    def __init__(self, glRenderer : GlRenderer, parent = None):
        super().__init__(parent)
        self.glRenderer = glRenderer

        self.setMinimumWidth(200)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.zoomSlider = QSlider(Qt.Orientation.Horizontal)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(100)
        self.zoomSlider.setValue(10)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.valueChanged.connect(self.updateZoom)

        self.zoomLabel = QLabel("Zoom")
        layout.addWidget(self.zoomLabel)
        layout.addWidget(self.zoomSlider)

        self.setLayout(layout)
        

    def updateZoom(self, value):
        self.glRenderer.updateZoom(value/10.0)
        