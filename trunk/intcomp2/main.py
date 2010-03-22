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
next = False
continuous = False
trajectories = False
restart = False

def display():
    global xrot, yrot, p, trajectories

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glMatrixMode(GL_MODELVIEW)

    glPushMatrix()

    glRotated(xrot, 1.0, 0.0, 0.0)
    glRotated(yrot, 0.0, 1.0, 0.0)

    p.display(trajectories)

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

def key_cb (key, x, y):
    global next, continuous, trajectories, restart
    global zoom, ZOOM_RATE
    if key == 'n' or key == 'N':
        next = True
    elif key == 'c' or key == 'C':
        continuous = not continuous
    elif key == 'v' or key == 'V':
        trajectories = not trajectories
    elif key == 'b' or key == 'B':
        restart = True
    elif key == '-':
        zoom += ZOOM_RATE
    elif key == '+':
        zoom -= ZOOM_RATE

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
    global zoom, depth, p, next, continuous, restart

    if zoom:
        depth += zoom
        zoom = 0.0
        set_camera()

    if restart:
        p.setup()
        print '\nWorld data:\n{0}'.format(p)
        restart = False
        next = False
    elif next or continuous:
        p.step()
        next = False

    glutPostRedisplay()
    glutTimerFunc(INTERVAL, update, 0)

def init(): 
    global p
    glClearColor(0.62, 0.62, 0.62, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    p = projectile.ProjectileEvaluator()
    print 'World data:\n{0}'.format(p)

if __name__ == '__main__':
    import sys

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("GENETIC ALGORITHM")

    init()

    glutKeyboardFunc(key_cb)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutTimerFunc(INTERVAL, update, 0)

    glutMainLoop()
