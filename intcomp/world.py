import random
import math

import settings
import aux
import world

class World():

    def __init__(self):
        self.running = False
        self.randomize()
        self.message = 'Press (Enter) to start, (R) to restart.'

    def update(self):
        if self.running:
            pass
        else:
            pass
            
        return True

    def expose(self, cr):
        cr.set_source_surface(settings.IMG_BG, 0, 0)
        cr.paint()

        cr.set_source_surface(settings.IMG_OBJ,
                              self.win_area[0] - settings.IMG_OBJ_XOFF, 
                              self.win_area[1] - settings.IMG_OBJ_YOFF)
        cr.paint()

        cr.set_source_surface(settings.IMG_BLK,
                              self.object[0] - settings.OBJ_WIDTH, 
                              self.object[1] - settings.OBJ_HEIGHT)
        cr.paint()

        cr.set_font_size(12)
        cr.set_source_rgb(65535, 65535, 65535)
        cr.move_to(12, 24)
        cr.show_text('Simulated Annealing: ' + self.message)

    def randomize(self):
        self.res = 0
        self.dest = None
        self.results = []
        # settings.DW_WIDTH / 2, settings.DW_HEIGHT / 2,
        self.object = (random.randint(0, settings.DW_WIDTH),
                       random.randint(0, settings.DW_HEIGHT),
                       random.randint(settings.MIN_MASS, settings.MAX_MASS))
        self.propulsors = (0, 0, 0, 0)
        self.wind_force = (random.uniform(-settings.MAX_WIND_FORCE, 
                                           settings.MAX_WIND_FORCE), 
                           random.uniform(-settings.MAX_WIND_FORCE, 
                                           settings.MAX_WIND_FORCE))
        self.friction = random.random()
        self.win_area = (random.randint(0, settings.DW_WIDTH),
                         random.randint(0, settings.DW_HEIGHT))

    def __str__(self):
        return ('World data:\n\tObject: %s\n\tPropulsors: %s\n\tWind: %s\n\t' + 
                'Frict: %s\n\tWin point: %s') % (self.object, 
                                                 self.propulsors, 
                                                 self.wind_force, 
                                                 self.friction, 
                                                 self.win_area)

    def simann(self):
        ox, oy, m = self.object
        wx, wy = self.win_area
        initsol = ((ox, oy), 
                   m, 
                   (wx, wy), 
                   w.wind_force, 
                   w.propulsors)
        print initsol

        def ofunc(x):
            '''
            Evaluate the final distance.
            '''
            ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
            prop_f = (pxp - pxn, pyp - pyn) # Composite propulsion force.
        
            forces = [prop_f, wf]
            (fx, fy) = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), forces)
            dx = ((fx * math.pow(settings.SEG, 2)) / m) * settings.STEPS
            dy = ((fy * math.pow(settings.SEG, 2)) / m) * settings.STEPS

            return aux.distance(ox + dx, oy + dy, ox, oy)

        def rfunc(x, tinit, t):
            '''
            Randomize the propulsion force.
            '''
            ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
            ratio = (t / tinit)
            return ((ox, oy), 
                    m, 
                    (wx, wy), 
                    wf, 
                    (random.uniform(settings.MIN_FORCE, 
                                    settings.MAX_FORCE), 
                     random.uniform(settings.MIN_FORCE, 
                                    settings.MAX_FORCE), 
                     random.uniform(settings.MIN_FORCE, 
                                    settings.MAX_FORCE), 
                     random.uniform(settings.MIN_FORCE, 
                                    settings.MAX_FORCE)))

        sched = (100, 0.0, 0.001)
        return simann(initsol, ofunc, rfunc, sched)


if __name__ == '__main__':
    w = World()
    print(w)
    w.randomize()
    print(w)
