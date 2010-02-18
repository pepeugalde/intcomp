import math


def get_angle(co, ca):
    return (math.atan(co/ca)*180)/math.pi


def get_direction(x2, y2, x1, y1):
    # On the axis
    if x2 == x1: # On the y axis
        if y2 >= y1: # below
            return 270
        else: # above
            return 90
    if y2 == y1: # On the x axis
        if x2 >= x1: # right
            return 0
        else: # left
            return 180
    
    # Elsewhere
    if x1 > x2 and y2 > y1:
        co = x1 - x2
        ca = y2 - y1
        angle = get_angle(co, ca)
        return 270 - angle
    elif x1 > x2 and y1 > y2:
        co = x1 - x2
        ca = y1 - y2
        angle = get_angle(co, ca)
        return 90 + angle
    elif x2 > x1 and y1 > y2:
        co = x2 - x1
        ca = y1 - y2
        angle = get_angle(co, ca)
        return 90 - angle
    else: # x2 > x1 and y2 > y1
        co = x2 - x1
        ca = y2 - y1
        angle = get_angle(co, ca)
        return 270 + angle


def get_increments(D, angle):
    dx = D * math.cos( (angle*math.pi)/180 )
    dy = D * math.sin( (angle*math.pi)/180 )
    return (dx, -1*dy)


def distance(x2, y2, x1=0, y1=0):
    x = x2 - x1
    y = y2 - y1
    return math.sqrt(math.pow(x,2) + math.pow(y,2))
