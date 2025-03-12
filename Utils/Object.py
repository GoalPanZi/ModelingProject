import numpy as np
from OpenGL.GL import *
from enum import Enum
from dataclasses import dataclass

class ObjectType(Enum):
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

        if self.indices is None:
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)

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
