#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 fragPos;

uniform vec4 color;


void main() {
    fragColor = color;
}