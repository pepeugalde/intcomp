# These are the settings of the project, import this file as
# import settings

import os
import cairo

# Simulation window settings.
SW_WIDTH = 640
SW_HEIGHT = 540
INTERVAL = 150

# Display widget settings.
DW_WIDTH = 640
DW_HEIGHT = 480

# Object data.
MIN_MASS = 100
MAX_MASS = 200
OBJ_WIDTH = 24
OBJ_HEIGHT = 24

# Simulated Annealing
SEG = 1
STEPS = 300
MAX_DISP_X = (0.75 * DW_WIDTH) / float(STEPS * SEG)
MAX_DISP_Y = (0.75 * DW_HEIGHT) / float(STEPS * SEG)
MIN_FORCE = 0
MAX_FORCE = (MAX_MASS  * MAX_DISP_X) / (SEG * SEG)

# World data.
MAX_WIND_FORCE = MAX_FORCE
MIN_WIN_SIZE = 5
MAX_WIN_SIZE = 150

# Images.
RES_DIR = os.path.join(os.path.dirname(__file__), 
                       'resources/').replace('\\', '/')
IMG_BG = cairo.ImageSurface.create_from_png(RES_DIR + 'bg.png')
IMG_OBJ = cairo.ImageSurface.create_from_png(RES_DIR + 'objective.png')
IMG_OBJ_XOFF = 250
IMG_OBJ_YOFF = 250
IMG_BLK = cairo.ImageSurface.create_from_png(RES_DIR + 'block.png')
