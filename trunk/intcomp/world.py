import random
import settings


class World():

    def __init__(self):
        self.randomize()

    def update(self):
        pass

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

    def randomize(self):
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


if __name__ == '__main__':
    w = World()
    print(w)
    w.randomize()
    print(w)
