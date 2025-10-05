"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np

class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k']

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self,list_pairs=[],display_color=True):#Display_color permet de controler si l'on veut afficher les couleurs, list_pairs permet de tracer graphiquement les paires si données au préalable
        """
        Plots a visual representation of the grid.

        Parameters:
        -------------
        list_pairs: list
            Liste des pairs que l'on veut afficher avec la représentation, fonctionne pour un paire ((i,j),(k,l)) ou une case seule (i,j)

        display_color: bool 
            Booléen permettant de décier si l'on veut afficher les couleurs (True = on affiche les couleurs)

        Return a representation of the grid using matplotlib.pylpot
        """

        def rect(k,l): #Trace le carré de coordonnée (k,l), col ='couleur' d'affichage

            if display_color:
                col = {0 : 'white', 1 : 'red', 2 : 'blue', 3 : 'green', 4 : 'black'}
            
            else :
                col={0 : 'white', 1 : 'white', 2 : 'white', 3 : 'white', 4 : 'white'}
              

            plt.fill([l,l+1,l+1,l],[self.n-1-k,self.n-1-k,self.n-1-k+1,self.n-1-k+1], color=col[self.color[k][l]])#Comble la case (k,l) de la bonne couleur col

            plt.text(l+0.5,self.n-1-k+0.5,str(self.value[k][l]),fontsize=15,color='black',ha='center',va='center')#Ecrit la valeur de la case (k,l)



        plt.figure()

        for i in range(self.n):
            for j in range(self.m):
                rect(i,j) #Trace chaque case (couleur et value)
        

        #Cadrillage noir
        for i in range(self.n+1):
            plt.plot([0,self.m],[i,i],linewidth=3,color='black')
        
        for j in range(self.m+1):
            plt.plot([j,j],[0,self.n],linewidth=3,color='black')

        #Affichage coordonnées des cases
        for i in range(self.n):#Coordonée ligne
            plt.text(-0.3,self.n-0.5-i,str(i),fontsize=12,color='black',ha='center',va='center')
        for j in range(self.m):#Coordonée colonne
            plt.text(j+0.5,self.n+0.3,str(j),fontsize=12,color='black',ha='center',va='center')


        #Affichage des paires si une liste est fournie

        def plot_pair(cell1,cell2):#Tracer le rectangle qui entoure les cases cell1 et cell2, si cell1==cell2 : entoure la case cell1 seule, donc fonctionne pour une case seule
            if cell1==cell2: #Si il faut entourer une case seule
                min_i = cell1[0]
                max_i = cell1[0]
                min_j = cell1[1]
                max_j = cell1[1]

            else : #Si il faut entourer une paire
                min_i=min(cell1[0],cell2[0])
                max_i=max(cell1[0],cell2[0])
                min_j=min(cell1[1],cell2[1])
                max_j=max(cell1[1],cell2[1])

            coord_x=[min_j+0.1,min_j+0.1,max_j+0.9,max_j+0.9,min_j+0.1]
            coord_y=[self.n-1-min_i+0.9,self.n-1-max_i+0.1,self.n-1-max_i+0.1,self.n-1-min_i+0.9,self.n-1-min_i+0.9]

            plt.plot(coord_x,coord_y,color='purple',linewidth=3)


        #Entourage des paires
        if list_pairs != []:

            visited = [[False for j in range(self.m)] for i in range(self.n)] #Matrice pour vérifier quelles case on a déjà visité

            for cell1,cell2 in list_pairs:

                visited[cell1[0]][cell1[1]]=True
                visited[cell2[0]][cell2[1]]=True

                plot_pair(cell1,cell2)#Entourer les paires avec deux cases différentes

            for i in range(self.n):
                for j in range(self.m):
                    if not visited[i][j] and not self.is_forbidden(i,j):
                        plot_pair((i,j),(i,j))#Entourer les cases seules


        plt.axis('off')#Masquer les axes

        plt.axis('equal')#axes à la même échelle
         
        plt.show()#Affichage
    

    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return self.color[i][j]==4
    


    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        return abs(self.value[pair[0][0]][pair[0][1]] - self.value[pair[1][0]][pair[1][1]])
    

    
    def pair_color(self,coord1,coord2):
        """
        Returns True if the pair between coord1 and coord2 is possible, False otherwise

        Parameters:            
        -----------
        coord1: tuple
            Tuple des coordonnéers (i,j) de la première case

        coord2: tuple
            Tuple des coordonnéers (k,l) de la deuxième case
        """

        #Couleurs des cases
        col1=self.color[coord1[0]][coord1[1]]
        col2=self.color[coord2[0]][coord2[1]]            
        
        #Tesst une case couleur couleur noir
        if col1==4 or col2==4:
            return False
            
        #Test une case couleur blanc
        elif col1==0 or col2==0: 
            return True
            
        #Si une case est rouge ou bleu juste verifier si l'autre n'est pas verte car ni blanch ni noire
        elif ((col1==1 or col1==2) and (col2!=3)) or  ((col2==1 or col2==2) and (col1!=3)):
            return True
            
        #Les deux cases sont vertes
        elif col1==3 and col2==3:
            return True
            
        #Cas restants : bleu-vert et rouge-vert
        else:
            return False
        
    def exist_cell(self,i,j):
        """
        Check if a cell exist, i.e. isn't outside of the grid

        i: int
        j: int
        Such as (i,j) is the coordonate of the cell
        """
        return i<self.n and i>-1 and j<self.m and j>-1
        
    def valid_neighbors(self,i,j):
        """
        Return the list of the possible neighbors of the cell (i,j) regarding the colors

        Parameters:
        -------------
        i:int
        j:int
        Such as (i,j) is the coordonates of the cell we are searching the possible neighbors for
        """

        adjacent_coord=[(-1,0),(0,-1),(1,0),(0,1)]

        valid_neighbors = [(i+el[0],j+el[1]) for el in adjacent_coord if self.exist_cell(i+el[0],j+el[1]) if self.pair_color((i,j),(i+el[0],j+el[1]))]
        
        return valid_neighbors
            

    def all_pairs(self,all_duo=True):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Parameters:
        ------------
        all_duo: bool
            Variable all_duo est la pour savoir si l'on veut toutes les pairs existantes ou faire toutes les paires possibles naivement sans doublons, une case n'apparait pas dans deux paires différentes
            Cette alternative sera utile pour le solverGreedy pour un premier calcul de score

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """

        list_pairs=[]

        if all_duo : 
            #Cas où on prend toutes les paires existantes

            list_pairs = [((i,j),el) for i in range(self.n) for j in range(self.m) for el in self.valid_neighbors(i,j) if (i+j)%2==0]

        else : 
            #Cas où on ne prend qu'une paire par case, pas de boublon, pour faire une première solution pour un premier calcul de score

            visited = [[False for j in range(self.m)] for i in range(self.n)] #Matrice pour vérifier quelles case on a déjà visité

            for i in range(self.n):
                for j in range(self.m):
                    if (i+j)%2==0:
                        for cell in self.valid_neighbors(i,j):
                            if not visited[i][j] and not visited[cell[0]][cell[1]]:
                                visited[i][j]=True
                                visited[cell[0]][cell[1]]=True
                                list_pairs.append(((i,j),cell))
                            
        return list_pairs
    

    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid


