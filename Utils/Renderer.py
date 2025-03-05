from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
from OpenGL.GL import *
from Utils.Object import Object, ObjectType

class Renderer:
    def __init__(self):
        self.shaderlist : list[str] = ["lineShader"]
        self.shaderPrograms : dict[str, ShaderProgram] = {}
        self.VAO : list[int] = []
        self.VBO : list[int] = []
        self.EBO : list[int] = []

        for shaderName in self.shaderlist:
            shaderProgram = compileProgram(
                compileShader(open(f"Shaders/{shaderName}.vert").read(), GL_VERTEX_SHADER),
                compileShader(open(f"Shaders/{shaderName}.frag").read(), GL_FRAGMENT_SHADER)
            )
            self.shaderPrograms[shaderName] = shaderProgram
        
    def render(self, objects : list[Object]):
        for object in objects:
            match (object.objectType):
                case ObjectType.LINE:
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
