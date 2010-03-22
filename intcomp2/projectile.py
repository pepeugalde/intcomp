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

    def __init__(self):
        self.distance = random.randint(100, 150)
        self.gravity = random.uniform(5.0, 15.0)
        self.ty = random.randint(25, 100)
        self.population = 36
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
            td = t * 2 / 10.0
            pts = [(vox * i * td, f(i * td)) for i in range(1, 10)]
            self.tank_list.append((ang_rad * (180.0 / math.pi), 
                                   pts, 
                                   e[0] == top[0]))

    def step(self):
        self.evalt = self.next_func(self.evalt)

    def display(self):
        def display_area():
            glPushMatrix()

            glTranslated(0.0, -5.0, 0.0)
            glColor4d (1.0, 1.0, 0.0, 1.0)
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
            glScaled(1.0, 2.0, 1.0)
            glColor4d(1.0, 1.0, 1.0, t)
            glutSolidCube(5.0)
            glTranslated(0.0, -5.0, 0.0)
            glColor4d(1.0, 0.0, 0.0, t)
            glutSolidCube(5.0)
            glTranslated(0.0, -5.0, 0.0)
            glColor4d(1.0, 1.0, 1.0, t)
            glutSolidCube(5.0)
            glPopMatrix()

        def display_tank(ang):
            glColor4d (0.0, 1.0, 0.0, 1.0)
            glutSolidSphere(5.0, 20, 20)
            glPushMatrix()
            glRotated(ang, 1, 0, 0)
            glTranslated(0.0, 0.0, -10.0)
            glScaled(1.0, 1.0, 10.0)
            glutSolidCube(2.0)
            glPopMatrix()

        def display_lines(pts, top):
            pass

        display_area()
        display_target()

        
        rot = 0.0
        for ang, pts, t in self.tank_list:
            glPushMatrix()
            glRotated(rot, 0, 1, 0)
            glTranslated(0.0, 0.0, self.distance)
            display_tank(ang)
            display_lines(pts, t)
            rot += 360.0 / self.population
            glPopMatrix()


if __name__ == '__main__':
    p = ProjectileEvaluator()
    print 'Distance: {0}\nG: {1}\nTy: {2}'.format(p.distance, 
                                                  p.gravity, 
                                                  p.ty)

    while True:
        for e in p.evalt:
            ang_rad, vox, voy, t, f = p.evaluate_individual(e[0])
            error = abs(p.ty - f(t))
            print '[{0}] error: {1}'.format(''.join(e[0]), error)
        print '\n-------------------------\n'
        p.step()
