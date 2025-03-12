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
        self.objectTypes = [ObjectType.LINE, ObjectType.LINES, ObjectType.TRIANGLES]
        self.objectTypeNames = ["line", "line", "triangle"]
        self.objects : dict[ObjectType, list[Object]] = {objectType: [] for objectType in self.objectTypes}
        self.camera = Camera2D(self.ratio)
        self.shaderPrograms : dict[ObjectType, ShaderProgram] = {}
        self.fbo : int = None
        self.screenTexture : int = None
        self.renderTarget = None

    def initializeGL(self):
        self.prepareShader()
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.screenTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.screenTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.screenTexture, 0)

        self.idTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.idTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, self.width, self.height, 0, GL_RED, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, self.idTexture, 0)

        self.depthBuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depthBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.depthBuffer)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR::FRAMEBUFFER:: Framebuffer is not complete!")


        self.renderTarget = [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1]
        glDrawBuffers(2, self.renderTarget)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        
        xAxis = np.array([[-2.0, 0.0], [2.0, 0.0]], dtype= np.float32)
        yAxis = np.array([[0.0, 2.0], [0.0, -2.0]], dtype= np.float32) 

        xCoords = np.linspace(-2.0,2.0, 500).astype(dtype=np.float32)
        g1YCoords = np.sin(5* np.pi * xCoords) * xCoords
        g1 = np.column_stack([xCoords,g1YCoords])

        gridData = []
        for i in range(-10,10):
            gridData.append([-10.0, i])
            gridData.append([10.0, i])
            gridData.append([i, -10.0])
            gridData.append([i, 10.0])

        grid = np.array(gridData, dtype=np.float32)

        self.objects[ObjectType.LINE].append(Object(xAxis, ObjectType.LINE))
        self.objects[ObjectType.LINE].append(Object(yAxis, ObjectType.LINE))
        self.objects[ObjectType.LINE].append(Object(g1, ObjectType.LINE))
        self.objects[ObjectType.LINES].append(Object(grid, ObjectType.LINES))

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.render()
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.resetFBO(width, height)
        self.width = width
        self.height = height
        self.ratio = width / height
        self.camera.setRatio(self.ratio)
        self.updateTransform()

    def resetFBO(self, width, height):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        glBindTexture(GL_TEXTURE_2D, self.screenTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)

        glBindTexture(GL_TEXTURE_2D, self.idTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_R8, width, height, 0, GL_RED, GL_UNSIGNED_BYTE, None)

        glBindRenderbuffer(GL_RENDERBUFFER, self.depthBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def updateTransform(self):
        for objectType in self.objectTypes:
            glUseProgram(self.shaderPrograms[objectType])
            bindingLocation = glGetUniformLocation(self.shaderPrograms[objectType], "transform")
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
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for objectType in self.objectTypes:
            glUseProgram(self.shaderPrograms[objectType])
            for object in self.objects[objectType]:
                match (objectType):
                    case ObjectType.LINE:
                        glBindVertexArray(object.vao)
                        glDrawArrays(GL_LINE_STRIP, 0, len(object.vertices))

                    case ObjectType.LINES:
                        glBindVertexArray(object.vao)
                        glDrawArrays(GL_LINES, 0, len(object.vertices))

                    case ObjectType.TRIANGLE:
                        glBindVertexArray(object.vao)
                        if object.indices is not None:
                            glDrawElements(GL_TRIANGLES, len(object.indices), GL_UNSIGNED_INT, None)
                        else:
                            glDrawArrays(GL_TRIANGLES, 0, len(object.vertices))

    def prepareShader(self):
        for objectType in self.objectTypes:
            with open(f"Utils/Shaders/{self.objectTypeNames[objectType.value]}Shader.vert", 'r') as file:
                vertShaderSource = file.read()
                vertShader = compileShader(vertShaderSource, GL_VERTEX_SHADER)

            with open(f"Utils/Shaders/{self.objectTypeNames[objectType.value]}Shader.frag", 'r') as file:
                fragShaderSource = file.read()
                fragShader = compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
            shaderProgram = compileProgram(vertShader,fragShader)
            self.shaderPrograms[objectType] = shaderProgram

        for objectType in self.objectTypes:
            glUseProgram(self.shaderPrograms[objectType])
            bindingLocation = glGetUniformLocation(self.shaderPrograms[objectType], "transform")
            glUniformMatrix4fv(bindingLocation, 1, GL_FALSE, self.camera.getProjection())
            bindingLocation = glGetUniformLocation(self.shaderPrograms[objectType], "color")
            glUniform4f(bindingLocation, 1.0, 1.0, 1.0, 1.0)


    def resize(self, width, height):
        self.resizeGL(width, height)
        self.updateTransform()

