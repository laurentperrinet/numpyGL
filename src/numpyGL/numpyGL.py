#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A simple framework to display numpy array on a screen. And only that.

Heavily based on https://github.com/vispy/vispy/blob/master/examples/tutorial/gloo/textured_quad.py
by Nicolas Rougier.

"""
from __future__ import division, print_function, absolute_import
__author__ = "Laurent Perrinet INT - CNRS"
__version__ = '0.1'
__licence__ = 'BSD licence'

import numpy as np
import time

# VISUALIZATION ROUTINES
from vispy import app
from vispy import gloo

#--------------------------------------------------------------------------

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
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
    def __init__(self, stimulus, timeline=np.linspace(0, 4, 4*30), keys='interactive', title='welcome to numpyGL'):
        self.stimulus = stimulus
        self.timeline = timeline
        app.use_app('pyglet')
        #app.Canvas.__init__(self, keys='interactive', title='welcome to numpyGL', fullscreen=True)#, size=(1280, 960))#, size=(512, 512)
        super(Canvas, self).__init__(keys=keys, title=title)
        width, height = self.physical_size
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (1, 0), (0, 1), (0, 0)]
        #self.program['texture'] = np.zeros((height, width, 3)).astype(np.uint8)
        self.program['texture'] = self.stimulus(t=0.)
        gloo.set_viewport(0, 0, width, height)
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.start = time.time()
        self.fullscreen = True
        self.show()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.set_clear_color('white')
        gloo.clear(color=True)
        t = time.time()-self.start
        if t  < self.timeline.max():
            width, height = self.physical_size
            self.program['texture'][...] = self.stimulus(t).astype(np.uint8)
            self.program.draw('triangle_strip')
        else:
            self.close()

    def on_timer(self, event):
        self.update()

if __name__ == '__main__':

    def checkerboard(t, grid_num=8, grid_size=32):
        row_even = grid_num // 2 * [0, 1]
        row_odd = grid_num // 2 * [1, 0]
        Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
        grid = Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)
        polarity = np.sign(np.sin(2*np.pi*t))
        return 255 * ((2*grid-1)*polarity +1) /2

    fps, T = 100, 10
    screen = Canvas(checkerboard, timeline=np.linspace(0, T, T*fps))
    screen.app.run()

