from graph import *

class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Given a list of pairs (self.pairs), this function returns the total score of the grid

        """

        sco=0

        visited = [[False for j in range(self.grid.m)] for i in range(self.grid.n)]# Pour savoir quelles cases on a déjà visité

        for cell1, cell2 in self.pairs : 
            visited[cell1[0]][cell1[1]]=True
            visited[cell2[0]][cell2[1]]=True
            sco+=self.grid.cost((cell1,cell2))#Ajout du score des paires

        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if not visited[i][j] and not self.grid.is_forbidden(i,j):
                    sco+= self.grid.value[i][j]# Ajout du score des cases seules

        return sco
    

class SolverGreedy(Solver) :

    def run(self):
        self.pairs = self.grid.all_pairs(all_duo=False)

class SolverEmpty(Solver):
    def run(self):
        pass

class Cell: #Création d'un class pour la méthode matching maximal
    def __init__(self, name, neighbors): 
        self.name=name # name := coordonnées de la case
        self.neighbors=neighbors #Les voisins valides par rapport à la couleurs de la case (i,j)


class Solver_matchmax_1(Solver):#Methode matching maximal

    def run(self):

        def argument(cell,visited=None):

            if visited == None:
                visited=set()

            visited.add(cell)

            for neigh in cell.neighbors : # On regarde chaque voisin possible de cell

                if neigh not in self.match : #si le voisin n'est pas couplé, on le couple avec cell
                    self.match[neigh]=cell #on ajoute neigh dans le dictionnaire des couples avec cell comme partenaire
                    return True #cell a été couplée 
                
                if self.match[neigh] not in visited and argument(self.match[neigh]): #fonction récursive si neigh, le voisin de cell est déjà couplé. self.argument(cell) = True. On essaye de trouver un nouveau couplage pour cell avec un autre voisin. 
                    self.match[neigh]=cell
                    return True 
                
            return False #si aucun couplage n'est possible pour cell 

        self.match = {} #dictionnaire pour stocker les paires, clés := coordonnees de case impaires, objets := class cell de case paires

        all_cells=[] #Initialisation de la liste all_cells, Objet de class Cell avec (i,j) les cases paires et neighbors les voisins valides (par rapport à la couleur)

        all_cells = [Cell((i,j),self.grid.valid_neighbors(i,j)) for i in range(self.grid.n) for j in range(self.grid.m) if (i+j)%2==0]

        for cell in all_cells:            
            if sum(cell.name)%2==0:#On ne regarde que les cell paires
                argument(cell) #on essaye de coupler cell avec l'un de ses voisins
        

        #Liste de paires finale
        self.pairs = [(self.match[el].name,el) for el in self.match.keys()]



class Solver_Ford_Fulkerson(Solver):
    """
    We convert the grid into a bipartite graph : 
        The vertices represent the cells. A cell (i, j) corresponds to the vertex i*m + j.
        The cells are divided between those such that i+j is even or odd.

        If two cells can be paired up (neighbors and matching colours), there is an edge between them.
    
    Using the Ford Fulkerson algorithm, we find a maximal matching of this graph, which we then convert into a list of pairs.
    """


    def grid_to_graph(self): 
        """
        Converts a grid into a graph.

        Output: 
        -----------
        grid_to_graph: Graph
        """

        n , m = self.grid.n, self.grid.m
        edges = {}

        for i in range (n):
            for j in range (m):
                edges[(i,j)] = []
                N = self.grid.valid_neighbors(i,j)

                for cell in N : 
                    edges[(i,j)].append(cell)

        return Graph(edges)
    

    def graph_set(self) : 
        """
        Returns one of the sets which define the bipartite graph.

        Output: 
        -----------
        set: List[int]
            List of the vertices that are part of the first set.
        """
        n, m = self.grid.n, self.grid.m
        S = {}
        
        # The list S is composed of the cells (i, j) such that i+j is even.
        for i in range(n):
            for j in range(m):
                if (i+j) % 2 == 0 :
                    S[(i,j)] = True
                else : 
                    S[(i,j)] = False
        return S


    def matching(self):
        """
        Returns a maximal matching of the bipartite graph using the Ford-Fulkerson algorithm.

        Output: 
        -----------
        matching: Graph
            A maximal matching of the graph.
        """
        S = self.graph_set()

        return self.grid_to_graph().max_matching(S)


    def run(self):
        """
        Each edge of the maximal matching represents a pair of cells. 
        We add those pairs to the result.
        """

        solution = self.matching()
        visited = {}

        for k in solution.edges:
            visited[k] = True
            l = solution.edges[k][0]
            if l not in visited : 
                self.pairs.append((k,l))


class Optimal_Solver(Solver_Ford_Fulkerson): 
    """
    We modelise the problem as a minimum-cost flow problem.
    We convert the grid into a weighted bipartite graph.
    The vertices, edges and sets are the same as the graph created in class SolverFordFulkerson.
    The weights correspond to the edges' gain : that is, whether it is advantageous to select an edge in the final matching or not.
    
    The algorithm is the same as the Ford Fulkerson algorithm, but instead of looking for any path between s and t, we look for shortest paths. 
    """
    def gain(self,cell1,cell2):
        i, j = cell1[0], cell1[1]
        k, l = cell2[0], cell2[1]
        return self.grid.cost((cell1,cell2)) - self.grid.value[i][j] - self.grid.value[k][l]


    def grid_to_weighted_graph(self): 
        """
        Converts a grid into a weighted graph.
        The weight of each edge represents its gain : we define the gain as the cost of the pair minus the sum of the vertices' value.

        Output: 
        -----------
        graph: Graph
        """

        n , m = self.grid.n, self.grid.m
        graph = WeightedGraph({},{})

        for i in range (n):
            for j in range (m):
                graph.edges[(i,j)] = []
                N = self.grid.valid_neighbors(i,j)

                for cell in N : 
                    graph.add_weighted_edge((i,j), cell, self.gain((i,j), cell))

        return graph
    

    def min_cost_matching(self): 
        """
        Returns a minimal cost matching of the bipartite graph.

        Output: 
        -----------
        matching: Graph
        """

        S = self.graph_set()
        graph = self.grid_to_weighted_graph()
        matching = graph.min_cost_flow(S)

        return matching
    

    def run(self):
        """
        Each edge of the minimal cost matching represents a pair of cells. 
        We add those pairs to the result.
        """

        solution = self.min_cost_matching()
        visited = {}

        for k in solution.edges:
            visited[k] = True
            l = solution.edges[k][0]
            if l not in visited : 
                self.pairs.append((k,l))








