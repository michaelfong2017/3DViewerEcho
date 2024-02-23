#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 fragPos;


void main() {
    vec3 color = vec3(0.57, 0.0, 0.63);
    fragColor = vec4(color, 1.0);
}