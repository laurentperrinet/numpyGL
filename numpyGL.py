#!/usr/bin/env python3
#
# Load a texture from an image file and map it to a quad.
#
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import numpy as np

import sys
import array
import random
#
do_fs = True
do_fs = False
# Window information
# # ------------------
import pyglet
platform = pyglet.window.get_platform()
print("platform" , platform)
display = platform.get_default_display()
print("display" , display)
screens = display.get_screens()
print("screens" , screens)
for i, screen in enumerate(screens):
    print('Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y))
N_screen = len(screens) # number of screens
N_screen = 1# len(screens) # number of screens
# assert N_screen == 1 # we should be running on one screen only

import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt
from pyglet.window import Window

window = Window(visible=False, resizable=True, fullscreen=do_fs)

@window.event
def on_draw():
    background.blit_tiled(0, 0, 0, window.width, window.height)
    img.blit(window.width // 2, window.height // 2, 0)

    window.width = img.width
    window.height = img.height
    window.set_visible()

@window.event
def on_draw():
    """Glut init function."""
#         texture = RandomTexture( 256, 256 )
    N_X, N_Y = 256, 256
    N_X, N_Y = screen.height, screen.width
#         tmpList = [ random.randint(0, 255) \
#             for i in range( 3 * N_X * N_Y ) ]
    tmpList = np.random.randint(0, high=255, size=3 * N_X * N_Y).astype('uint8').tolist()
    gl.glClearColor ( 0, 0, 0, 0 )
    gl.glShadeModel( gl.GL_SMOOTH )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR )
    gl.glTexParameterf( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR )
    gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, 3, N_X, N_Y, 0,
                 gl.GL_RGB, gl.GL_UNSIGNED_BYTE, array.array( 'B', tmpList ).tostring() )
    gl.glEnable( gl.GL_TEXTURE_2D )

    """Glut display function."""
    gl.glClear( gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )
    gl.glColor3f( 1, 1, 1 )
    gl.glBegin( gl.GL_QUADS )
    gl.glTexCoord2f( 0, 1 )
    gl.glVertex3f( -1.0, 1.0, 0 )
    gl.glTexCoord2f( 0, 0 )
    gl.glVertex3f( -1.0, -1.0, 0 )
    gl.glTexCoord2f( 1, 0 )
    gl.glVertex3f( 1.0, -1.0, 0 )
    gl.glTexCoord2f( 1, 1 )
    gl.glVertex3f( 1.0, 1.0, 0 )
    gl.glEnd(  )
#     glut.glutSwapBuffers (  )

# @window.event
# def on_key_press(symbol, modifiers):
#     if symbol == pyglet.window.key.TAB:
#         if window.fullscreen:
#             window.set_fullscreen(False)
#             window.set_location(screen.width/3, screen.height/3)
#         else:
#             window.set_fullscreen(True)
# 
def _test():
    import doctest
    doctest.testmod()
#####################################
import time
t0 = time.time()
def callback(dt):
    global t0
    print('FPS=', 1./(time.time()-t0))
    t0 = time.time()

pyglet.clock.schedule(callback)
pyglet.app.run()
