from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QSlider, QLabel, QWidget, QFormLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Utils.GlRendererQt import GlRenderer

class SideDockWidget(QDockWidget):
    def __init__(self, glRenderer : GlRenderer):
        super().__init__()
        self.glRenderer = glRenderer
        self.setMinimumWidth(200)
        self.initUI()
    
    def initUI(self):
        self.widgetContainer = QWidget()
        self.layout = QFormLayout()
        self.layout.setContentsMargins(4,4,4,4)
        self.zoomSlider = QSlider(Qt.Orientation.Horizontal)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(50)
        self.zoomSlider.setValue(10)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.valueChanged.connect(self.updateZoom)

        self.zoomLabel = QLabel("Zoom")
        self.zoomLabel.setFont(QFont("Roboto", 14, QFont.Weight.Bold))
        self.zoomLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoomLabel.setFixedHeight(20)

        self.objectList = QListWidget()
        self.objectList.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        self.objectList.setContentsMargins(2,2,2,2)
        self.objectList.itemAlignment = Qt.AlignmentFlag.AlignCenter

        listItems = ["Object 1", "Object 2", "Object 3"]
        for itemName in listItems:
            item = QListWidgetItem(itemName)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.objectList.addItem(item)

        self.layout.addWidget(self.zoomLabel)
        self.layout.addWidget(self.zoomSlider)
        self.layout.addWidget(self.objectList)
        self.widgetContainer.setLayout(self.layout)
        self.setWidget(self.widgetContainer)
        

    def updateZoom(self, value):
        self.glRenderer.updateZoom(value/10.0)

 