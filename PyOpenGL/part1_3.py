import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

def main():

    # initialize glfw
    if not glfw.init():
        return

    # create a window
    w = 800
    h = 600
    mywin = glfw.create_window(w, h, "My Window", None, None)

    # check if window was created
    if not mywin:
        glfw.terminate()
        return

    # Set the created window as the current context
    glfw.make_context_current(mywin)


    # add a triangle
    triangle = [-.5, -.5, 0.,
                .5, -.5, 0.,
                0., .5, 0.]
    triangle = np.array(triangle, dtype=np.float32)


    vertex_shader = """
    #version 330
    in vec4 position;
    void main()
    {
        gl_Position = position;
    }
    """

    fragment_shader = """
    #version 330
    void main()
    {
        gl_FragColor = vec4(1.0f, 1.0f, 0.0f, .1f);
    }
    """

    # compile the shader (this is the shader program)
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # send data to GPU, by creating a vertex buffer object (VBO)
    VBO = glGenBuffers(1)  # create buffer object
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # bind the vertex buffer object (VBO) to array_buffer (basically defining VBO as a vertex attribute)
    glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position") # get the postion from the shader program
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    glUseProgram(shader)

    """
    Explanation of the shader-related commands above:

    glGenBuffer:
    glBindBuffer:
    glBufferData:

    glGetAttribLocation:
    glVertexAttribPointer:
    glEnableVertexAttribArray

    glUseProgram
    """


    # add some color
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
