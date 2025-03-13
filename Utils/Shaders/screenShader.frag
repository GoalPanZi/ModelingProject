#version 450
layout(location = 0) out vec4 outColor;
layout(location = 1) out uint outID;

uniform vec4 color;
uniform uint objectID;

void main() {
    outColor = color;
    outID = objectID;
}