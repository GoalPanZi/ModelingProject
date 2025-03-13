import numpy as np
from OpenGL.GL import *
from enum import Enum
from dataclasses import dataclass

class RenderUnitType(Enum):
    LINE = 0
    LINES = 1
    TRIANGLES = 2

@dataclass
class ObjectConfig:
    color : tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    lineWidth : float = 1.0
    vao : int = None
    vbo : int = None
    ebo : int = None
    
    def set_vao(self, vao : int):
        self.vao = vao

    def set_vbo(self, vbo : int):
        self.vbo = vbo

    def set_ebo(self, ebo : int):
        self.ebo = ebo

<<<<<<< HEAD
@dataclass
class RenderConfig:
    color : tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    objectID : int = 0
    vao : int = None
    vbo : int = None
    ebo : int = None
    vertexCount : int = 0
    indicesCount : int = 0
    renderFlag : int = None
    renderUnitType : RenderUnitType = None


class RenderUnit:
    def __init__(self, vertices : np.ndarray, renderUnitType : RenderUnitType, indices : np.ndarray = None):
        self.vertices = vertices
        self.indices = indices
        self.renderUnitType = renderUnitType
        self.renderConfig = RenderConfig()
        self.renderConfig.renderUnitType = renderUnitType
        
        self.renderConfig.vao = glGenVertexArrays(1)
        print(self.renderConfig.vao)
        glBindVertexArray(self.renderConfig.vao)
=======
class Object:
    def __init__(self, 
                 vertices : np.ndarray, 
                 objectType : ObjectType, 
                 color : tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                 indices : np.ndarray = None, 
                 lineWidth : float = 1.0):
        self.vertices = vertices
        self.indices = indices
        self.objectType = objectType
        self.color = color
        self.lineWidth = lineWidth
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
>>>>>>> 03c31feaf1e063179142544b8dac246c25144752

        self.renderConfig.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.renderConfig.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

<<<<<<< HEAD
        self.renderConfig.vertexCount = len(self.vertices)
        if self.indices is not None:
            self.renderConfig.indicesCount = len(self.indices)

        if self.indices is not None:
            self.renderConfig.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.renderConfig.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

class lineUnit(RenderUnit):
    def __init__(self, vertices : np.ndarray, indices : np.ndarray = None):
        super().__init__(vertices, RenderUnitType.LINE, indices)
        self.renderConfig.renderFlag = GL_LINE_STRIP

class linesUnit(RenderUnit):
    def __init__(self, vertices : np.ndarray, indices : np.ndarray = None):
        super().__init__(vertices, RenderUnitType.LINES, indices)
        self.renderConfig.renderFlag = GL_LINES
class triangleUnit(RenderUnit):
    def __init__(self, vertices : np.ndarray, indices : np.ndarray = None):
        super().__init__(vertices, RenderUnitType.TRIANGLE, indices)
        self.renderConfig.renderFlag = GL_TRIANGLES

class Object:
    def __init__(self, id : int):
        self.renderUnits = {renderUnitType : [] for renderUnitType in RenderUnitType}
        self.id = id

    def addRenderUnit(self, renderUnit : RenderUnit):
        renderUnit.renderConfig.objectID = self.id
        self.renderUnits[renderUnit.renderUnitType].append(renderUnit)
=======
        else:
            self.ebo = glGenBuffers(1)
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
>>>>>>> 03c31feaf1e063179142544b8dac246c25144752
