#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;


vec3 getLight(vec3 color) {
    // ambient light
    vec3 ambient = light.Ia;
    return color * ambient;
}


void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = getLight(color);
    fragColor = vec4(color, 1.0);
}