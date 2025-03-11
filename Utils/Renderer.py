from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
from OpenGL.GL import *
from Utils.Object import Object, ObjectType
from Utils.Camera2D import Camera2D

class Renderer:
    def __init__(self, ratio : float):
        self.shaderlist : list[str] = ["lineShader", "triangleShader"]
        self.shaderPrograms : dict[str, ShaderProgram] = {}
        self.VAO : list[int] = []
        self.VBO : list[int] = []
        self.EBO : list[int] = []
        self.camera : Camera2D = Camera2D(ratio)

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
        
    def render(self, objects : list[Object]):
        for object in objects:
            match (object.objectType):
                case ObjectType.LINE:
                    glUseProgram(self.shaderPrograms["lineShader"])
                    bindingLocation = glGetUniformLocation(self.shaderPrograms["lineShader"], "color")
                    glUniform4f(bindingLocation, object.color[0], object.color[1], object.color[2], object.color[3])
                    glBindVertexArray(object.vao)
                    glLineWidth(object.lineWidth)
                    glDrawArrays(GL_LINE_STRIP, 0, len(object.vertices))

                case ObjectType.LINES:
                    glUseProgram(self.shaderPrograms["lineShader"])
                    bindingLocation = glGetUniformLocation(self.shaderPrograms["lineShader"], "color")
                    glUniform4f(bindingLocation, object.color[0], object.color[1], object.color[2], object.color[3])
                    glBindVertexArray(object.vao)
                    glLineWidth(object.lineWidth)
                    glDrawArrays(GL_LINES, 0, len(object.vertices))

                case ObjectType.TRIANGLES:
                    glUseProgram(self.shaderPrograms["triangleShader"])
                    bindingLocation = glGetUniformLocation(self.shaderPrograms["triangleShader"], "color")
                    glUniform4f(bindingLocation, object.color[0], object.color[1], object.color[2], object.color[3])
                    glBindVertexArray(object.vao)

                    if object.indices is not None:
                        glDrawElements(GL_TRIANGLES, len(object.indices), GL_UNSIGNED_INT, None)
                    else:
                        glDrawArrays(GL_TRIANGLES, 0, len(object.vertices))

    def updateTransform(self):
        for shaderName in self.shaderlist:
            glUseProgram(self.shaderPrograms[shaderName])
            bindingLocation = glGetUniformLocation(self.shaderPrograms[shaderName], "transform")
            glUniformMatrix4fv(bindingLocation, 1, GL_FALSE, self.camera.getProjection())

    def zoomIn(self):
        self.camera.zoomIn()
        self.updateTransform()

    def zoomOut(self):
        self.camera.zoomOut()
        self.updateTransform()

    def move(self, x : float, y : float):
        self.camera.move(x, y)
        self.updateTransform()

    def startDragging(self, x : float, y : float):
        self.camera.startDragging(x, y)

    def stopDragging(self):
        self.camera.stopDragging()

    def setWindowSize(self, width : int, height : int):
        glViewport(0, 0, width, height)
        self.camera.setRatio(width / height)
        self.updateTransform()
