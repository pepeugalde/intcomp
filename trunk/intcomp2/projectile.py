import random
import math

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '''
ERROR: PyOpenGL not installed properly.  
        '''

from genea import genea, get_top


class ProjectileEvaluator:

    def __init__(self, population = 36):
        self.setup(population)

    def setup(self, p = 36):
        self.distance = random.uniform(25.0, 175.0)
        self.gravity = random.uniform(5.0, 400.0)
        self.ty = random.uniform(10.0, 200.0)
        self.population = p
        self.init_genea()

    def evaluate_individual(self, x):
        def decimal_bin(x):
            return sum([int(n) * math.pow(2, -i) for i, n in enumerate(x)])

        # Angle.
        angle = int(''.join(x[0:8]), 2) % 90
        angle += decimal_bin(x[8:16])
        ang_rad = angle * (math.pi / 180.0)
        # Velocity.
        vo = int(''.join(x[16:24]), 2)
        vo += decimal_bin(x[24:])
        vo = 1 if not vo else vo
        vox = vo * math.cos(ang_rad)
        voy = vo * math.sin(ang_rad)
        # Time required to reach the target.
        t = self.distance / vox
        # Function used to calc the position in 'y'.
        return (ang_rad, 
                vox, voy, 
                t, 
                lambda t: (voy * t) - (0.5 * self.gravity * t * t))

    def init_genea(self):
        def decimal_bin(x):
            return sum([int(n) * math.pow(2, -i) for i, n in enumerate(x)])

        def fit(x):
            ang_rad, vox, voy, t, f = self.evaluate_individual(x)
            error = abs(self.ty - f(t))
            return math.pow(error + 1, -1)

        alphabet = ['0', '1']
        genelen = 32

        self.evalt, self.next_func = genea(alphabet, 
                                           fit, 
                                           genelen, 
                                           self.population)
        self.get_data(self.evalt)


    def get_data(self, evalt):
        self.tank_list = []
        top = get_top(self.evalt)
        for e in self.evalt:
            ang_rad, vox, voy, t, f = self.evaluate_individual(e[0])
            td = (t * 2) / 100.0
            pts = [(vox * i * td, f(i * td)) for i in range(0, 100)]
            self.tank_list.append((ang_rad * (180.0 / math.pi), 
                                   pts, 
                                   e[0] == top[0],
                                   (vox, voy)))

    def step(self):
        self.evalt = self.next_func(self.evalt)
        self.get_data(self.evalt)

    def display(self, trajectories):
        def display_area():
            glPushMatrix()

            glTranslated(0.0, -5.0, 0.0)
            glColor4d (0.25, 0.125, 0.0, 1.0)
            glBegin(GL_QUADS)
            glVertex3d(200.0, 0, -200.0)
            glVertex3d(-200.0, 0, -200.0)
            glVertex3d(-200.0, 0, 200.0)
            glVertex3d(200.0, 0, 200.0)
            glEnd()

            glPopMatrix()

        def display_target(t = 0.5):
            glPushMatrix()
            glTranslated(0.0, self.ty, 0.0)
            glColor4d (1.0, 1.0, 0.0, 1.0)
            glutSolidSphere(1.0, 20, 20)
            glPopMatrix()

        def display_tank(ang, (vx, vy)):
            glColor4d (0.0, 1.0, 1-(vy/512 + vy/512), 0.5)
            glutSolidSphere(2.0, 20, 20)
            glPushMatrix()
            glRotated(ang, 1, 0, 0)
            glTranslated(0.0, 0.0, -5.0)
            glScaled(1.0, 1.0, 5.0)
            glutSolidCube(1.0)
            glPopMatrix()

        def display_lines(pts, top):
            if top:
                glColor4d (1.0, 0.0, 0.0, 1.0)
            else:
                glColor4d (1.0, 1.0, 1.0, 0.5)
            glBegin(GL_LINE_STRIP)
            for z, y in pts:
                glVertex3d(0.0, y, -z)
            glEnd()
                

        display_area()
        display_target()

        rot = 0.0
        for ang, pts, t, vels in self.tank_list:
            glPushMatrix()
            glRotated(rot, 0, 1, 0)
            glTranslated(0.0, 0.0, self.distance)
            display_tank(ang, vels)
            if trajectories:
                display_lines(pts, t)
            #glColor4d (1.0, 0.0, 0.0, 1.0)
            #glutSolidCube(10.0)
            rot += 360.0 / self.population
            glPopMatrix()

    def __str__(self):
        return ('Distance: {0:5.2f}m\nG: {1:5.2f}m/s2\n' + 
                'Ty: {2:5.2f}m').format(self.distance, 
                                      self.gravity, 
                                      self.ty)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    import sys, math

    f = lambda x: abs(x) -1 if x % 2 else abs(x)
    p = ProjectileEvaluator(population = f(int(sys.argv[1])))
    print p, '\n'

    sumf = 0.0
    for i in range(0, abs(int(sys.argv[2]))):
        top = get_top(p.evalt)
        for e in p.evalt:
            ang_rad, vox, voy, t, f = p.evaluate_individual(e[0])
            error = abs(p.ty - f(t))
            sumf += e[1]
            print ('[{0}]{4} error: {1:5.3f} ' + 
                   'f: {2:5.3f} ps: {3:5.3f}').format(''.join(e[0]), 
                                                      error,
                                                      e[1],
                                                      e[2],
                                                      '*' if e[0] == top[0]
                                                      else ' ')
        print ('Fitness sum: {0:5.3f}\n' + 
               'Avg. fitness: {1:5.3f}').format(sumf,
                                                sumf / p.population)
        print '\n-------------------------\n'
        p.step()
