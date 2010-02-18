import math
import random

def prob(t, de):
    k = 1.380E-23
    prob = math.exp(-de / t)
    #print 'prob: %4f' % (prob)
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
    e1 = best_energy
    solution_history.append((t, solution, e1))
    # Search.
    while t > tmin:
        # Randomly tweak.
        new_solution = rfunc(solution, tinit, t)
        # Assess new solution.
        e2 = ofunc(new_solution)
        # Acceptance criteria.
        de = e2 - e1
        print 'Solutions: %4f -> %4f, de: %4f' % (e1, e2, de)
        p = prob(t, de) > random.random()
        if de <= 0 or p:
            # Record attempts.
            solution_history.append((t, new_solution, e2))
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
    wx, wy = w.win_area
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
        dx, dy = w.eval_sol(x)
        return aux.distance(ox + dx, oy + dy, wx, wy)

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
