from grid import Grid
from interface import interface_jeu_solo
from solver import *
import time

import sys
sys.path.append("code/")

#Utilisation de l'interface de jeu : faire compiler ce document

algo = interface_jeu_solo(Optimal_Solver)
algo.run()