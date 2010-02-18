import math
import random

def boltzmann_prob(t, de):
    return 0.5

def simann(initsol, ofunc, efunc, rfunc, (t, tmin, step)):
    '''
    Simulated Annealing.
    initsol -> Initial solution.
    ofunc -> Objective function.
    efunc -> Energy function.
    rfunc -> Randomize function
    (t, tmin, step) -> Schedule (Initial temperature, minimum and step change).
    '''
    solution = initsol
    while t > tmin:
        e1 = efunc(solution) # Assess solution.
        new_solution = rfunc(solution) # Randomly tweak.
        e2 = efunc(new_solution) # Assess new solution.
        # Acceptance criteria.
        de = e2 - e1
        if de <= 0:
            solution = new_solution
        else:
            if random() < boltzmann_prob(t, de):
                solution = new_solution
        t -= step
        print ('%s' % (t))
        
    return solution


if __name__ == '__main__':
    import settings

    initsol = (0, 0, 0, 0)
    ofunc = lambda x: 1
    efunc = lambda x: 1
    rfunc = lambda x: (0, 0, 0, 0)
    sched = (100, 0, 1)
    res = simann(initsol, ofunc, efunc, rfunc, sched)
    print res
    print 'poop'
