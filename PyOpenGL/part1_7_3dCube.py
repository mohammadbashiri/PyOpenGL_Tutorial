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
    mywin = glfw.create_window(width=w, height=h, title="My Window", monitor=None, share=None)

    # check if the window is created
    if not mywin:
        glfw.terminate()
        return

    # set the window as the current context
    glfw.make_context_current(mywin)

    # create the mesh - cube (has 8 vertices)
             # position      # color
    cube = [-.75, -.75, .5,   1., 0., 0.,
            -.75,  .25, .5,   1., 0., 0.,
             .25,  .25, .5,   1., 0., 0.,
             .25, -.75, .5,   1., 0., 0.,
            -.5, -.5, 1,  0., 0., 1.,
            -.5,  .5, 1,  0., 0., 1.,
             .5,  .5, 1,  0., 0., 1.,
             .5, -.5, 1,  0., 0., 1.]

    # defining all the faces
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               5, 6, 2, 2, 1, 5,
               6, 7, 3, 3, 2, 6,
               4, 7, 3, 3, 0, 4]


    cube = np.array(cube, dtype=np.float32)
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

    # create fragment shader
    fragment_shader = """
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main(){
        outColor = vec4(newColor, 1.0f);
    }
    """

    # create shader program by compile the two shader objects
    shader = glShader.compileProgram(glShader.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                     glShader.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # send the data to GPU
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, cube.shape[0] * 4, cube, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.shape[0] * 4, indices, GL_STATIC_DRAW)

    # define the layout by enabling and passing the vertex attributes
    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # color attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # use the shader program
    glUseProgram(shader)

    glFrontFace(GL_CW)
    glEnable(GL_DEPTH_TEST)

    # draw loop
    while not glfw.window_should_close(mywin):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glfw.swap_buffers(mywin)
        glfw.poll_events()

    glfw.destroy_window(mywin)
    glfw.terminate()

if __name__ == "__main__":
    main()