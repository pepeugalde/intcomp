import random
import math
import time

import settings
import calc
import world
import simann


class World():

    def __init__(self):
        self.randomize()

    def update(self):
        if self.results:
            ox, oy = self.results.pop()
            self.object = (ox, oy, self.object[2])
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
        cr.show_text('Simulated Annealing')

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

    def eval_sol(self, x):
        ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
        prop_f = (pxp - pxn, pyp - pyn) # Composite propulsion force.
        
        forces = [prop_f, wf]
        (fx, fy) = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), forces)
        return (((fx * math.pow(settings.SEG, 2)) / m) * settings.STEPS, 
               ((fy * math.pow(settings.SEG, 2)) / m) * settings.STEPS)

    def run_simann(self):
        ox, oy, m = self.object
        wx, wy = self.win_area
        initsol = ((ox, oy), 
                   m, 
                   (wx, wy), 
                   self.wind_force, 
                   self.propulsors)
        print initsol

        def ofunc(x):
            '''
            Evaluate the final distance.
            '''
            ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
            dx, dy = self.eval_sol(x)
            return calc.distance(ox + dx, oy + dy, wx, wy)

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
        return simann.simann(initsol, ofunc, rfunc, sched)

    def start_simann(self):
        (best_solution, best_energy, solution_history) = self.run_simann()
        f = open('out', 'w')
        for (t, sol, e) in solution_history + [(None, best_solution, None)]:
            ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = sol
            dx, dy = self.eval_sol(sol)
            self.results.append((ox + dx, oy + dy))
            if t and e:
                f.write('%s %s\n' % (t, e))
        tmp = random.sample(self.results, 99)
        tmp.append(self.results[-1])
        tmp.reverse()
        self.results = tmp
        print 'Best solution:\n\t%s energy: %s' % (best_solution, best_energy)
        print 'Animating...'


if __name__ == '__main__':
    w = World()
    print(w)
    w.randomize()
    print(w)
