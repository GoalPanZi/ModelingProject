#version 330 core
layout(location = 0) out vec4 FragColor;
layout(location = 1) out uint outID;
uniform vec4 color;
uniform uint objectID;

void main()
{
    FragColor = color;
    outID = objectID;
}
