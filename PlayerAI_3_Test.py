import unittest
from PlayerAI_3 import PlayerAI
from Grid_3 import Grid

grid = Grid()
grid.map[0][0] = 2
grid.map[0][1] = 4
grid.map[1][1] = 2


class SolverTest(unittest.TestCase):

    def test_minimax(self):
        player = PlayerAI()
        print("original grid")
        for i in grid.map:
            print(i)
        print(player.getMove(grid))

if __name__ == '__main__':
    unittest.main()
