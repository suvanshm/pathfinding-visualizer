# Pathfinding Visualizer
by Jakub, Jerry and Suvansh

This project is a visualization tool for various pathfinding algorithms. It allows you to choose an algorithm, set a start and end point, and watch as the algorithm finds the shortest path between the two points.

## main.py 

This is the main entry point for the application. Run this script to start the visualizer.

## Algorithms 

This project includes several different pathfinding algorithms, each in its own Python script.

### djikstra.py 

This script implements Dijkstra's algorithm, a popular algorithm for finding the shortest path in a graph. Dijkstra's algorithm works by assigning a cost to each node, starting with 0 for the initial node and infinity for all others. It then repeatedly selects the node with the smallest cost, updates the costs of its neighbors, and marks it as visited. This process continues until the destination node has been visited. Dijkstra's algorithm is guaranteed to find the shortest path, and its time complexity is O((V+E) log V) where V is the number of vertices and E is the number of edges. In our case, all the weights/costs are the same fixed value across the entire grid. So essentially, a dijkstra implementation reduces down to simply breadth-first search with time complexity O(V+E). 

### a_star.py

This script implements the A* algorithm, which is a more efficient algorithm for pathfinding that uses heuristics to guide its search. The A* algorithm works similarly to Dijkstra's algorithm, but in addition to the cost of reaching a node, it also considers an estimate of the cost to reach the destination from that node (the heuristic). This project includes two heuristics: the Manhattan distance, which is the sum of the absolute differences in the x and y coordinates, and the Euclidean distance, which is the square root of the sum of the squares of the differences in the x and y coordinates.  The A* algorithm is also guaranteed to find the shortest path when using an admissible heuristic (one that never overestimates the true cost), and its time complexity is O((V+E) log V).

### dfs.py

This script implements depth-first search, a simple but powerful algorithm that can find a path in a graph. Depth-first search works by exploring as far as possible along each branch before backtracking. While depth-first search is not guaranteed to find the shortest path, it is useful for exploring complex structures due to its simplicity and low memory requirements. Its time complexity is O(V + E).

### bidirectional_bfs.py

This script implements bidirectional breadth-first search, an optimized version of the traditional breadth-first search algorithm. Bidirectional breadth-first search works by simultaneously running two breadth-first searches, one from the start node and one from the end node. When the two searches meet, a path has been found. This can significantly reduce the search space and therefore the time complexity, especially in large graphs. However, it's important to note that this algorithm is not guaranteed to find the shortest path in a graph with weighted edges. Its time complexity is O(V + E) where V is the number of vertices and E is the number of edges.

## How to Use

To use the visualizer, run the `main.py` script. The dependencies are listed in the pyproject.toml file. 
Use right click to toggle start and end nodes, in that order. 
Use left click to toggle walls, or left click + drag mouse to set multiple walls. 
Click on the corresponding button to run the the algorithm. 
Click 'R' to reset the algorithm visualization, retaining the start/end nodes and walls. 
Click 'C' to clear the visualization and also the start/end nodes and walls. 
