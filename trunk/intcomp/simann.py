import math
import random

def prob(t, de):
    k = 1.380E-23
    prob = -de / t
    return prob

def simann(initsol, ofunc, rfunc, (tinit, tmin, step)):
    '''
    Simulated Annealing.
    initsol -> Initial solution.
    ofunc -> Objective function.
    rfunc -> Randomize function
    (tinit, tmin, step) -> Schedule (Init temperature, minimum and step change).
    '''
    # Initial setup.
    
    t = float(tinit)
    best_solution = initsol
    best_energy = ofunc(initsol)
    solution_history = []
    
    # Assess solution.
    solution = initsol
    e1 = ofunc(solution)
    solution_history.append((solution, e1))
    # Search.
    while t > tmin:
        # Randomly tweak.
        new_solution = rfunc(solution, tinit, t)
        # Assess new solution.
        e2 = ofunc(new_solution)
        # Record attempts.
        solution_history.append((new_solution, e2))
        # Acceptance criteria.
        de = e2 - e1
        print 'Solutions: %s -> %s, de: %s' % (e1, e2, de)
        if de <= 0 or prob(t, de) < random.random():
            solution = new_solution
            e1 = e2
            if e2 < best_energy:
                best_solution = new_solution
                best_energy = e2
        t -= step
    return (best_solution, best_energy, solution_history)


if __name__ == '__main__':
    import random
    import math

    import settings
    import aux
    import world

    w = world.World()
    print w
    ox, oy, m = w.object
    wx, wy, _, _ = w.win_area
    initsol = ((ox, oy), 
               m, 
               (wx, wy), 
               w.wind_force, 
               w.propulsors)
    print initsol

    def ofunc(x):
        '''
        Evaluate the final distance.
        '''
        ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
        prop_f = (pxp - pxn, pyp - pyn) # Composite propulsion force.
        
        forces = [prop_f, wf]
        (fx, fy) = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]), forces)
        dx = ((fx * math.pow(settings.SEG, 2)) / m) * settings.STEPS
        dy = ((fy * math.pow(settings.SEG, 2)) / m) * settings.STEPS

        return aux.distance(ox + dx, oy + dy, ox, oy)

    def rfunc(x, tinit, t):
        '''
        Randomize the propulsion force.
        '''
        ((ox, oy), m, (wx, wy), wf, (pxn, pxp, pyn, pyp)) = x
        ratio = (t / tinit)
        return ((ox, oy), 
                m, 
                (wx, wy), 
                wf, 
                (random.uniform(settings.MIN_FORCE, 
                                settings.MAX_FORCE), 
                 random.uniform(settings.MIN_FORCE, 
                                settings.MAX_FORCE), 
                 random.uniform(settings.MIN_FORCE, 
                                settings.MAX_FORCE), 
                 random.uniform(settings.MIN_FORCE, 
                                settings.MAX_FORCE)))

    sched = (100, 0.0, 0.001)
    (bs, be, h) = simann(initsol, ofunc, rfunc, sched)
    print be
