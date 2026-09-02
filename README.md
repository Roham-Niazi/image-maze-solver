# Image Maze Solver

A Python-based maze solver that uses **image processing and graph-based pathfinding** to find a path between two user-selected points in a maze image.

## Features

* Extracts maze structure from an input image using OpenCV
* Detects horizontal and vertical maze lines and their intersections
* Builds a graph from detected points
* Uses **Breadth-First Search (BFS)** to find a path
* Allows the user to select the start and end points directly on the image
* Visualizes the detected solution on the maze

## How It Works

1. The maze image is converted into a binary representation.
2. Horizontal and vertical structures are detected using morphological image processing.
3. Intersection points are extracted and used as graph nodes.
4. Connections between nodes are detected to build the maze graph.
5. BFS searches the graph for a path between the selected start and end points.
6. The resulting path is drawn on the maze image.

## Limitations

This is an **early version** of the project and is not yet compatible with all types of maze images.

For testing, it is recommended to use **simple rectangular mazes with horizontal and vertical lines**. Some images within this category may still not be detected correctly.

Improving robustness against noisy, complex, and differently structured maze images is planned for future versions.

## Technologies

* Python
* OpenCV
* NumPy
* Gradio
* Graph Algorithms

## License

This project is licensed under the MIT License.
