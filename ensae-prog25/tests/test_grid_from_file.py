# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys
sys.path.append("code/")

import unittest 
import numpy as np
from grid import Grid # type: ignore
from solver import SolverGreedy # type: ignore
from solver import Solver_matchmax_1 # type: ignore
from solver import Solver_Ford_Fulkerson # type: ignore
from solver import Optimal_Solver # type: ignore
from graph import * # type: ignore
import time


class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

 
class Test_is_forbidden(unittest.TestCase):
    def test_grid1(self): 
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.is_forbidden(0,1), True)

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        self.assertEqual(grid.is_forbidden(0,1), True)

    def test_grid12(self):
        grid = Grid.grid_from_file("input/grid12.in",read_values=True)
        self.assertEqual(grid.is_forbidden(1,0), True)

class Test_cost(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.cost(((0,0),(0,1))), 3)
        self.assertEqual(grid.cost(((0,0),(1,0))), 6)

    def test_grid5(self):
        grid = Grid.grid_from_file("input/grid05.in",read_values=True)
        self.assertEqual(grid.cost(((0,0),(1,0))), 4)

class Test_valid_neighbors(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.valid_neighbors(1,2),[(0,2),(1,1)])

    def test_grid5(self):
        grid = Grid.grid_from_file("input/grid05.in",read_values=True)
        self.assertEqual(grid.valid_neighbors(1,5),[(0,5),(1,4),(2,5)])

class Test_all_pairs(unittest.TestCase):
    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.all_pairs(),[ ((0,0),(1,0)) , ((0,2),(1,2)) , ((1,1),(1,0)) , ((1,1),(1,2)) ])

    def test_grid3(self): 
        grid = Grid.grid_from_file("input/grid03.in",read_values=True)
        self.assertEqual(len(grid.all_pairs()), 18)

    def test_grid5(self):
        grid = Grid.grid_from_file("input/grid05.in",read_values=True)
        self.assertEqual(len(grid.all_pairs()), 22)

class Test_grid_plot(unittest.TestCase):
    def test_grid17(self):
        grid = Grid.grid_from_file("input/grid17.in",read_values=True)
        
        #grid.plot()

class Test_SolverGreedy(unittest.TestCase):
    def test_grid1(self):
# on vérifie pour cette première résolution, le score de grid1 est 8
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        #Test temps
        T1  = time.perf_counter()
        solver = SolverGreedy(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(),8)
        print("temps solverGreedy grid1 :", T2-T1)

        #grid.plot(solver.pairs)


    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = SolverGreedy(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(),1)
        print("temps solverGreedy grid2 :", T2-T1)

        #grid.plot(solver.pairs)

    def test_grid3(self):
        grid = Grid.grid_from_file("input/grid03.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = SolverGreedy(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(),2)
        print("temps solverGreedy grid3 :", T2-T1)

        #grid.plot(solver.pairs)

    def test_grid5(self): 
        grid = Grid.grid_from_file("input/grid05.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = SolverGreedy(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(),57)
        print("temps solverGreedy grid5 :", T2-T1)

        #grid.plot(solver.pairs)

class Test_Solver_matchmax_1(unittest.TestCase):
    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = Solver_matchmax_1(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(), 1) # on en déduit que le score est de 1
        print("temps solver matchmax1 grid2 :", T2-T1)

        #grid.plot(solver.pairs)

    def test_grid3(self):
        grid = Grid.grid_from_file("input/grid03.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = Solver_matchmax_1(grid)
        solver.run()
        T2 = time.perf_counter()
        self.assertEqual(solver.score(), 2) #on en déduit que le score est de 2 car il y a 18 cases blanches, et le reste est noir
        print("temps solver matchmax1 grid3 :", T2-T1)

        #grid.plot(solver.pairs)

    def test_grid04(self):
        grid = Grid.grid_from_file("input/grid04.in",read_values=True)
        # Test Temps
        T1  = time.perf_counter()
        solver = Solver_matchmax_1(grid)
        solver.run()
        T2 = time.perf_counter()
        print("temps solver matchmax1 grid4 :", T2-T1)

        #grid.plot(solver.pairs) #on représente visuellement les paires choisies
        
    def test_grid11(self):#Trop de récursivité pour nos ordinateurs
        grid = Grid.grid_from_file("input/grid11.in",read_values=True)
        # Test Temps
        #T1  = time.perf_counter()
        #solver = Solver_matchmax_1(grid)
        #solver.run()
        #T2 = time.perf_counter()
        #print("temps solver matchmax1 grid11 :", T2-T1)

        #grid.plot(solver.pairs) #on représente visuellement les paires choisies

class Test_Solver_Ford_Fulkerson(unittest.TestCase):#Autre solver de match maxing
        def test_grid11(self):
            grid = Grid.grid_from_file("input/grid11.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Solver_Ford_Fulkerson(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps solver Ford Fulkerson grid11 :", T2-T1)
            
            #grid.plot(solver.pairs)
        
        def test_grid14(self):
            grid = Grid.grid_from_file("input/grid14.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Solver_Ford_Fulkerson(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps solver Ford Fulkerson grid14 :", T2-T1)
            
            #grid.plot(solver.pairs)
        
        def test_grid16(self):
            grid = Grid.grid_from_file("input/grid16.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Solver_Ford_Fulkerson(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps solver Ford Fulkerson grid16 :", T2-T1)
            
            #grid.plot(solver.pairs)

        def test_grid21(self):
            grid = Grid.grid_from_file("input/grid21.in",read_values=True)
            # # Test Temps
            # T1  = time.perf_counter()
            # solver = Solver_Ford_Fulkerson(grid)
            # solver.run()
            # T2 = time.perf_counter()
            # print("temps solver Ford Fulkerson grid21 :", T2-T1)
            
            #grid.plot(solver.pairs)


class Test_Optimal_Solver(unittest.TestCase):#Solver dans le cas général (Ford Fulkerson)
        def test_grid5(self):
            grid = Grid.grid_from_file("input/grid05.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Optimal_Solver(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps optimal solver grid5 :", T2-T1)

            print("Score optimal solver gird5 :", solver.score())
            
            #grid.plot(solver.pairs)
        
        def test_grid12(self):
            grid = Grid.grid_from_file("input/grid12.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Optimal_Solver(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps optimal solver grid12 :", T2-T1)

            print("Score optimal solver gird12 :", solver.score())
            
            #grid.plot(solver.pairs)
        
        def test_grid18(self):
            grid = Grid.grid_from_file("input/grid18.in",read_values=True)
            # Test Temps
            T1  = time.perf_counter()
            solver = Optimal_Solver(grid)
            solver.run()
            T2 = time.perf_counter()
            print("temps optimal solver grid18 :", T2-T1)

            print("Score optimal solver gird18 :", solver.score())
            
            #grid.plot(solver.pairs)           

        def test_grid23(self):
            grid = Grid.grid_from_file("input/grid23.in",read_values=True)
            # # Test Temps
            # T1  = time.perf_counter()
            # solver = Optimal_Solver(grid)
            # solver.run()
            # T2 = time.perf_counter()
            # print("temps optimal solver grid23 :", T2-T1)

            # print("Score optimal solver grid23 :", solver.score())
            
            #grid.plot(solver.pairs)

if __name__ == '__main__':
    unittest.main()

