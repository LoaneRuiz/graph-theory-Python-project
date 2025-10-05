# graph-theory-Python-project
### Python project from the first-year enginneering program at ENSAE, Institut Polytechnique de Paris.
The goal of this project was to provide a first practical application of Python skills and to introduce graph theory.
It focuses on finding the least-cost matching of elements in a grid using graph algorithms, in particular bipartite graphs, under a set of predefined constraints.

**I. Definition of the necessary methods**  

**I.1 Explanation of the methods and complexity analysis**

First of all, before solving the problem, it is necessary to define certain methods required for selecting cells and calculating the cost.  

The method *is_forbidden*: returns True if the cell is black, False otherwise.  
The method *cost*: calculates the cost of a pair by taking the absolute value of the difference between the values of the cells in the pair.  
The method *pair_color* checks if two cells can form a pair based on their respective colors. This function seems efficient in terms of speed and space usage, as it performs a fixed number of operations in constant time.  
The function *exist_cell* checks whether a cell exists within the grid boundaries.  
The function *valid_neighbors* returns the list of compatible neighbors of a cell while taking color constraints into account. This method executes in constant time O(1) since it does not depend on the size of the grid.  
The method *all_pairs*: generates a list of cell pairs that respect color and adjacency constraints.  

Adding the parameter *all_duo* allows choosing between two options:  
    *all_duo* = True: all existing pairs are generated  
    *all_duo*= False: duplicates are avoided by ensuring that a cell is used only once in a pair.  
This allows the method to be used flexibly, especially for the next steps in solving the problem.  

We traverse the cells of the grid by focusing on the even cells (i.e., those for which the sum of the coordinates is even) to avoid counting the same pair twice.  

If *all_duo* = True  
We test the 4 adjacent cells (top, left, bottom, then right) using the *pair_color* function.  
Traversing the grid with a double ‘for’ loop gives a complexity of O(n.m), where n and m are the dimensions of the grid. The complexity thus increases with them. Since we must examine all cells, this complexity seems necessary and optimal. Using the pair_color function does not increase the complexity, as the method is efficient.  

If *all_duo* = False  
To avoid duplicates, we store the cells already used in a list list_coord_pairs. Thus, each cell is added only once. However, checking that a cell does not belong to this list may slow execution because there is an additional condition to test. Nevertheless, this maintains a complexity level of the order of O(n.m) as long as list_coord_pairs is of moderate size. The complexity of the function can therefore increase with the size of the grid.

**I.2 Results**  

<img width="315" height="164" alt="Capture d’écran 2025-10-05 à 12 08 52" src="https://github.com/user-attachments/assets/523f597e-464d-4a40-83af-db78b46b2ae4" />  

The *all_pairs* method seems efficient in terms of time.  

**I.3 Improvement suggestion**  

Using a set instead of a list to store the used cells could speed up the membership check. Indeed, this would avoid having to traverse all elements of the list (in the worst case) to check if a cell is stored. However, with a set, the order of the pairs would no longer be guaranteed, which could pose a problem for the next steps of the solution.  

**II. First resolution method**  

**II.1 Method description**  

We propose a first naive solution to the problem. Here, we will use the parameter *all_duo*=False of the *all_pairs* function to define *grid.pairs* in the tests. The method assigns to each even cell the first neighbor with which it can be paired, without considering the cell’s value.  

We introduce the *score* method in the SolverGreedy subclass, which calculates the score of a grid: it sums the scores of the cell pairs and the values of the single cells.  

**II.2 Efficiency and complexity**  

The *visited* list is a matrix of size n.m that allows knowing which cells have already been visited.  

Calculation of the cost of single cells:  
The double ‘for’ loop, which traverses the entire grid, also gives a complexity of O(n.m).
Checking membership in *visited* and that the cell is not black remains of complexity O(1). So in the worst case, the total complexity is O(n².m²).  
Calculation of the cost of pairs gives a complexity of O(n.m). Indeed, we iterate over all pairs and since there are at most (n*m)/2 pairs, the complexity is indeed O(n.m) in the worst case.  

Finally, the complexity of our method can be high and reach O(n².m²) in the worst case.  

**II.3 Results**  
<img width="268" height="82" alt="Capture d’écran 2025-10-05 à 12 14 26" src="https://github.com/user-attachments/assets/7a020b7f-d5be-48d0-9192-358d8d9fa8db" />  

Execution times remain short but seem to increase with the size of the grid. This can be explained by the fact that complexity increases with the size of the grid. This first naive method is quite fast but does not take into account the values of the cells, which leads to errors in pair selection. This is the case, for example, for Grid 5, where this method results in leaving high-value cells alone (such as 7 or 8), which increases the score.  

**II.4 Improvement suggestions**  

To reduce the complexity of calculating the cost of single cells, one could beforehand build a list of unmatched cells directly during the calculation of pairs. However, this would complicate the algorithm upstream.  
Using a set instead of a matrix for *visited* could allow using less memory but might make membership checking slower.  

**III. Special case: all cells have a value of 1**  

**III.1 Explanation of the methods**  

Before implementing a solution algorithm, several elements are defined to facilitate pair construction:  

The *Cell* class represents a cell with its coordinates and compatible neighbors.  
The *visited* set stores already visited cells to avoid repeated cycles.  
The *match* dictionary stores the formed cell pairs, with an odd cell as key and an associated even cell as value.  

In this special case, finding the optimal score comes down to forming the maximum number of possible pairs respecting color and adjacency constraints.  

The *argument* method allows forming pairs according to the following algorithm: for each even cell, it tries to pair it with a neighbor that is not yet used. If this neighbor is already in a pair, the algorithm attempts to find it a new partner recursively before associating it with the new cell. This method optimizes the number of formed pairs.  

