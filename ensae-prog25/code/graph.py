from collections import deque

class Graph() :
    """
    A class representing the graph. 

    Attributes: 
    -----------
    edges : Dict{vertex : List[vertices]}
        List where edges[i] is a list of i's neighbours.
        The vertices can be coded with different types.
    """

    def __init__(self,adjacency_dict):
        self.edges = adjacency_dict


    def add_edge(self,u,v):
        """ 
        Adds an edge between u and v, oriented towards v.
        If we want to add an edge to an unoriented graph, we would have to add both the edge (u,v) and the edge (v,u).

        Parameters: 
        -----------
        u, v : vertices
        """
        if not (u in self.edges) :
            self.edges[u] = [v]
        else : 
            self.edges[u].append(v)


    def find_path(self,u,v):
        """
        Returns a path between the vertices u and v (or an empty one if it does not exist) using the Breadth-First Search algorithm.

        Parameters: 
        -----------
        u, v: vertices

        Output: 
        -----------
        path: List[int]
            List of vertices that form a path from u to v.
        """

        # Visited is a dictionary that indicates if a vertex has already been seen.
        visited = {}
        predecessors = {}
  
        # We create a queue of paths.
        queue=deque([u])

        # The starting vertex is marked as visited.
        visited[u] = True

        # While the queue is not empty : 
        while queue:
            # We remove the first vertex added to the queue.
            i = queue.popleft()
            
            # If the vertex is v, we have found a path from u to v.
            if i == v:
                   return predecessors

            # Else, we explore i's neighbours
            if i in self.edges : 
                for j in self.edges[i]:
                    if j not in visited :
                        visited[j] = True
                        predecessors[j] = i
                        queue.append(j)
        
        # If the queue is empty, all paths have been considered and none leads to v.  We return an empty dictionary.
        return {}
    

    def path(self,u,v):
        predecessors = self.find_path(u,v)
        path = Graph({})

        if predecessors == {} : 
            return path 
        
        k = predecessors[v]
        while k != u :
            prec = predecessors[k] 
            if prec == 's' : 
                break
            else : 
                path.add_edge(k, prec)
                path.add_edge(prec, k)
                k = prec
        return path


    def matching_graph(self,matching,S):
        """ 
        We consider the bipartite graph calling the method (divided between even and odd vertices) and a matching.
        We define a matching as a sub-graph of the bipartite graph (all edges in the matching are edges in the bipartite graph).

        Matching graph :
        The matching graph is an oriented graph with the same vertices as the bipartite graph, with two more : s and t. We define the edges as such :
            If the even vertex i is not part of an edge in the matching, (s, i) is an edge in the matching graph.
            If the odd vertex i is not part of an edge in the matching, (i, t) is an edge in the matching graph.
            If (i, j) is an edge in the bipartite graph but not in the matching, (i, j) is an edge in the matching graph.
            If (i, j) is an edge in the bipartite graph and in the matching, (j, i) is an edge in the matching graph. 

        Bipartite graph : 
        In a bipartite graph, the vertices are divided into two sets. 
        The set S is one of those two sets, and indicates how the vertices are divided.
        
        Parameters: 
        -----------
        matching: Graph
            A sub-graph of the bipartite graph.
        S: Dict{vertex : bool}
            One of the sets of the bipartite graph. The vertices are divided between those that are in S, and those that are not.

        Output: 
        -----------
        oriented_graph: Graph
            The oriented graph defined above. 
        """

        residual_graph = Graph({"s" : [], "t" : []})

        for k in self.edges : 

            if S[k] : 

                if k not in matching.edges :
                    # The vertex from the first set has no neighbour in matching, add the edge (s, k) to the oriented_graph.
                    residual_graph.add_edge("s",k)

                # Go through k's neighbours, add oriented edges to oriented_graph according to whether they are edges in the matching or not.
                # The graph is bipartite : to go through all edges, it is enough to only scan vertices from one set.
                for l in self.edges.get(k,[]): 
                    if l in matching.edges.get(k,[]) : 
                        residual_graph.add_edge(l,k)
                    else : 
                        residual_graph.add_edge(k,l)

            else :

                if k not in matching.edges :
                    # If the vertex from the other set has no neighbour in matching, we add the edge (k, t) to the oriented_graph.
                    residual_graph.add_edge(k,"t")

        return residual_graph
    

    def symetrical_difference(self, path):
        """
        Returns a graph composed of the edges that are either in the graph calling the method or in the path, but not in both.

        Parameters: 
        -----------
        graph2: Graph
            Has the same vertices as the graph calling the method.

        Output: 
        -----------
        symetrical_difference: Graph
        """

        graph = Graph({})

        for i in self.edges:
            for j in self.edges[i]: 
                if (j not in path.edges.get(i, [])) and (i not in path.edges.get(j, [])) and j != "s":
                    graph.add_edge(i, j)

        for i in path.edges:
            for j in path.edges[i]: 
                if j not in self.edges.get(i, []):
                    graph.add_edge(i, j)

        return graph


    def max_matching(self,S):
        """
        Using the augmenting path algorithm, or Ford-Fulkerson algorithm, returns a maximal matching of the graph.

        Initialisation : 
            Matching <- empty matching
            Oriented graph <- matching graph of Matching

        While there is a path P between s and t in Oriented graph : 
            Augmenting path <- sub-list of P excluding s and t.
            Matching <- symetrical difference of Matching and Augmenting path
            Orienetd grapg <- matchig graph of Matching

        Parameters : 
        -----------
        S: List[int]
            One of the sets that define the bipartite graph.

        Output: 
        -----------
        matching: Graph
            A maximal matching of the graph.
        """

        matching = Graph({})
        residual_graph = self.matching_graph(matching,S) 

        augmenting_path = residual_graph.path("s","t")

        while augmenting_path.edges != {} :
            # Changes matching to the symetrical difference of matching and augmenting_path
            matching = matching.symetrical_difference(augmenting_path)

            # Finds the new oriented graph and an augmenting path between s and t, if it exists
            residual_graph = self.matching_graph(matching,S)
            augmenting_path = residual_graph.path("s","t")
            
        return matching



