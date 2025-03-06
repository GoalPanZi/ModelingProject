import glfw
import numpy as np
from Utils.Object import Object, ObjectType
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
        
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)

        if not self.window:
            print("Failed to create window")
            glfw.terminate()
            return
        
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.keyCallback)
        glfw.set_scroll_callback(self.window, self.scrollCallback)
        glfw.set_cursor_pos_callback(self.window, self.cursorPosCallback)
        glfw.set_mouse_button_callback(self.window, self.mouseButtonCallback)
        glfw.set_window_size_callback(self.window, self.windowSizeCallback)

        # Initialize renderer
        self.renderer = Renderer(self.ratio)

        self.setup()

    def keyCallback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def scrollCallback(self, window, xoffset, yoffset):
        if yoffset > 0:
            self.renderer.zoomIn()
        elif yoffset < 0:
            self.renderer.zoomOut()

    def cursorPosCallback(self, window, xpos, ypos):
        x = float(xpos) / float(self.width) * self.ratio
        y = float(ypos) / float(self.height)
        self.renderer.move(x, y)

    def mouseButtonCallback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            x = float(x) / float(self.width) * self.ratio
            y = float(y) / float(self.height)
            self.renderer.startDragging(x, y)
        elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
            self.renderer.stopDragging()

    def windowSizeCallback(self, window, width, height):
        self.width = width
        self.height = height
        self.ratio = width / height
        self.renderer.setWindowSize(width, height)

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.draw()
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def setup(self):
        pass

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.renderer.render(self.objects)

    def addLine(self, vertices):
        line = Object(vertices=vertices, objectType=ObjectType.LINE)
        self.objects.append(line)

    def addLines(self, vertices):
        lines = Object(vertices=vertices, objectType=ObjectType.LINES)
        self.objects.append(lines)

    def addGraph(self, vertices):
        graph = Object(vertices=vertices, objectType=ObjectType.LINE)
        self.objects.append(graph)

    



