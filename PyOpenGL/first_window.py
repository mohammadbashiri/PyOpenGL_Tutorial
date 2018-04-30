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

    while not glfw.window_should_close(mywin):

        glfw.swap_buffers(mywin)  # swap the front and back buffer
        glfw.poll_events()  # listen for events

if __name__ == "__main__":
    main()