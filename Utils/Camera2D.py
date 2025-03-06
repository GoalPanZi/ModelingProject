from OpenGL.GL import *

class Camera2D:
    def __init__(self):
        self.zoom = 1.0
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.dragging = False
        self.dragStartX = 0.0
        self.dragStartY = 0.0

    def setZoom(self, zoom : float):
        self.zoom = zoom
        self.updateProjection()

    def zoomIn(self):
        self.zoom *= 1.1
        self.updateProjection()

    def zoomOut(self):
        self.zoom /= 1.1
        self.updateProjection()

    def startDragging(self, x : float, y : float):
        self.dragging = True
        self.dragStartX = x
        self.dragStartY = y

    def stopDragging(self):
        self.dragging = False

    def updateProjection(self):
        print("projection update call")
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10*self.zoom + self.offsetX, 10*self.zoom + self.offsetX,
                 -10*self.zoom + self.offsetY, 10*self.zoom + self.offsetY, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glOrtho(-10*self.zoom + self.offsetX, 10*self.zoom + self.offsetX,
                 -10*self.zoom + self.offsetY, 10*self.zoom + self.offsetY, -1.0, 1.0)

    def move(self, x, y):
        if self.dragging:
            dx = (x - self.dragStartX) * self.zoom * 0.02
            dy = (y - self.dragStartY) * self.zoom * 0.02
            self.offsetX -= dx
            self.offsetY += dy
            self.dragStartX = x
            self.dragStartY = y
            self.updateProjection()
            
