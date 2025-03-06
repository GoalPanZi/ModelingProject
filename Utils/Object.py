import numpy as np
from OpenGL.GL import *
from enum import Enum

class ObjectType(Enum):
    LINE = 0
    TRIANGLE = 1

class Object:
    def __init__(self, vertices : np.ndarray, objectType : ObjectType, indices : np.ndarray = None):
        self.vertices = vertices
        self.indices = indices
        self.objectType = objectType
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
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
            
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
