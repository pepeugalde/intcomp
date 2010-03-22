try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''

import projectile


# ----- CONSTANTS -----
INTERVAL = 16
WIDTH = 640
HEIGHT = 480
DEPTH = 450
ZOOM_RATE = 3.0

# ----- VARIABLES -----
depth = DEPTH
zoom = 0.0;

mouseDown = False
xrot = 0.0
yrot = 0.0
xdiff = 0.0
ydiff = 0.0

p = None


def display ():
    global xrot, yrot, p

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_MODELVIEW)

    glPushMatrix()

    glRotated(xrot, 1.0, 0.0, 0.0)
    glRotated(yrot, 0.0, 1.0, 0.0)

    p.display()

    glPopMatrix()

    glFlush()
    glutSwapBuffers()

def set_camera():
    global depth

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, depth, 0, 0, 0, 0, 1, 0)

def resize(w, h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, w, h)
    gluPerspective(30.0, (1.0 * w) / h, 1.0, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    set_camera()

def mouse(button, state, x, y):
    global mouseDown, xrot, yrot, xdiff, ydiff

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouseDown = True
            xdiff = x - yrot
            ydiff = -y + xrot
        else:
            mouseDown = False

def mouse_motion(x, y):
    global mouseDown, xrot, yrot, xdiff, ydiff

    if mouseDown:
        yrot = (x - xdiff)
        xrot = (y + ydiff)

def update(value):
    global zoom, depth

    if zoom:
        depth += zoom
        zoom = 0.0
        set_camera()

    glutPostRedisplay()
    glutTimerFunc(INTERVAL, update, 0)

def init(): 
    global p
    glClearColor(0.62, 0.62, 0.62, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    p = projectile.ProjectileEvaluator()

if __name__ == '__main__':
    import sys

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("TEMPLATE")

    init()

    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(INTERVAL, update, 0)

    glutMainLoop()