class WeightedGraph(Graph): 
    """
    A class representing the weighted graph. 

    Attributes: 
    -----------
    edges : List[List[int]]
        List where edges[i] is a list of i's neighbours.

    weight : Dict{tuple[int] : int}
        Dictionary of the edges' weight.
        weight[(i,j)] corresponds to the weight of the edge (i,j).
    """

    def __init__(self,adjacency_dict,weight):
        self.edges = adjacency_dict
        self.weight = weight
    
    def add_weighted_edge(self,u,v,w):
        """ 
        Refer to the function add_edge from the class Graph. 
        The only difference is the addition of the edge's weight.
        """

        self.add_edge(u,v)
        self.weight[(u,v)] = w

    
    def matching_weighted_graph(self,matching,S):
        """ 
        We consider the bipartite graph calling the method (divided between even and odd vertices) and a matching.
        We define a matching as a sub-graph of the bipartite graph (all edges in the matching are edges in the bipartite graph).

        Matching graph :
        The matching graph is an oriented graph with the same vertices as the bipartite graph, with two more : s and t. We define the edges as such :
            If the even vertex i is not part of an edge in the matching, (s, i) is an edge in the matching graph.
            If the odd vertex i is not part of an edge in the matching, (i, t) is an edge in the matching graph.
            If (i, j) is an edge in the bipartite graph but not in the matching, (i, j) is an edge in the matching graph.
            If (i, j) is an edge in the bipartite graph and in the matching, (j, i) is an edge in the matching graph. 

        Bipartite graph : 
        In a bipartite graph, the vertices are divided into two sets. 
        The set S is one of those two sets, and indicates how the vertices are divided.
        
        Parameters: 
        -----------
        matching: Graph
            A sub-graph of the bipartite graph.
        S: Dict{vertex : bool}
            One of the sets of the bipartite graph. The vertices are divided between those that are in S, and those that are not.

        Output: 
        -----------
        oriented_graph: Graph
            The oriented graph defined above. 
        """

        residual_graph = WeightedGraph({"s" : [], "t" : []},{})

        for k in self.edges : 

            if S[k] : 

                if k not in matching.edges :
                    # The vertex from the first set has no neighbour in matching, add the edge (s, k) to the oriented_graph.
                    residual_graph.add_weighted_edge("s",k,0)

                # Go through k's neighbours, add oriented edges to oriented_graph according to whether they are edges in the matching or not.
                # The graph is bipartite : to go through all edges, it is enough to only scan vertices from one set.
                for l in self.edges.get(k,[]): 
                    if l in matching.edges.get(k,[]) : 
                        residual_graph.add_weighted_edge(l,k,-self.weight[(k,l)])
                    else : 
                        residual_graph.add_weighted_edge(k,l,self.weight[(k,l)])

            else :

                if k not in matching.edges :
                    # If the vertex from the other set has no neighbour in matching, we add the edge (k, t) to the oriented_graph.
                    residual_graph.add_weighted_edge(k,"t",0)

        return residual_graph
    

    def find_shortest_path(self,s,t):
        """
        Returns a shortest path between the vertices u and v (or an empty one if it does not exist) using Bellman-Ford's algorithm.

        Parameters: 
        -----------
        s, t: int
            Represent vertices.

        Output: 
        -----------
        path: List[int]
            List of vertices that form a path from u to v.
        """
        n = len(self.edges)
        distance = {k : float('inf') for k in self.edges}    # List of the distances between the vertex s and other vertices, initialised with infinity
        predecessors = {}                                    # List of predecessors in order to keep track of the path
        distance[s] = 0
        
        for _ in range (n-1):                                             # The number of edges that can be in a path
            updated = False
            for u in self.edges :
                for v in self.edges[u] :                                  # Go through all edges (u,v) of the graph
                    if distance[u] + self.weight[(u,v)] < distance.get(v,float('inf')) :
                        distance[v] = distance[u] + self.weight[(u,v)]
                        predecessors[v] = u
                        updated = True
            if not updated : 
                break

        if distance[t] == float('inf') :
            return predecessors, distance[t]
        
        return predecessors, distance[t]
    

    def shortest_path(self,u,v):
        predecessors, dist = self.find_shortest_path(u,v)
        path = Graph({})

        if predecessors == {} : 
            return path 
        
        k = predecessors.get(v,u)
        while k != u :
            prec = predecessors[k] 
            if prec == 's' : 
                break
            else : 
                path.add_edge(k, prec)
                path.add_edge(prec, k)
                k = prec
        return path, dist
    

    def min_cost_flow(self,S):
        """
        Refer to the function max_matching from the class Graph. 
        The only difference is the way we look for a path between s and t. 
        In this version of the algorithm, we use the find_shortest_path function.
        """

        matching = Graph({})
        residual_graph = self.matching_weighted_graph(matching,S)  
        augmenting_path, dist = residual_graph.shortest_path("s","t")

        while augmenting_path.edges != {} :
            
            if dist > 0 :
                break 

            else :
                # Changes matching to the symetrical difference of matching and augmenting_path
                matching = matching.symetrical_difference(augmenting_path)

                # Finds the new oriented graph and an augmenting path between s and t, if it exists
                residual_graph = self.matching_weighted_graph(matching,S)
                augmenting_path, dist = residual_graph.shortest_path("s","t")
        
        return matching