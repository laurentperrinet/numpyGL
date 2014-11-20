#!/usr/bin/env python
# 
# Load a texture from an image file and map it to a quad.
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
import array
import random

# try:
#   import OpenGL.GLUT as glut
#   import OpenGL.GL as gl
#   import OpenGL.GLU as glu
# except:
#   print ''' Error PyOpenGL not installed properly !!'''
#   sys.exit(  )
# 
do_fs = True
do_fs = False
# Window information
# ------------------
import pyglet
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
N_screen = len(screens) # number of screens
N_screen = 1# len(screens) # number of screens
assert N_screen == 1 # we should be running on one screen only

from pyglet.window import Window

if do_fs:
    win_0 = Window(screen=screens[0], fullscreen=True, resizable=True)
else:
    win_0 = Window(width=screen.width*2/3, height=screen.height*2/3, screen=screens[0], fullscreen=False, resizable=True)
    win_0.set_location(screen.width/3, screen.height/3)
import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt
import numpy as np
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH) #
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glDepthFunc(gl.GL_LEQUAL)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)# gl.GL_FASTEST)# gl.GL_NICEST)# GL_DONT_CARE)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glDisable(gl.GL_CLIP_PLANE0)
    gl.glDisable(gl.GL_CLIP_PLANE1)
    gl.glDisable(gl.GL_CLIP_PLANE2)
    gl.glDisable(gl.GL_CLIP_PLANE3)
    return pyglet.event.EVENT_HANDLED

win_0.on_resize = on_resize
win_0.set_visible(True)

@win_0.event
def on_resize(width, height):
    print 'The window was resized to %dx%d' % (width, height)

@win_0.event
def on_draw():
	"""Glut init function."""
#         texture = RandomTexture( 256, 256 )
        N_X, N_Y = 256, 256
#         tmpList = [ random.randint(0, 255) \
# 			for i in range( 3 * N_X * N_Y ) ]
        tmpList = np.random.randint(0, high=255, size=3 * N_X * N_Y).tolist()
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
# 	glut.glutSwapBuffers (  )


@win_0.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.TAB:
        if win_0.fullscreen:
            win_0.set_fullscreen(False)
            win_0.set_location(screen.width/3, screen.height/3)
        else:
            win_0.set_fullscreen(True)
    elif symbol == pyglet.window.key.SPACE:
        do_firstperson = not(do_firstperson)
    elif symbol == pyglet.window.key.LEFT:
        s.rot_heading_fp += s.inc_heading_fp
    elif symbol == pyglet.window.key.RIGHT:
        s.rot_heading_fp -= s.inc_heading_fp

def _test():
    import doctest
    doctest.testmod()
#####################################
import time
t0 = time.time()
def callback(dt):
    global t0
    print 'FPS=', 1./(time.time()-t0)
    t0 = time.time()

pyglet.clock.schedule(callback)
pyglet.app.run()
