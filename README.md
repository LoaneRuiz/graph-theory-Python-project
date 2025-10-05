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
If all_duo = True
We test the 4 adjacent cells (top, left, bottom, then right) using the pair_color function.
Traversing the grid with a double ‘for’ loop gives a complexity of O(n.m), where n and m are the dimensions of the grid. The complexity thus increases with them. Since we must examine all cells, this complexity seems necessary and optimal. Using the pair_color function does not increase the complexity, as the method is efficient.
If all_duo = False
To avoid duplicates, we store the cells already used in a list list_coord_pairs. Thus, each cell is added only once. However, checking that a cell does not belong to this list may slow execution because there is an additional condition to test. Nevertheless, this maintains a complexity level of the order of O(n.m) as long as list_coord_pairs is of moderate size. The complexity of the function can therefore increase with the size of the grid.
