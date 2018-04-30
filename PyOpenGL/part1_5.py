import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
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

    # set the created window as the current context
    glfw.make_context_current(mywin)


    # create a mesh
    triangle = [-.5, -.5, 0., 1., 0., 0.,
                0., .5, 0.,   0., 1., 0.,
                .5, -.5, 0.,  0., 0., 1.]
    triangle = np.array(triangle, dtype=np.float32)

    # create the shader
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # create the shader program (combines shader objects)
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1) # create empty buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO) # bind it
    glBufferData(GL_ARRAY_BUFFER, triangle.shape[0] * 4, triangle, GL_STATIC_DRAW) # copy the triangle data into the buffer


    glEnableVertexAttribArray(0)  # 0 is the index of position attribute in vertex shader
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)  # 1 is the index of color attribute in vertex shader
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


    glUseProgram(shader)

    # add some color (background)
    glClearColor(.2, .3, .2, 1.0)
    '''----------------------------------------------
                    Draw Loop
    ----------------------------------------------'''
    while not glfw.window_should_close(mywin):
        # put everything that you wanna be drawn here
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 3)
        """
        Explanation: glDrawArrays
        """

        glfw.swap_buffers(mywin)  # swap the front and back buffer
        glfw.poll_events()  # listen for events

    glfw.destroy_window(mywin)
    glfw.terminate()


if __name__ == "__main__":
    main()