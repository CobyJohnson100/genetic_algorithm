# genetic_algorithm/genetic_algorithm.py
import os
import time
import datetime
import traceback
from numpy.random import randint, rand

import util

script_name = os.path.splitext(os.path.basename(__file__))[0]
logger = util.setup_logging(script_name)

def selection(population, scores, k=3):
    # first random selection
    selection_index = randint(len(population))
    for index in randint(0, len(population), k-1):
        # check if better (e.g. perform a tournament)
        if scores[index] < scores[selection_index]:
            selection_index = index
    return population[selection_index]

# crossover two parents to create two children
def crossover(parent1, parent2, r_crossover):
    # children are copies of parents by default
    child1, child2 = parent1.copy(), parent2.copy()
    # check for recombination
    if rand() < r_crossover:
        # select crossover point that is not on the end of the string
        crossover_point = randint(1, len(parent1)-2)
    # perform crossover
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return [child1, child2]

def mutation(bitstring, r_mutation):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mutation:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

def genetic_algorithm(objective, n_bits, n_iteration, n_population, r_crossover, r_mutation):
    try:
        logger.info(f"Initializing genetic_algorithm("
                    f"n_bits={n_bits}, "
                    f"n_iteration={n_iteration}, "
                    f"n_population={n_population}, "
                    f"r_crossover={r_crossover}, "
                    f"r_mutation={r_mutation})"
                    " ...")
        
        # initialize population of random bitstring
        # generate list of size n_population where each element is list of size n_bits where each element is 0 or 1
        population = [randint(0, 2, n_bits).tolist() for _ in range(n_population)]
        if len(population) > 1:
            logger.info(f"population (random bitstring)\n[{population[0]}, {population[1]}, ...]")
        else:
            logger.info(f"population\n{population}")
        
        best, best_evaluation = 0, objective(population[0])
        logger.info(f"Initialized best={best} and best_evaluation={best_evaluation}")
        
        for generation in range(n_iteration):
            # evaluate all candidates in the population
            scores = [objective(population_sample) for population_sample in population]
            # logger.info(f"generation={generation}, scores\n{scores}")
            
            for i in range(n_population):
                if scores[i] < best_evaluation: # "<" because minimizing 
                    best, best_evaluation = population[i], scores[i]
                    logger.info(">%d, new best f(%s) = %.3f" % (generation, population[i], scores[i]))
            
            # select parents
            selected = [selection(population, scores) for _ in range(n_population)]
            # create the next generation
            children = list()
            for i in range(0, n_population, 2):
                # get selected parents in pairs
                parent1, parent2 = selected[i], selected[i+1]
                # crossover and mutation
                for child in crossover(parent1, parent2, r_crossover):
                    # mutation
                    mutation(child, r_mutation)
                    # store for next generation
                    children.append(child)
            # replace population
            population = children
        return [best, best_evaluation]
    except:
        logger.error(f"An error occured:\n{traceback.print_exc()}")

if __name__ == "__main__":
    logger.info("Run directly")
    start_time = time.time()
    genetic_algorithm()
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_readable = str(datetime.timedelta(seconds=execution_time))
else:
    logger.info("Imported")