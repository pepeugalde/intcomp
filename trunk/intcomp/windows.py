import sys

import gtk
import random
import cairo
import gobject

import settings
import world

class DisplayWidget(gtk.DrawingArea):

    def __init__(self):
        super(DisplayWidget, self).__init__()
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 0, 0))
        self.set_size_request(settings.DW_WIDTH, settings.DW_HEIGHT)
        self.connect("expose-event", self.expose)
        self.init()

    def update(self):
        # World update.
        self.world.update()
        self.queue_draw()
        return True

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        if not self.paused:
            # Clear screen.
            cr.set_source_rgb(0, 0, 0)
            cr.paint()
            # Wolrd expose.
            self.world.expose(cr)

    def init(self):
        self.paused = False
        self.world = world.World()
        gobject.timeout_add(50, self.update)
        #glib.timeout_add(50, self.on_timer)


class SimulationWindow(gtk.Window):

    def __init__(self):
        super(SimulationWindow, self).__init__()
        
        self.set_title('SISINT')
        self.set_size_request(settings.SW_WIDTH, settings.SW_HEIGHT)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER)

        self.display_widget = DisplayWidget()
        self.add(self.display_widget)

        self.connect("key-press-event", self.on_key_down)
        self.connect("destroy", gtk.main_quit)

        self.show_all()

    def on_key_down(self, widget, event):
        print 'poop'
