#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A simple framework to display numpy array on a screen. And only that.

Heavily based on https://github.com/vispy/vispy/blob/master/examples/tutorial/gloo/textured_quad.py
by Nicolas Rougier and more example scripts from the vispy documentation.

"""
from __future__ import division, print_function, absolute_import
__author__ = "Laurent Perrinet INT - CNRS"
__version__ = '0.1'
__licence__ = 'BSD licence'

import numpy as np
import time
import pyglet

from vispy import app
from vispy import gloo, keys
from vispy import visuals
from vispy.visuals.transforms import STTransform
#--------------------------------------------------------------------------
class Canvas(app.Canvas):
    """
    The client initializes and updates the display where stimulations and
    camera take will occur.

    Parameters
    ----------

    cmap : str | ColorMap
        Colormap to use for luminance images.
    clim : str | tuple
        Limits to use for the colormap. Can be 'auto' to auto-set bounds to
        the min and max of the data.
    interpolation : str
        Selects method of image interpolation. Makes use of the two Texture2D
        interpolation methods and the available interpolation methods defined
        in vispy/gloo/glsl/misc/spatial_filters.frag
            * 'nearest': Default, uses 'nearest' with Texture2D interpolation.
            * 'bilinear': uses 'linear' with Texture2D interpolation.
            * 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'bicubic',
                'catrom', 'mitchell', 'spline16', 'spline36', 'gaussian',
                'bessel', 'sinc', 'lanczos', 'blackman'

    """
    def __init__(self, stimulus,
            fullscreen=True, interpolation='nearest', #'linear',
            vsync=True, #False,
            cmap='grays',
            W=1920, H=1200, # screen's size # TODO : retrieve automatically
            clim=(0, 1),
            T_max=4., fps=30,
            keys='interactive', title='welcome to numpyGL'):
        self.stimulus = stimulus
        self.T_max = T_max
#         self.fps = fps
        app.use_app('pyglet')
        #print (self.physical_size)
        #H, W = self.physical_size
        super(Canvas, self).__init__(keys=keys, title=title, size = (W, H), vsync=vsync)
#                 ImageVisual data. Can be shape (M, N), (M, N, 3), or (M, N, 4).
        self.image = visuals.ImageVisual(self.stimulus(t=0.), interpolation=interpolation, method='subdivide', clim=clim, cmap=cmap)
        # scale and center image in canvas
        s_W, s_h = self.image.size
        s = H / s_h
        h = 0#.5 * H # (H - (self.image.size[0] * s))
        w = 0#.5 * W #(W - (self.image.size[1] * s))
        self.image.transform = STTransform(scale=(s, s), translate=(h, w))
        self._timer = app.Timer(1./fps, connect=self.on_timer, start=True)
        self.start = time.time() # use the timer above
        self.fullscreen = fullscreen
        self.native.set_mouse_visible(False)
        self.show()

    def on_key_press(self, event):
        if event.key == 'Tab':
            fullscreen = not self.fullscreen
            self.fullscreen = fullscreen
        if event.key is keys.SPACE:
            if self._timer.running:
                self._timer.stop()
            else:
                self._timer.start()

    def on_resize(self, event):
        # Set canvas viewport and reconfigure visual transforms to match.
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.context.set_viewport(*vp)
        self.image.transforms.configure(canvas=self, viewport=vp)

    def on_draw(self, event):
        gloo.clear(color=True, depth=True)
        self.image.draw()

    def on_timer(self, event):
        t = time.time()-self.start
        if t  < self.T_max:
            self.image.set_data(self.stimulus(t))#.astype(np.uint8))
        else:
            self.close()
        self.update()

if __name__ == '__main__':
    W, H = 160, 100

    def checkerboard(t, freq=8., grid_num=8, grid_size=4):
        row_even = grid_num // 2 * [0, 1]
        row_odd = grid_num // 2 * [1, 0]
        Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
        grid = Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)
        polarity = np.sign(np.sin(2*np.pi*t*freq))
        return ((2*grid-1)*polarity +1) /2

    def noise(t, W=W, H=H):
        # Image to be displayed
        I = np.random.uniform(0, 1, (H, W, 3)).astype(np.float32)
#         I = np.random.uniform(0, 1, (W, H)).astype(np.float32)
        return I

    #screen = Canvas(checkerboard, timeline=np.linspace(0, T, T*fps))
    screen = Canvas(noise, fps=60)
    screen.measure_fps()
    screen.app.run()
    screen.app.quit()

