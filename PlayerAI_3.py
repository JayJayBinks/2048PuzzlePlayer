import math
import sys
import time


from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):
    # for pruning
    alpha = -math.inf
    beta = math.inf

    children_to_check = list()
    moves_to_check = list()

    maximize_counter = 0
    minimize_counter = 0

    # Time Limit Before Losing
    time_limit = 0.2
    conservative_minus = 0.005

    prev_time_move = None

    # increasing limit to not fail execution
    sys.setrecursionlimit(0x100000)

    def getMove(self, grid):
        return PlayerAI.minimax(grid)

    @staticmethod
    def minimax(grid):
        best_move = None
        best_utility = -math.inf

        PlayerAI.moves_to_check = grid.getAvailableMoves()
        for move in PlayerAI.moves_to_check:
            PlayerAI.prev_time_move = time.clock()
            new_grid = grid.clone()
            new_grid.move(move)

            # print("maximize grid")
            # for i in new_grid.map:
            #     print(i)
            PlayerAI.children_to_check = PlayerAI.generate_children_minimize(new_grid)
            for child in PlayerAI.children_to_check:
                # print("check child minimax")
                # for i in child.map:
                #     print(i)
                max_child, max_utility = PlayerAI.maximize(child)
                # print("util:" , max_utility)
                if max_utility > best_utility:
                    best_move = move
                    best_utility = max_utility
        return best_move

    @staticmethod
    def maximize(grid):
        PlayerAI.maximize_counter += 1
        if PlayerAI.check_timelimit_exceeded() or not grid.canMove():
            return None, PlayerAI.eval_util(grid)

        max_child = None
        max_utility = -math.inf

        child_ctr = 0
        for child in PlayerAI.generate_children_maximize(grid):

            # print("check max child" , child_ctr, "from max", PlayerAI.maximize_counter)
            # for i in child.map:
            #     print(i)
            min_child, utility = PlayerAI.minimize(child)

            if utility > max_utility:
                max_child, max_utility = child, utility

            child_ctr += 1

            if max_utility >= PlayerAI.beta:
                #print("prune", child_ctr, "from max ", PlayerAI.maximize_counter)
                break

            if max_utility > PlayerAI.alpha:
                PlayerAI.alpha = max_utility

        return max_child, max_utility

    @staticmethod
    def minimize(grid):
        PlayerAI.minimize_counter += 1
        if PlayerAI.check_timelimit_exceeded() or not grid.canMove():
            return None, PlayerAI.eval_util(grid)

        min_child = None
        min_utility = math.inf

        child_ctr = 0
        for child in PlayerAI.generate_children_minimize(grid):

            # print("check min child", child_ctr , "from min", PlayerAI.minimize_counter)
            # for i in child.map:
            #     print(i)
            max_child, utility = PlayerAI.maximize(child)

            if utility < min_utility:
                min_child, min_utility = child, utility
            child_ctr += 1

            if min_utility <= PlayerAI.alpha:
                #print("prune", child_ctr, "from min", PlayerAI.minimize_counter)
                break

            if min_utility < PlayerAI.beta:
                PlayerAI.beta = min_utility
        return min_child, min_utility

    @staticmethod
    def generate_children_maximize(grid):
       children = list()
       for move in grid.getAvailableMoves():
           new_grid = grid.clone()
           new_grid.move(move)
           children.append(new_grid)

       return children

    @staticmethod
    def generate_children_minimize(grid):
        children = list()
        for cell in grid.getAvailableCells():
            new_grid = grid.clone()
            new_grid.setCellValue(cell, 2)
            children.append(new_grid)
            new_grid = grid.clone()
            new_grid.setCellValue(cell, 4)
            children.append(new_grid)

        return children

    @staticmethod
    def eval_util(grid):
        weight1 = 1
        # weight2 = 0.3
        # as little tiles on the board as possible
        util = len(grid.getAvailableCells()) * weight1
        # will two tiles be next to each other after moving?,
        # TODO this is too time consuming turning off atm
        # util += PlayerAI.get_adjacent_tile_values(grid) * weight2

        return util

    @staticmethod
    def get_adjacent_tile_values(grid):
        util = 0
        for x in range(grid.size):
            for y in range(grid.size):
                value = grid.map[x][y]
                if value != 0:
                    util += PlayerAI.eval_neighbours(grid, (x, y), value)
        return util

    @staticmethod
    def eval_neighbours(grid, pos, value):
        util = 0

        neighbours = list()
        neighbours.append([pos[0] - 1, pos[1]])  # up
        neighbours.append([pos[0] + 1, pos[1]])  # down
        neighbours.append([pos[0], pos[1] - 1])  # left
        neighbours.append([pos[0], pos[1] + 1])  # right
        for neighbour in neighbours:
            if grid.getCellValue(neighbour) == value:
                util += 1
        return util

    @staticmethod
    def check_timelimit_exceeded():
        curr_time = time.clock()

        valid_time = PlayerAI.time_limit / len(PlayerAI.moves_to_check) - PlayerAI.conservative_minus
        # print("time", curr_time - PlayerAI.prev_time_move, "valid time", valid_time)
        # give every move equal time to evaluate further states
        if curr_time - PlayerAI.prev_time_move > valid_time:
            # print("time exceeded")
            return True
        else:
            return False
