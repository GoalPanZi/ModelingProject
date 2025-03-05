import glfw
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader

#Constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200
RATIO = WINDOW_WIDTH / WINDOW_HEIGHT
TITLE = "Runge-Kutta Demo"
BACKGROUND_COLOR = (26.0/255, 26.0/255, 26.0/255, 1.0)
ZERO_POSITION = (-0.5, -0.5)

#Shader Codes
VERTEX_SHADER_CODE = """
#version 330 core
layout (location = 0) in vec2 aPos;
uniform mat4 transform;
void main()
{
    gl_Position = transform * vec4(aPos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER_CODE = """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

VERTEX_SHADER_CODE_FOR_TEXT = """
#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aTexCoords;
uniform mat4 transform;

out vec2 TexCoords;

void main()
{
    gl_Position = transform * vec4(aPos, 0.0, 1.0);
    TexCoords = aTexCoords;
}
"""

FRAGMENT_SHADER_CODE_FOR_TEXT = """
#version 330 core
in vec2 TexCoords;
out vec4 fragColor;

uniform sampler2D textureMap;

void main()
{   
    vec4 sampled = texture(textureMap, TexCoords);
    if (sampled.a < 0.1) discard;
    fragColor = sampled;
}
"""

#Generate Function
def generateFunctionData():
    x = np.linspace(-0.5, 1.5, 1000)
    y = np.log(x+1.0) * x * x * 0.2
    vertices = np.column_stack((x, y)).astype(np.float32)
    return vertices

def generateAxisData():
    x = np.linspace(-0.5, 1.5, 2)
    y = np.zeros_like(x)
    xAxis = np.column_stack((x, y)).astype(np.float32)
    yAxis = np.column_stack((y, x)).astype(np.float32)
    return xAxis, yAxis

def generateGridData():
    ymin = -0.5
    ymax = 1.5
    xmin = -0.5
    xmax = 1.5

    x = np.linspace(-0.5, 1.5, 13)
    xgrid = np.zeros((len(x)*2, 2)).astype(np.float32)
    for i in range(len(x)):
        xgrid[i*2][0] = x[i]
        xgrid[i*2][1] = ymin
        xgrid[i*2+1][0] = x[i]
        xgrid[i*2+1][1] = ymax
    y = np.linspace(-0.5, 1.5, 13)
    ygrid = np.zeros((len(y)*2, 2)).astype(np.float32)
    for i in range(len(y)):
        ygrid[i*2][0] = xmin
        ygrid[i*2][1] = y[i]
        ygrid[i*2+1][0] = xmax
        ygrid[i*2+1][1] = y[i]
    return xgrid, ygrid

def loadTextureOfCharacter(character, fontSize=32):
    font = ImageFont.load_default()
    textSize = (fontSize*len(character), fontSize)
    image = Image.new("RGBA", textSize, (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), character, font=font, fill=(0, 255, 255, 255))

    textData = np.array(image)
    textureId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureId)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textSize[0], textSize[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return textureId, textSize

#Shader Program getter
def getShaderProgram(VertexShaderCode, FragmentShaderCode):
    vertexShader = compileShader(VertexShaderCode, GL_VERTEX_SHADER)
    fragmentShader = compileShader(FragmentShaderCode, GL_FRAGMENT_SHADER)
    return compileProgram(vertexShader, fragmentShader)

#Get the transformation matrix
def getTransformationMatrix(ratio, dx, dy):
    return np.array([
        [1, 0, 0, 0],
        [0, ratio, 0, 0],
        [0, 0, 1, 0],
        [dx, dy, 0, 1]
    ])

#Create Buffer from Data
def createBuffer(data):
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO

#Render Text
def renderText(textureID, textSize, x, y):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)

    glBegin(GL_QUADS)
    
    glVertex2f(x, y)
    glTexCoord2f(0, 0)
    glVertex2f(x+2*textSize[0]/WINDOW_WIDTH, y)
    glTexCoord2f(1, 0)
    glVertex2f(x+2*textSize[0]/WINDOW_WIDTH, y+2*textSize[1]/WINDOW_HEIGHT)
    glTexCoord2f(1, 1)
    glVertex2f(x, y+2*textSize[1]/WINDOW_HEIGHT)
    glTexCoord2f(0, 1)
    glEnd()
    glDisable(GL_TEXTURE_2D)


#Main function
def main():
    #Initialize glfw
    if not glfw.init():
        print("Failed to initialize GLFW!")
        return
    
    #Create window
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, None, None)
    if not window:
        print("Failed to create window!")
        glfw.terminate()
        return
    
    #Make the context current
    glfw.make_context_current(window)

    #Get the transformation matrix
    transformationMatrix = getTransformationMatrix(RATIO, ZERO_POSITION[0], ZERO_POSITION[1])

    #Get the shader program
    shaderProgram = getShaderProgram(VERTEX_SHADER_CODE, FRAGMENT_SHADER_CODE)
    shaderProgramForText = getShaderProgram(VERTEX_SHADER_CODE_FOR_TEXT, FRAGMENT_SHADER_CODE_FOR_TEXT)

    #Load the texture of the character
    textureId, textSize = loadTextureOfCharacter("A",50)

    #Generate Function Data
    functionData = generateFunctionData()
    xAxisData, yAxisData = generateAxisData()
    xgridData, ygridData = generateGridData()

    #Create Buffer
    functionVAO = createBuffer(functionData)
    xAxisVAO = createBuffer(xAxisData)
    yAxisVAO = createBuffer(yAxisData)
    xgridVAO = createBuffer(xgridData)
    ygridVAO = createBuffer(ygridData)


    #Set the transformation matrix
    glUseProgram(shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transformationMatrix)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClearColor(*BACKGROUND_COLOR)
        glClear(GL_COLOR_BUFFER_BIT)
        
        #Draw the grid
        glUseProgram(shaderProgram)
        glBindVertexArray(xgridVAO)
        glLineWidth(1.0)
        glDrawArrays(GL_LINES, 0, len(xgridData))
        glBindVertexArray(0)

        glBindVertexArray(ygridVAO)
        glLineWidth(1.0)
        glDrawArrays(GL_LINES, 0, len(ygridData))
        glBindVertexArray(0)

        #Draw the text
        glUseProgram(shaderProgramForText)
        glUniformMatrix4fv(glGetUniformLocation(shaderProgramForText, "transform"), 1, GL_FALSE, transformationMatrix)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textureId)
        glUniform1i(glGetUniformLocation(shaderProgramForText, "textureMap"), 0)
        renderText(textureId, textSize, 0.1, 0.1)

        #Draw the axis
        glUseProgram(shaderProgram)
        glBindVertexArray(xAxisVAO)
        glLineWidth(2.0)
        glDrawArrays(GL_LINE_STRIP, 0, len(xAxisData))
        glBindVertexArray(0)

        glBindVertexArray(yAxisVAO)
        glLineWidth(2.0)
        glDrawArrays(GL_LINE_STRIP, 0, len(yAxisData))
        glBindVertexArray(0)

        #Draw the function
        glUseProgram(shaderProgram)
        glBindVertexArray(functionVAO)
        glLineWidth(3.0)
        glDrawArrays(GL_LINE_STRIP, 0, len(functionData))
        glBindVertexArray(0)

        glfw.swap_buffers(window)

    #Terminate glfw
    glfw.terminate()



#Entry point
if __name__ == "__main__":
    main()
    

