import math
import time
from BaseAI_3 import BaseAI



class PlayerAI(BaseAI):
    # for pruning
    alpha = -math.inf
    beta = math.inf

    # Time Limit Before Losing
    time_limit = 0.2
    prev_time = None

    def getMove(self, grid):
        PlayerAI.prev_time = time.clock()
        return PlayerAI.minimax(grid)

    @staticmethod
    def minimax(grid):
        best_move = None
        best_utility = -math.inf
        for move in grid.getAvailableMoves():
            new_grid = grid.clone()
            new_grid.move(move)

            max_child, max_utility = PlayerAI.maximize(new_grid)
            if max_utility > best_utility:
                best_move = move
                best_utility = max_utility
        return best_move

    @staticmethod
    def maximize(grid):
        if PlayerAI.check_timelimit_exceeded() or not grid.canMove():
            return None, PlayerAI.eval_util(grid)

        max_child = None
        max_utility = -math.inf

        for child in PlayerAI.generate_children(grid):
            min_child, utility = PlayerAI.minimize(child)

            if utility > max_utility:
                max_child, max_utility = child, utility

            if max_utility >= PlayerAI.beta:
                break

            if max_utility > PlayerAI.alpha:
                PlayerAI.alpha = max_utility

        return max_child, max_utility

    @staticmethod
    def minimize(grid):
        if PlayerAI.check_timelimit_exceeded() or not grid.canMove():
            return None, PlayerAI.eval_util(grid)

        min_child = None
        min_utility = math.inf

        for child in PlayerAI.generate_children(grid):
            max_child, utility = PlayerAI.maximize(child)

            if utility < min_utility:
                min_child, min_utility = child, utility

            if min_utility <= PlayerAI.alpha:
                break

            if min_utility < PlayerAI.beta:
                PlayerAI.beta = min_utility

        return min_child, min_utility

    @staticmethod
    def generate_children(grid):
       children = list()
       for move in grid.getAvailableMoves():
           new_grid = grid.clone()
           new_grid.move(move)
           children.append(new_grid)

       return children

    @staticmethod
    def eval_util(grid):
        # as little tiles on the board as possible
        util = 0
        for values in grid.map:
            for value in values:
                if value == 0:
                    util += 1
        return util

    @staticmethod
    def check_timelimit_exceeded():
        curr_time = time.clock()
        if curr_time - PlayerAI.prev_time > PlayerAI.time_limit:
            return True
        else:
            return False
