# genetic_algorithm\onemax.py
import os
import time
import datetime
import traceback

from genetic_algorithm import genetic_algorithm

import util

script_name = os.path.splitext(os.path.basename(__file__))[0]
logger = util.setup_logging(script_name)

def onemax_objective_function(x):
    return -sum(x) # negative because genetic algorithm is minimizing the objective function

def onemax():
    try:
        n_iteration = 100
        n_bits = 20
        n_population = 100
        r_cross = 0.9
        r_mutation_rate = 1.0 / float(n_bits)

        best, score = genetic_algorithm(
            onemax_objective_function,
            n_bits,
            n_iteration,
            n_population,
            r_cross,
            r_mutation_rate
            )
        logger.info(f"genetic_algorithm:\nbest={best}\nscore={score}")
    except:
        logger.error(f"An error occured:\n{traceback.print_exc()}")

if __name__ == "__main__":
    logger.info("Run directly")
    start_time = time.time()
    onemax()
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_readable = str(datetime.timedelta(seconds=execution_time))
else:
    logger.info("Imported")