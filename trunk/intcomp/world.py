import settings
import gtk
from random import *

class World():

    self.object = (x,y,mass)
    self.propulsors = (f_x_pos, f_x_neg, f_y_pos, f_y_neg)
    self.wind_force = (fx,fy)
    self.friction = 0
    self.win_area = (x,y,width,height)
    
    def randomize():
      a = random.randint(-settings.DW_WIDTH, settings.DW_WIDTH)
      b = random.randint(-settings.DW_HEIGHT, settings.DW_HEIGHT)
      return (a,b)
    
    def initObject(self):
        self.object = (settings.DW_WIDTH/2, settings.DW_HEIGHT/2,
                        random.randint(settings.MAX_MASS))
      
    def initPropulsors(self):
     self.propulsors = (0,0,0,0)
     
    def initWindForce(self):
      self.wind_force = randomize()
     
    def initFriction(self):
      self.friction = random()
    
    def initWinArea(self):
      win_rect = gtk.gdk.Rectangle = (randomize(),randomize())
      self.win_area = win_rect
    
     
      

    def __init__(self):
        initObject(self)
        initPropulsors(self)
        initWindForce(self)
        initFriction(self)
        initWinArea(self)
        pass

    def update(self):
        pass

    def expose(self, cr):
        pass
