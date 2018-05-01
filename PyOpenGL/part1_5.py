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
    w = 600
    mywin = glfw.create_window(w, h, "My Window", None, None)

    # check if the window is initialized
    if not mywin:
        glfw.terminate()
        return

    # set the created window the current context
    glfw.make_context_current(mywin)

    # create a mesh
                # psotion        #color
    triangle = [-.5, -.5, 0.,  1., 0., 0.,
                 0.,  .5, 0.,  0., 1., 0.,
                 .5, -.5, 0.,  0., 0., 1.]

    triangle = np.array(triangle, dtype=np.float32)


    # now we pass these information to the GPU (creating mesh program)
    # vertex shader
    vertex_shader="""
    #version 330
    in vec3 position;
    in vec3 color;
    out vec3 newColor;
    void main(){
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    # fragment shader
    fragment_shader="""
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main(){
        outColor = vec4(newColor, 1.0f);
    }
    """

    # compile shader program (combine shader objects)
    shader = glShader.compileProgram(glShader.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                     glShader.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # send the information to GPU (create VBO, bind and copy data)
    vbo = glGenBuffers(1)  # create vbo
    glBindBuffer(GL_ARRAY_BUFFER, vbo)  # bind it
    glBufferData(GL_ARRAY_BUFFER, triangle.shape[0] * 4, triangle, GL_STATIC_DRAW)

    # now we have to enable and pass the attributes specifically
    # enable and pass position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

    # enable and pass color attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # and finally, enable the shader program
    glUseProgram(shader)

    # change the background color
    glClearColor(.6, 0., .15, 1.)
    # draw loop
    while not glfw.window_should_close(mywin):

        # clear color and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw the triangle (primitive, starting index, number of indices to render)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(mywin)  # swap front and back buffer
        glfw.poll_events()  # keep receiving events

    # after exit (closing window), destroy window object and terminate glfw
    glfw.destroy_window(mywin)
    glfw.terminate()

if  __name__ == "__main__":
    main()