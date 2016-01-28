#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

The client side.

"""

import numpy as np
import time
import cv2

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


def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num // 2 * [0, 1]
    row_odd = grid_num // 2 * [1, 0]
    Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


class Client(app.Canvas):
    """
    The client initializes and updates the display where stimulations and
    camera take will occur.
    """
    def __init__(self, timeline):
        self.timeline = timeline
        app.use_app('pyglet')
        app.Canvas.__init__(self, size=(512, 512), keys='interactive', title='toto', fullscreen=True)#, size=(1280, 960))#
        width, height = self.physical_size
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (1, 0), (0, 1), (0, 0)]
        self.program['texture'] = np.zeros((height, width, 3)).astype(np.uint8)
        #self.program['texture'] = checkerboard()
        gloo.set_viewport(0, 0, width, height)
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.start = time.time()
        self.show()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.clear('black')
        if time.time()-self.start < self.timeline.max(): # + ret.sleep_time*2:
            width, height = self.physical_size
            image = np.random.rand(height, width, 3)*255
            self.program['texture'][...] = image.astype(np.uint8).reshape((height, width, 3))
            self.program.draw('triangle_strip')
        else:
            self.close()

    def on_timer(self, event):
        self.update()

if __name__ == '__main__':

    import cv2
    import numpy as np

    fps = 100
    screen = Client(timeline=np.linspace(0, 3., 3.*fps))
    app.run()

