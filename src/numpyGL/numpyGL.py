#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A minimal example of a routine to show a numpy array on a screen.

"""

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

class Client(app.Canvas):
    """
    The client initializes and updates the display where stimulations and
    camera take will occur.
    """
    def __init__(self, timeline):
        self.timeline = timeline
#         app.use_app('Glfw')
        app.use_app('pyglet')
        #app.Canvas.__init__(self, keys='interactive', title='welcome to numpyGL', fullscreen=True)#, size=(1280, 960))#, size=(512, 512)
        super(Client, self).__init__(fullscreen=True)
        width, height = self.physical_size
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (1, 0), (0, 1), (0, 0)]
        self.program['texture'] = np.zeros((height, width, 3)).astype(np.uint8)
        #self.program['texture'] = checkerboard()
        gloo.set_viewport(0, 0, width, height)
        self._timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.start = time.time()
        self.fullscreen = True
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

    fps, T = 100, 10
    screen = Client(timeline=np.linspace(0, T, T*fps))
    screen.app.run()

