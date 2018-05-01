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

    # create a mesh

