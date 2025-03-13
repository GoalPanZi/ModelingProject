import glfw
import numpy as np
from Utils.Object import Object, lineUnit
from Utils.Renderer import Renderer

from OpenGL.GL import *

class ProjectApp:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.ratio = width / height
        self.title = title
        self.window = None
        self.renderer = None
        self.objects : list[Object] = []

    
    def initialize(self):
        if not glfw.init():
            print("Failed to initialize GLFW")
            return
        
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)

        if not self.window:
            print("Failed to create window")
            glfw.terminate()
            return
        
        
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.keyCallback)
        glfw.set_scroll_callback(self.window, self.scrollCallback)

        self.renderer = Renderer(self.width, self.height)

        self.setup()

    def keyCallback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def scrollCallback(self, window, xoffset, yoffset):
        if yoffset > 0:
            self.renderer.zoomIn()
        elif yoffset < 0:
            self.renderer.zoomOut()

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.renderer.render()
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def setup(self):
        xAxis = np.array([
            [-10.0, 0.0],
            [10.0, 0.0]
        ], dtype=np.float32)
        yAxis = np.array([
            [0.0, -10.0],
            [0.0, 10.0]
        ], dtype=np.float32)

        xAxisUnit = lineUnit(xAxis)
        yAxisUnit = lineUnit(yAxis)

        axisObject = Object(1)
        axisObject.addRenderUnit(xAxisUnit)
        axisObject.addRenderUnit(yAxisUnit)

        self.renderer.addObject(axisObject)

    



