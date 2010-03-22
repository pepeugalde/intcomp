# Genetic algorithm.

from random import randint, random
from math import pow

def init(n, l, a):
    '''
    n -> Number of initial elements.
    l -> Length of the genome.
    a -> Alphabet.
    returns: The initial population (list).
    '''
    return [[a[randint(0, len(a) - 1)] for i in range(0, l)] 
            for i in range(0, n)]

def eval_pop(p, fit):
    '''
    p -> Population (list).
    fit -> Fitness function.
    returns: List of tuples as (individual, Fitness, Pselect, ExpCount).
    '''
    p1 = [(i, float(fit(i))) for i in p]
    sumf = sum([f for (i, f) in p1])
    return [(i, f, f / sumf) for (i, f) in p1]

def print_table(evalt):
    '''
    evalt -> List of tuples returned by eval_pop.
    '''
    for e, f, ps in evalt:
        print '%s f:%f ps:%f' % (''.join(e), f, ps)

def get_top(evalt):
    '''
    Selects the individual with the top fitness as a tuple (indiv, fitness).
    '''
    max = 0
    tope = []
    topf = 0
    for e, f, ps in evalt:
        if f >= topf:
            tope = e
            topf = f
    return (tope, topf)

def reproduce(evalt, npop):
    pop = []
    prev = 0.0
    slices = []
    for e, f, ps in evalt:
        slices.append((e, prev, prev + ps))
        prev += ps
    for i in range(0, npop):
        rp = random()
        for e, low, top in slices:
            if rp >= low and rp < top:
                pop.append(e)
                break
    return pop

def mutate(e, alph):
    for i in range(0, len(e)):
        e[i] = alph[randint(0, len(alph) - 1)] if random() <= 0.01 else e[i]
    return e

def sex(a, b, genelen, alph):
    m = randint(0, genelen)
    return [mutate(a[: m] + b[m :], alph), mutate(b[: m] + a[m :], alph)]

def crossover(pop, genelen, alph):
    npop = []
    for i in range(0, len(pop), 2):
        npop += sex(pop[i], pop[i + 1], genelen, alph)
    return npop

def genea(alphabet, 
          fitnessfunc,
          genelen,
          startpop = 10):
    population = init(startpop, genelen, alphabet)
    evalt = eval_pop(population, fitnessfunc)

    def next_func(e):
        '''
        This function evaluates the current evaluation table to generate and
        evaluate a new population.
        '''
        p = crossover(reproduce(e, startpop), genelen, alphabet)
        return eval_pop(p, fitnessfunc)

    return (evalt, 
            next_func)
