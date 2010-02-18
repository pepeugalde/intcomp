import sys

import gtk
import random
import cairo
import glib

import settings
import world

class DisplayWidget(gtk.DrawingArea):

    def __init__(self, world):
        super(DisplayWidget, self).__init__()
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.set_size_request(settings.DW_WIDTH, settings.DW_HEIGHT)
        self.connect("expose-event", self.expose)
        self.world = world

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        # Clear screen.
        cr.set_source_rgb(0, 0, 0)
        cr.paint()
        # Wolrd expose.
        self.world.expose(cr)


class SimulationWindow(gtk.Window):

    def __init__(self):
        super(SimulationWindow, self).__init__()
        
        self.set_title('SISINT - Simulated Annealing')
        self.set_size_request(settings.SW_WIDTH, settings.SW_HEIGHT)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER)

        self.w = world.World()
        self.display_widget = DisplayWidget(self.w)
        self.add(self.display_widget)

        self.connect("key-press-event", self.on_key_down)
        self.connect("destroy", gtk.main_quit)
        glib.timeout_add(settings.INTERVAL, self.update)

        self.show_all()

    def update(self):
        self.w.update()
        self.display_widget.queue_draw()

        return True # Needed for glib.timeout_add

    def on_key_down(self, widget, event):
        self.w.randomize()