Once the pairs are determined, they are returned as a list of tuples containing the coordinates of the associated cells.  

**III.2 Efficiency and complexity:**  

The *argument* method: a cell can be tested with at most four neighbors; if all neighbors are already paired, recursion can be longer if the algorithm needs to modify many pairings. In the worst case, recursion can reach a path proportional to the grid, so complexity can reach O(n.m).  
The *run* method: the command for cell in all_cells iterates over O(n.m) cells. Each call to *argument(cell)* can trigger O(n.m) recursive calls in the worst case. Therefore, the total complexity can reach O(n².m²) in the worst case. However, in practice, the number of recursive calls decreases as pairings stabilize. So on average, the complexity of this method is O(n.m).  
Constructing the final list generates a list of pairs from the *self.match* dictionary, which contains at most O(n.m) elements, so this step has complexity O(n.m).  

Finally, the total complexity of the code for this special case is O(n.m), thus proportional to the grid size, and can increase up to O(n².m²) if the number of recursive calls is large.  

**III.3 Results**  
<img width="123" height="71" alt="Capture d’écran 2025-10-05 à 12 17 40" src="https://github.com/user-attachments/assets/a824327c-af80-48cc-8c46-7be1a3fb2ad1" />  

This solution seems fast and efficient for moderately sized grids. However, for larger grids, the number of recursive calls becomes too high, which poses a problem.  

**III.4 Improvement suggestion:**  

The speed of pairing and the number of recursive calls could be improved if we prioritize cells with the fewest compatible neighbors. However, this would require prior sorting of the cells, which could offset the time gain if the grid is large.  

**IV. Special case: all cells have a value of 1 (Ford-Fulkerson algorithm)**  

**IV.1 Explanation of the algorithm**  

We implement the Ford-Fulkerson algorithm to find a maximal matching. For this, several methods are needed:  
The *grid_to_graph method* converts the grid into a bipartite graph to facilitate the application of the algorithm. Each cell is represented by a vertex, distinguishing even and odd cells. The edges of the graph connecting vertices represent possible pairs between neighboring cells.  
The *graph_set* method separates even cells in the first set (True) and the others in the second set (False).  
The *matching* method applies the Ford-Fulkerson algorithm. The algorithm searches for augmenting paths, i.e., forming pairs that increase the number of matchings by replacing certain existing edges with new ones. The algorithm continues until no augmenting path can be found.  
The *run* function builds the final list of cell pairs.  

**IV.2 Efficiency and complexity**  

The *grid_to_graph* and *set_graph* methods have a complexity of O(n.m) because all cells of the grid are traversed. The complexity of the Ford-Fulkerson algorithm depends on the number of edges (maximum 4nm, as each cell has at most 4 neighbors) and the maximum number of matchings (here (n*m)/2). Thus, in the worst case, the total complexity is O(n².m²). By calling the *matching* function, which itself uses *max_matching*, the run function has a complexity of O(n².m²).  

Comparing with the first method for this special case, both algorithms have similar complexities. However, the Ford-Fulkerson algorithm can suffer from dependence on the maximum flow (since each iteration searches for an augmenting path and increases the flow, contributing to total time complexity), whereas the first algorithm may be complicated by recursion depth.  

**IV.3 Results**  
<img width="185" height="69" alt="Capture d’écran 2025-10-05 à 12 22 31" src="https://github.com/user-attachments/assets/b2585bbe-45fe-474b-8f42-f68e7d46b9b1" />  

**V. General case resolution**  

**V.1 Explanation of the algorithm**  

As with the Ford-Fulkerson algorithm, we first convert the grid into a bipartite graph. Cells represent vertices; edges represent possible pairs between neighboring cells with an associated gain. The gain of a cell pair is calculated by the *gain* method, as the cost of the pair minus the sum of the cells’ values. This corresponds to what is “gained” by pairing these two cells.  

The *grid_to_weighted_graph* method converts the grid into a weighted graph by finding valid neighbors for each cell and adding edges weighted by the gain of each pair.  

Several methods are necessary to find the minimum-cost matching:  
The *find_shortest_path method* finds the shortest path between two vertices in a graph using the Bellman-Ford algorithm. Each vertex and its neighbors are checked to see if the distance can be improved for each edge, attempting to find a shorter path. The method returns the predecessors (vertex it was linked to) and the minimal distance to a neighbor.  
The *shortest_path* method uses the predecessors found by find_shortest_path to reconstruct the path between the two vertices. It initializes a new graph to store the path and returns the path and minimal distance.  
The *min_cost_flow* method uses the paths returned by shortest_path to iteratively improve the matching until an optimal cost matching is reached.  

The *min_cost_matching* method of the Solver class applies *min_cost_flow* to calculate the minimum-cost matching for the bipartite graph.
Finally, the *run* method executes the algorithm and builds the final list of cell pairs. The *visited* dictionary ensures that each cell is visited only once.  

**V.2 Complexity**  

The *grid_to_weighted_graph* method iterates over each cell of the grid, giving a complexity of O(n.m). The *min_cost_matching* method depends on the *shortest_path* method, whose complexity is O(vE) per iteration (where v is the number of vertices and E the number of edges). Thus, in the worst case, V=nm and E=nm, and since there are at most nm iterations, the total complexity is at most O(n³.m³).
The run method iterates over the edges of the minimum-cost matching to add pairs, giving a complexity of O(n.m).
Finally, the total complexity of the algorithm for the general case is at most O(n³.m³).  

**V.3 Results**  
<img width="207" height="71" alt="Capture d’écran 2025-10-05 à 12 26 04" src="https://github.com/user-attachments/assets/d0c924c3-0e1c-4e0f-80ce-24e384f40df6" />
