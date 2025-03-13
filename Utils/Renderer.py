from OpenGL.GL import *
from Utils.Object import Object, RenderUnitType, RenderUnit, lineUnit, linesUnit
from Utils.Camera2D import Camera2D
from Utils.ShaderManager import ShaderManager
import numpy as np

class Renderer:
    def __init__(self, width : int, height : int):
        self.width = width
        self.height = height
        self.ratio = width / height
        self.camera = Camera2D(width, height)
        self.renderUnits : dict[RenderUnitType, list[RenderUnit]] = {renderUnitType : [] for renderUnitType in RenderUnitType}
        self.shaderManager = None
        self.initialize()
        

    def initialize(self):
        self.shaderManager = ShaderManager()
        self.updateTransform()
        # msaa framebuffer
        self.msaaFramebuffer = glGenFramebuffers(1)
        self.msaaScreenBuffer = glGenRenderbuffers(1)
        self.msaaIdBuffer = glGenRenderbuffers(1)
        self.msaaDepthBuffer = glGenRenderbuffers(1)

        self.framebuffer = glGenFramebuffers(1)
        self.screenBuffer = glGenRenderbuffers(1)
        self.idBuffer = glGenRenderbuffers(1)
        self.depthBuffer = glGenRenderbuffers(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.msaaFramebuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.msaaScreenBuffer)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_RGBA8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, self.msaaScreenBuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.msaaIdBuffer)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_R32UI, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_RENDERBUFFER, self.msaaIdBuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.msaaDepthBuffer)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_DEPTH24_STENCIL8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.msaaDepthBuffer)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("MSAA Framebuffer is not complete")

        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.screenBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, self.screenBuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.idBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_R32UI, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_RENDERBUFFER, self.idBuffer)

        glBindRenderbuffer(GL_RENDERBUFFER, self.depthBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.depthBuffer)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Framebuffer is not complete")

        glBindFramebuffer(GL_FRAMEBUFFER, self.msaaFramebuffer)

        glDrawBuffers(2, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1])

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

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

        self.addObject(axisObject)

        gridData = []
        for i in range(-10,10):
            gridData.append([-10.0, i])
            gridData.append([10.0, i])
            gridData.append([i, -10.0])
            gridData.append([i, 10.0])

        grid = np.array(gridData, dtype=np.float32)

        gridUnit = linesUnit(grid)

        backgroundObject = Object(2)
        backgroundObject.addRenderUnit(gridUnit)

        self.addObject(backgroundObject)

        print("Camera Projection Matrix:")
        print(self.camera.getProjection())

    def addObject(self, object : Object):
        for renderUnitType in RenderUnitType:
            for renderUnit in object.renderUnits[renderUnitType]:
                self.renderUnits[renderUnitType].append(renderUnit)

    def render(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.msaaFramebuffer)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for renderUnitType in RenderUnitType:
            self.shaderManager.useShaderProgram(renderUnitType)
            self.checkGLError()
            for renderUnit in self.renderUnits[renderUnitType]:
                config = renderUnit.renderConfig
                self.shaderManager.setUniforms(config)
                glBindVertexArray(config.vao)
                if config.indicesCount > 0:
                    glDrawElements(config.renderFlag, config.indicesCount, GL_UNSIGNED_INT, None)
                else:
                    glDrawArrays(config.renderFlag, 0, config.vertexCount)
                glBindVertexArray(0)
                self.checkGLError()
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.msaaFramebuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.framebuffer)

        glBlitFramebuffer(0, 0, self.width, self.height, 
                        0, 0, self.width, self.height,
                        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT, 
                        GL_NEAREST)

        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.framebuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)

        glBlitFramebuffer(0, 0, self.width, self.height, 
                        0, 0, self.width, self.height,
                        GL_COLOR_BUFFER_BIT, 
                        GL_NEAREST)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
            

    def setZoom(self, zoom : float):
        self.camera.setZoom(zoom)
        self.updateTransform()

    def zoomIn(self):
        self.camera.zoomIn()
        self.updateTransform()

    def zoomOut(self):
        self.camera.zoomOut()
        self.updateTransform()

    def updateTransform(self):
        transformMatrix = self.camera.getProjection()
        self.shaderManager.setTransform(transformMatrix)
        
    def checkGLError(self):
        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL Error: {error}")


