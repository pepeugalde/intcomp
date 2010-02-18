import random

import settings


class World():

    def __init__(self):
        self.randomize()

    def update(self):
        pass

    def expose(self, cr):
        pass

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
