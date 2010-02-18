import random
import settings


class World():

    def __init__(self):
        self.randomize()

    def update(self):
        pass

    def expose(self, cr):
        r, g, b, a =  (0, 65535, 65535, 0.5)
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle((self.object[0] - settings.OBJ_WIDTH),
                     (self.object[1] - settings.OBJ_HEIGHT),
                     settings.OBJ_WIDTH,
                     settings.OBJ_HEIGHT)
        cr.fill()

        cr.set_source_rgba(65535, 65535, 65535, 1)
        
        r, g, b, a =  (0, 65535, 65535, 0.5)
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle((self.win_area[0] - self.win_area[2]),
                    (self.win_area[1] - self.win_area[3]),
                    self.win_area[2],
                    self.win_area[3])
        cr.fill()

        cr.set_source_rgba(65535, 65535, 65535, 1)
        


    def randomize(self):
        self.object = (settings.DW_WIDTH / 2, settings.DW_HEIGHT / 2,
                       random.randint(settings.MIN_MASS, settings.MAX_MASS))
        self.propulsors = (0, 0, 0, 0)
        self.wind_force = (random.uniform(-settings.MAX_WIND_FORCE, 
                                           settings.MAX_WIND_FORCE), 
                           random.uniform(-settings.MAX_WIND_FORCE, 
                                           settings.MAX_WIND_FORCE))
        self.friction = random.random()
        self.win_area = (random.randint(0, settings.DW_WIDTH),
                         random.randint(0, settings.DW_HEIGHT),
                         random.randint(settings.MIN_WIN_SIZE, 
                                        settings.MAX_WIN_SIZE),
                         random.randint(settings.MIN_WIN_SIZE, 
                                        settings.MAX_WIN_SIZE))

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
