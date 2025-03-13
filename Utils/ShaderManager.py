from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
from OpenGL.GL import *
from Utils.Object import RenderUnitType, RenderConfig
import numpy as np

class ShaderManager:
    def __init__(self):
        self.shaderMap : dict[RenderUnitType, str] = {RenderUnitType.LINE : "lineShader",
                                                      RenderUnitType.LINES : "lineShader",
                                                      RenderUnitType.TRIANGLES : "triangleShader"}
        self.shaderPrograms : dict[str, ShaderProgram] = { "lineShader" : None,
                                                            "triangleShader" : None}

        for shaderName in self.shaderPrograms:
            self.addShaderProgram(shaderName)

    def addShaderProgram(self, shaderName: str):
        with open(f"Utils/Shaders/{shaderName}.vert", "r") as file:
            vertexShader = file.read()
            vertShader = compileShader(vertexShader, GL_VERTEX_SHADER)
        with open(f"Utils/Shaders/{shaderName}.frag", "r") as file:
            fragmentShader = file.read()
            fragShader = compileShader(fragmentShader, GL_FRAGMENT_SHADER)

        self.shaderPrograms[shaderName] = compileProgram(vertShader, fragShader)

    def useShaderProgram(self, shaderName: str):
        glUseProgram(self.shaderPrograms[shaderName])

    def useShaderProgram(self, renderUnitType : RenderUnitType):
        glUseProgram(self.shaderPrograms[self.shaderMap[renderUnitType]])

    def setUniforms(self, renderConfig : RenderConfig):
        glUniform4f(glGetUniformLocation(self.shaderPrograms[self.shaderMap[renderConfig.renderUnitType]], "color"), *renderConfig.color)
        glUniform1ui(glGetUniformLocation(self.shaderPrograms[self.shaderMap[renderConfig.renderUnitType]], "objectID"), renderConfig.objectID)

    def setTransform(self, transformMatrix : np.ndarray):
        for shaderProgram in self.shaderPrograms.values():
            glUseProgram(shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transformMatrix)
            glUseProgram(0)
