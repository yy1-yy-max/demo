// example_shader.glsl
// Minimal GLSL style pseudo-shader for point-sprite instanced rendering.
// Note: TouchDesigner GLSL MAT expects specific uniforms/attributes — treat this as a starting point.
// Vertex: position comes from instance attribute, apply model-view-projection.
// Fragment: sample sprite texture or use instance color.

////////// Vertex shader (GLSL 330 style) //////////
#version 330 core
layout(location = 0) in vec3 inPosition;       // prototype vertex (usually 0,0,0)
layout(location = 1) in vec3 instancePos;     // per-instance position attribute
layout(location = 2) in vec3 instanceColor;   // per-instance color
layout(location = 3) in float instanceScale;  // per-instance scale

uniform mat4 uModelViewProj;

out vec3 vColor;
out float vPointSize;

void main() {
    vec3 pos = instancePos + inPosition * instanceScale;
    gl_Position = uModelViewProj * vec4(pos, 1.0);
    vColor = instanceColor;
    vPointSize = instanceScale; // or scale * constant
    // For GL_POINTS:
    gl_PointSize = max(1.0, vPointSize);
}

////////// Fragment shader //////////
#version 330 core
in vec3 vColor;
in float vPointSize;

out vec4 fragColor;

uniform sampler2D uSpriteTex; // optional sprite texture
uniform bool uUseTexture;

void main() {
    vec4 col = vec4(vColor, 1.0);
    if (uUseTexture) {
        // sample using gl_PointCoord for point sprite
        vec4 t = texture(uSpriteTex, gl_PointCoord);
        fragColor = col * t;
    } else {
        fragColor = col;
    }
}