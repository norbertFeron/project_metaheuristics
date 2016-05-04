import logging
from tools.enumGraphe import validate_solution

log = logging.getLogger(__name__)

def tabusearch(init_function,move_operator,objective_function,max_evaluations,delta_max, mu):

    tabuList = []
    best=init_function()
    best_score=objective_function(best, mu)
    tabuList.append(best)

    num_evaluations=1

    log.debug('tabusearch started: score=%f' % best_score)

    while num_evaluations < max_evaluations:
        # examine moves around current position
        move_made=False
        for next in validate_solution(move_operator(best), delta_max):
            if num_evaluations >= max_evaluations:
                break
            next_score = objective_function(next, mu)
            if next not in tabuList and next_score < best_score:
                # see if this move is better than the current
                num_evaluations+=1
                best=next
                best_score=next_score
                move_made=True
                tabuList.append(best)
                break
        if not move_made:
            break # couldn't find a better move
    log.debug('tabusearch finished: num_evaluations=%d , best_score=%d' % (num_evaluations, best_score))
    return (num_evaluations,best_score,best)