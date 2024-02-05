# Bellman Ford Algorithm Visualizer

## Introduction
Welcome to the Bellman Ford Algorithm Visualizer repository! This Python script implements a versatile Graph Visualizer using Tkinter for GUI, NetworkX for graph manipulation, and Matplotlib for dynamic graph visualization. The primary goal is to provide users with a user-friendly interface for visualizing graphs, executing graph algorithms, and solving real-life problems.

## Overview

### 2.1 Graph Representation
- The script leverages the NetworkX library for robust representation and manipulation of both undirected and directed graphs.

### 2.2 GUI
- Tkinter is employed to create an intuitive graphical user interface.
- Features include generating predefined graphs, running the Bellman-Ford algorithm, solving real-life problems, and various graph operations (add/remove nodes and edges, save/load graphs, clear the graph, etc.).

### 2.3 Bellman-Ford Algorithm
- Implementation of the Bellman-Ford algorithm for finding shortest paths in weighted graphs.
- Handles negative weight cycles and provides a dynamic visualization of the algorithm's execution.

### 2.4 Real-Life Problem Solving
- Includes a sample real-life problem where the optimal path in a graph is found, showcasing the practical application of the tool.

## Code Structure

### 3.1 Class Structure
- The main class is `GraphVisualizer`, responsible for initializing the GUI and managing graph-related operations.

### 3.2 Methods
- Methods cover graph generation, Bellman-Ford algorithm execution, real-life problem-solving, and graph manipulation functions.

### 3.3 GUI Components
- The GUI comprises buttons for various operations, a canvas for graph visualization, and a matrix frame for displaying the adjacency matrix.

## Graph Visualization

### 4.1 Matplotlib Integration
- Matplotlib is seamlessly integrated into the Tkinter GUI using `FigureCanvasTkAgg` for graph visualization.

### 4.2 Dynamic Visualization
- The script dynamically visualizes the Bellman-Ford algorithm's execution by highlighting edges during each iteration.

## User Interaction

### 5.1 Dialogs
- The application uses dialogs (message boxes and input dialogs) for interacting with the user for input and information display.

### 5.2 Real-Life Problem Solving
- An example demonstrates solving a real-life problem using the graph, illustrating the practical utility of the application.

## Conclusion

The Graph Visualizer successfully combines Tkinter, NetworkX, and Matplotlib to create an interactive tool for graph visualization and manipulation. Whether for graph enthusiasts or those interested in applying graph algorithms practically, this tool provides a versatile and user-friendly interface. The inclusion of the Bellman-Ford algorithm and real-life problem-solving adds educational and practical value.

## Future Enhancements

- Incorporate more graph algorithms for a comprehensive tool.
- Improve user feedback during algorithm execution.
- Enhance error handling for invalid user inputs.

Overall, the code serves as a foundation for further development and exploration in the field of graph theory and algorithms. Feel free to contribute and explore!
