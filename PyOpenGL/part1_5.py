import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

def main():

    # initialize glfw
    if not glfw.init():
        return

    # create a window
    h = 800
    w = 600
    mywin = glfw.create_window(w, h, "My Window", None, None)

    # check if the window was initialized
    if not mywin:
        glfw.terminate()
        return

    # set the created window as the current context
    glfw.make_context_current(mywin)


    # create a mesh
    triangle = [-.5, -.5, 0.,
                0., .5, 0.,
                .5, -.5, 0.]
    triangle = np.array(triangle, dtype=np.float32)

    # create the shader
    vertex_shader = """
    #version 330
    in vec4 fragCoord;
    void main()
    {
        gl_Position = fragCoord;
    }
    """

    fragment_shader = """
    #version 330
    void main()
    {
        gl_FragColor = vec4(1.0, 1.0, 0.0, .1);
    }
    """

    # create the shader program (combines shader objects)
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    """
    now we have to copy the data for the triangle to onto the graphics card
    by using a unit called Vertext Buffer Object (VBO). To do this we:
    1. generate an empty buffer.
    2. set it as the current buffer in OpenGL's state machine by "binding"
    3. copy the points into the currently bound buffer
    """
    VBO = glGenBuffers(1) # create empty buffer
    glBindBuffer(GL_ARRAY_BUFFER, VBO) # bind it
    glBufferData(GL_ARRAY_BUFFER, triangle.shape[0] * 4, triangle, GL_STATIC_DRAW) # copy the triangle data into the buffer


    glEnableVertexAttribArray(0)  # enable the vertex attribute in position 0
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    """
    glVertexAttribPointer function defines the layout of our first vertex buffer;
    "0" means define the layout for attribute number 0.
    "3" means that the variables are vec3 made from every 3 floats (GL_FLOAT) in the buffer.
    """
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