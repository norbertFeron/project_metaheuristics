import random
import math
import logging
from tools import enumGraphe

log = logging.getLogger(__name__)


class ObjectiveFunction:
    # struct to store best solution & score known
    # so ObjectiveFunction is a callable function and also store best sol

    def __init__(self, objective_function):
        self.objective_function = objective_function
        self.best = None
        self.best_score = None

    def __call__(self, solution, mu):
        score = self.objective_function(solution, mu)
        if self.best is None or score < self.best_score:
            self.best_score = score
            self.best = solution
            log.debug('new best score: %f' % self.best_score)
        return score


def P(prev_score, next_score, temperature):
    # probabilistically choosing a neighbour
    # @return acceptation probability
    if next_score < prev_score:
        return 1.0
    else:
        return math.exp(-abs(prev_score - next_score) / temperature)


def kirkpatrick_cooling(start_temp, alpha):
    # cooling schedule
    # get start_temp cooling by alpha=[0,1]
    T = start_temp
    while True:
        yield T
        T = alpha * T


def anneal(init_function, move_operator, objective_function, max_evaluations, start_temp, alpha, delta_max, mu):
    objective_function = ObjectiveFunction(objective_function)

    current = init_function()
    current_score = objective_function(current, mu)
    num_evaluations = 1

    cooling_schedule = kirkpatrick_cooling(start_temp, alpha)

    log.debug('anneal started: score=%f' % current_score)

    for temperature in cooling_schedule:
        done = False
        # examine moves around current position
        for next in enumGraphe.validate_solution(move_operator(current), delta_max):
            if num_evaluations >= max_evaluations:
                done = True
                break

            next_score = objective_function(next, mu)
            num_evaluations += 1

            # probabilistically accept this solution
            # always accepting better solutions
            p = P(current_score, next_score, temperature)
            if random.random() < p:
                current = next
                current_score = next_score
                break
        if done: break  # no better solution

    best_score = objective_function.best_score
    best = objective_function.best
    log.debug('final temperature: %f' % temperature)
    log.debug('anneal finished: num_evaluations=%d, best_score=%d' % (num_evaluations, best_score))
    return num_evaluations, best_score, best, temperature
