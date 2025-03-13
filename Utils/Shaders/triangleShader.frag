#version 330 core
<<<<<<< HEAD
layout(location = 0) out vec4 FragColor;
layout(location = 1) out uint outID;
uniform vec4 color;
uniform uint objectID;
=======
out vec4 FragColor;
uniform vec4 color;
>>>>>>> 03c31feaf1e063179142544b8dac246c25144752

void main()
{
    FragColor = color;
<<<<<<< HEAD
    outID = objectID;
=======
>>>>>>> 03c31feaf1e063179142544b8dac246c25144752
}
