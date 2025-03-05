import glfw
import numpy as np
from Utils.Camera2D import Camera2D
from Utils.Object import Object
from Utils.Renderer import Renderer

from OpenGL.GL import *

class ProjectApp:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self.camera = Camera2D()
        self.objects : list[Object] = []
        self.renderer = Renderer()

    
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

        self.camera.updateProjection()

    def keyCallback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def scrollCallback(self, window, xoffset, yoffset):
        if yoffset > 0:
            self.camera.zoomIn()
        elif yoffset < 0:
            self.camera.zoomOut()

    def cursorPosCallback(self, window, xpos, ypos):
        self.camera.move(xpos, ypos)

    def mouseButtonCallback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            self.camera.startDragging(x, y)
        elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
            self.camera.stopDragging()

    def run(self):
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            glColor3f(0.5, 0.5, 0.5)
            glBegin(GL_TRIANGLES)
            glVertex2f(-5, 0)
            glVertex2f(5, 0)
            glVertex2f(0, 10)
            glEnd()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()



