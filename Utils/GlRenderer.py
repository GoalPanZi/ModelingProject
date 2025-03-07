import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Utils.Object import Object, ObjectType
from Utils.Camera2D import Camera2D

class GlRenderer(QOpenGLWidget):
    def __init__(self, width, height, parent = None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.ratio = width / height
        
        self.objects : list[Object] = []
        self.camera = Camera2D(self.ratio)
        self.shaderlist : list[str] = ["lineShader"]
        self.shaderPrograms : dict[str, ShaderProgram] = {}

    def initializeGL(self):
        self.makeCurrent()

        for shaderName in self.shaderlist:
            with open(f"Utils/Shaders/{shaderName}.vert", 'r') as file:
                vertShaderSource = file.read()
                vertShader = compileShader(vertShaderSource, GL_VERTEX_SHADER)

            with open(f"Utils/Shaders/{shaderName}.frag", 'r') as file:
                fragShaderSource = file.read()
                fragShader = compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
            shaderProgram = compileProgram(vertShader,fragShader)
            self.shaderPrograms[shaderName] = shaderProgram

        for shaderName in self.shaderlist:
            glUseProgram(self.shaderPrograms[shaderName])
            bindingLocation = glGetUniformLocation(self.shaderPrograms[shaderName], "transform")
            glUniformMatrix4fv(bindingLocation, 1, GL_FALSE, self.camera.getProjection())
            bindingLocation = glGetUniformLocation(self.shaderPrograms[shaderName], "color")
            glUniform4f(bindingLocation, 1.0, 1.0, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)

        
        xAxis = np.array([[-10.0, 0.0], [10.0, 0.0]], dtype= np.float32)
        yAxis = np.array([[0.0, 10.0], [0.0, -10.0]], dtype= np.float32) 

        xCoords = np.linspace(-10.0,10.0, 1500).astype(dtype=np.float32)
        g1YCoords = np.sin(5* np.pi * xCoords) * xCoords
        g1 = np.column_stack([xCoords,g1YCoords])

        gridData = []
        for i in range(-10,10):
            gridData.append([-10.0, i])
            gridData.append([10.0, i])
            gridData.append([i, -10.0])
            gridData.append([i, 10.0])

        grid = np.array(gridData, dtype=np.float32)

        self.objects.append(Object(xAxis, ObjectType.LINE))
        self.objects.append(Object(yAxis, ObjectType.LINE))
        self.objects.append(Object(g1, ObjectType.LINE))
        self.objects.append(Object(grid, ObjectType.LINES))
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        self.ratio = width / height
        self.camera.setRatio(self.ratio)
        self.updateTransform()

    def updateTransform(self):
        for shaderName in self.shaderlist:
            glUseProgram(self.shaderPrograms[shaderName])
            bindingLocation = glGetUniformLocation(self.shaderPrograms[shaderName], "transform")
            glUniformMatrix4fv(bindingLocation, 1, GL_FALSE, self.camera.getProjection())
        
        self.update()

    def updateZoom(self, value):
        self.camera.setZoom(value)
        self.updateTransform()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.camera.zoomIn()
        else:
            self.camera.zoomOut()
        self.updateTransform()

    def render(self):
        for object in self.objects:
            match (object.objectType):
                case ObjectType.LINE:
                    glUseProgram(self.shaderPrograms["lineShader"])
                    glBindVertexArray(object.vao)
                    glDrawArrays(GL_LINE_STRIP, 0, len(object.vertices))

                case ObjectType.LINES:
                    glUseProgram(self.shaderPrograms["lineShader"])
                    glBindVertexArray(object.vao)
                    glDrawArrays(GL_LINES, 0, len(object.vertices))

                case ObjectType.TRIANGLE:
                    glUseProgram(self.shaderPrograms["triangleShader"])
                    glBindVertexArray(object.vao)

                    if object.indices is not None:
                        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, object.ebo)
                        glDrawElements(GL_TRIANGLES, len(object.indices), GL_UNSIGNED_INT, None)
                    else:
                        glDrawArrays(GL_TRIANGLES, 0, len(object.vertices))

    def resize(self, width, height):
        self.resizeGL(width, height)
        self.updateTransform()

