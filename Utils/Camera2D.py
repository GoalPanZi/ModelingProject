from OpenGL.GL import *
import numpy as np
class Camera2D:
    def __init__(self, width : int, height : int):
        self.zoom = 1.0
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.dragging = False
        self.dragStartX = 0.0
        self.dragStartY = 0.0
        self.ratio : float = width / height

    def setRatio(self, ratio : float):
        self.ratio = ratio

    def setZoom(self, zoom : float):
        self.zoom = zoom

    def zoomIn(self):
        self.zoom *= 1.1

    def zoomOut(self):
        self.zoom /= 1.1

    def startDragging(self, x : float, y : float):
        self.dragging = True
        self.dragStartX = x
        self.dragStartY = y

    def stopDragging(self):
        self.dragging = False

    def getProjection(self):
        return np.array([[self.zoom / self.ratio, 0.0, 0.0, 0.0],
                         [0.0, self.zoom, 0.0, 0.0],
                         [0.0, 0.0, 1.0, 0.0],
                         [self.offsetX, self.offsetY, 0.0, 1.0]], dtype=np.float32)

    def move(self, x, y):
        if self.dragging:
            dx = (x - self.dragStartX) * 2.0
            dy = (y - self.dragStartY) * 2.0
            self.offsetX += dx
            self.offsetY -= dy
            self.dragStartX = x
            self.dragStartY = y
