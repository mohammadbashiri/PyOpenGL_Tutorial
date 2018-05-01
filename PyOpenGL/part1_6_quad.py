import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as glShader
import numpy as np


def main():

    # initialize glfw
    if not glfw.init():
        return

    # create a window
    h = 600
    w = 800
    mywin = glfw.create_window(w, h, "My Window", None, None)

    # check if the window was initialized
    if not mywin:
        glfw.terminate()
        return

    # set the window as current context
    glfw.make_context_current(mywin)

    # create a mesh (vertices and indices)
            # position     # color
    quad = [-.5, -.5, 0.,  1., 0., 0.,
            -.5, .5, 0.,   0., 1., 0.,
            .5, .5, 0.,    0., 0., 1.,
            .5, -.5, 0.,   1., 1., 1.]

    indices = [0, 1, 2,
               2, 3, 0]

    quad = np.array(quad, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    # create vertex shader
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec3 newColor;
    void main(){
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main(){
        outColor = vec4(newColor, 1.0f);
    }
    """

    # create shader program (compile the shader objects)
    shader = glShader.compileProgram(glShader.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                     glShader.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # send info to GPU (vbo and ebo)
    # VBO (VERTEX BUFFER OBJECT)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, quad.shape[0] * 4, quad, GL_STATIC_DRAW)

    # EBO (ELEMENT BUFFER OBJECT)
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.shape[0] * 4, indices, GL_STATIC_DRAW)

    # define the layout (by enabling and passing the attributes)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # use the shader program
    glUseProgram(shader)

    while not glfw.window_should_close(mywin):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(mywin)
        glfw.poll_events()

    glfw.destroy_window(mywin)
    glfw.terminate()

if __name__ == "__main__":
    main()