#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A simple framework to display numpy array on a screen. And only that.

Heavily based on https://github.com/vispy/vispy/blob/master/examples/tutorial/gloo/textured_quad.py
by Nicolas Rougier and more example scripts in the vispy documentation.

"""
from __future__ import division, print_function, absolute_import
__author__ = "Laurent Perrinet INT - CNRS"
__version__ = '0.1'
__licence__ = 'BSD licence'

import numpy as np
import time

from vispy import app
from vispy import gloo
#--------------------------------------------------------------------------
# A simple texture quad
data = np.zeros(4, dtype=[('a_position', np.float32, 2),
                          ('a_texcoord', np.float32, 2)])
data['a_position'] = np.array([[-1, -1], [+1, -1], [-1, +1], [+1, +1]])
data['a_texcoord'] = np.array([[1, 0], [1, 1.], [0, 0], [0, 1.]])


vertex = """
    attribute vec2 a_position;
    attribute vec2 a_texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
        v_texcoord = a_texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""

class Canvas(app.Canvas):
    """
    The client initializes and updates the display where stimulations and
    camera take will occur.
    """
    def __init__(self, stimulus, 
            fullscreen=True, interpolation='linear',
            timeline=np.linspace(0, 4, 4*30), keys='interactive', title='welcome to numpyGL'):
        self.stimulus = stimulus
        self.timeline = timeline
        app.use_app('pyglet')
        super(Canvas, self).__init__(keys=keys, title=title)
        width, height = self.physical_size
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program.bind(gloo.VertexBuffer(data))
        #self.program['a_position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        #self.program['a_texcoord'] = [(1, 1), (1, 0), (0, 1), (0, 0)]
        #self.program['texture'] = self.stimulus(t=0.)
        self.program['texture'] = gloo.Texture2D(self.stimulus(t=0.), interpolation=interpolation)
        gloo.set_viewport(0, 0, width, height)
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.start = time.time() # use the timer above
        self.fullscreen = fullscreen
        self.show()

    def on_key_press(self, event):
        if event.key == 'F':
            fullscreen = not self.fullscreen
            self.fullscreen = fullscreen

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        t = time.time()-self.start
        if t  < self.timeline.max():
            width, height = self.physical_size
            self.program['texture'][...] = (255 * self.stimulus(t)).astype(np.uint8)
            self.program.draw('triangle_strip')
        else:
            self.close()

    def on_timer(self, event):
        self.update()

if __name__ == '__main__':

    def checkerboard(t, freq=8., grid_num=8, grid_size=4):
        row_even = grid_num // 2 * [0, 1]
        row_odd = grid_num // 2 * [1, 0]
        Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
        grid = Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)
        polarity = np.sign(np.sin(2*np.pi*t*freq))
        return ((2*grid-1)*polarity +1) /2

    fps, T = 100, 10
    screen = Canvas(checkerboard, timeline=np.linspace(0, T, T*fps))
    screen.app.run()

