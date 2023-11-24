# Graph Algorithm Visualizer

## Description

Develop a visualization tool for graph traversal algorithms, focusing on Dijkstra and A* algorithms, utilizing Python and Pygame.

## Project Structure

- **algorithms**
  - `dijkstra.py`: Implementation of Dijkstra's algorithm.
  - `a_star.py`: Implementation of A* algorithm for pathfinding.
- **components**
  - `spot.py`: Definition and management of a spot/node in the grid.
  - `grid.py`: Handling grid functionality, drawings, and updates.
- **assets**
  - `demo.mov`: A demonstration video providing an example of expected outcomes.
- **main.py**: Main script to execute the application.
- **pyproject.toml**: Configuration file for Poetry, outlining project dependencies.

## Prerequisites

- **Python** (3.x recommended)
- **Poetry**
- **Pygame**

To install dependencies, utilize Poetry:
```bash
poetry add pygame
```

Ensure the virtual environment is active when running the project.

### Bonus: Beat Python’s Built-in (10% Extra Points)

Outperform Python's built-in graph traversal in terms of time complexity using one of your implemented algorithms. Ensure relevant comparisons (e.g., Dijkstra with Dijkstra). Document your results, methodology, and findings in your README.md. It is also important to mention why your implementation is able to outperform (or not) the built-in traversal. Bonus points can carry over to other assignments, such as the midterm. Of course, if you produce very impressive results, you may be rewarded with more than 10% extra points and might consider writing a paper about it. You can be creative with your methodology, but ensure that it is valid and reproducible. Include unit tests and screenshots of your results.

## Grading Rubric

1. **Algorithm Implementation and Visualization**: 50% (65% for solo participants)
   - Effective implementation and visualization of **Dijkstra and A* algorithms**.
2. **Code Quality and User Interaction**: 15%
   - Maintain code quality and ensure intuitive user interactions.
   - Modular code with proper documentation.
   - If you want more methodology points, please make sure your code is properly organized and documented so that I can understand your methodology. If not properly documented, I will not be able to understand your methodology and will not be able to give you points.
3. **Testing and Validation**: 20%
   - Validate the algorithm’s correctness and efficiency through testing.
4. [Optional] **Pathfinding Statistics**: 5% (for groups only)
   - Time taken to traverse. [done]
   - How many nodes were traversed (space complexity). [done]
   - One or two additional statistics of your choice. The more the merrier. Be creative! [path_len, max queue size]
5. [Optional] **Additional Algorithm(s) Implementation**: 10% (for groups only)
   - Implement two more graph traversal algorithms at least. [dfs, ]


## Your README

In your ```README.md```, include:
- Descriptions of algorithms implemented.
- Encountered issues or challenges.
- Instructions on code execution.
- [If applicable] Methodology and findings from the bonus challenge of beating Python’s built-in algorithms.
- Any extra information you would like to share with me.
- **List the names of all group members, or your own name if you are a solo participant.**

