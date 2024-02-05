import os
import psutil
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import timeit

class GraphVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualizer")

        self.graph = nx.Graph()
        self.dist = {}
        self.parent = {}
        self.matrix = []

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=1000, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.graph_frame = ttk.Frame(self.master)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.graph_type_var = tk.StringVar(value="Undirected")
        graph_type_label = ttk.Label(self.graph_frame, text="Graph Type:")
        graph_type_menu = ttk.Combobox(self.graph_frame, textvariable=self.graph_type_var,
                                       values=["Undirected", "Directed"])
        graph_type_label.grid(row=0, column=0, padx=10, pady=5)
        graph_type_menu.grid(row=0, column=1, padx=10, pady=5)
        graph_type_menu.bind("<<ComboboxSelected>>", self.update_graph_type)

        ttk.Separator(self.graph_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)

        buttons = [
            ("Generate Predefined Graph", self.generate_predefined_graph),
            ("Run Bellman-Ford Algorithm", self.run_algorithm),
            ("Solve Real-Life Problem", self.solve_real_life_problem),
            ("Add Node", self.add_node),
            ("Add Edge", self.add_edge),
            ("Remove Node", self.remove_node),
            ("Remove Edge", self.remove_edge),
            ("Save Graph", self.save_graph),
            ("Load Graph", self.load_graph),
            ("Clear Graph", self.clear_graph),
        ]
        max_button_width = max(len(text) for text, _ in buttons)
        for i, (text, command) in enumerate(buttons, start=2):
            row = i if i < 9 else i + 1  # Adjust row for the "Run Bellman-Ford Algorithm" button
            tk.Button(self.graph_frame, text=text, command=command, width=max_button_width + 2).grid(row=row, column=0 if i != 2 else 2, columnspan=2, pady=10 if i != 2 else 5)

        ttk.Separator(self.graph_frame, orient=tk.HORIZONTAL).grid(row=len(buttons) + 3, column=0, columnspan=3, sticky="ew", pady=10)

        self.refresh_graph()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def update_graph_type(self, event):
        graph_type = self.graph_type_var.get()
        self.graph = nx.Graph() if graph_type == "Undirected" else nx.DiGraph()
        self.refresh_graph()

    def run_algorithm(self):
        algorithm = "Bellman-Ford"
        try:
            src_vertex = simpledialog.askstring("Input", "Enter source vertex:")
            if src_vertex is not None:
                src_vertex = int(src_vertex)
                execution_time = timeit.timeit(lambda: self.run_bellman_ford(src_vertex), number=1)
                self.display_analysis(execution_time)
                self.generate_adjacency_matrix()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid vertex ID.")

    def run_bellman_ford(self, src):
        self.dist = {node: float("inf") for node in self.graph.nodes}
        self.parent = {node: -1 for node in self.graph.nodes}
        self.dist[src] = 0
        self.matrix = [self.dist.copy()]

        for _ in range(len(self.graph.nodes) - 1):
            for node in self.graph.nodes:
                for neighbor, weight in self.graph[node].items():
                    self.relax(node, neighbor, weight['weight'])
            self.matrix.append(self.dist.copy())

        for node in self.graph.nodes:
            for neighbor, weight in self.graph[node].items():
                if self.dist[node] != float("inf") and self.dist[node] + weight['weight'] < self.dist[neighbor]:
                    messagebox.showerror("Error", "Negative weight cycle detected. Bellman-Ford cannot be applied.")
                    return

        self.visualize_algorithm()

    def relax(self, u, v, weight):
        if self.dist[u] != float("inf") and self.dist[u] + weight < self.dist[v]:
            self.dist[v] = self.dist[u] + weight
            self.parent[v] = u

    def visualize_algorithm(self):
        fig, ax = plt.subplots()
        pos = nx.spring_layout(self.graph, k=0.3, iterations=50)

        nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_size=200, node_color="skyblue")

        if isinstance(self.graph, nx.DiGraph):
            nx.draw_networkx_edges(self.graph, pos, ax=ax, width=1.0, alpha=0.7, arrows=True)
        else:
            nx.draw_networkx_edges(self.graph, pos, ax=ax, width=1.0, alpha=0.7)

        nx.draw_networkx_labels(self.graph, pos, ax=ax)

        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        for edge in self.graph.edges():
            for i, matrix_step in enumerate(self.matrix):
                if matrix_step[edge[1]] == self.dist[edge[1]] and matrix_step[edge[0]] != float("inf"):
                    nx.draw_networkx_edges(self.graph, pos, edgelist=[edge], edge_color='g', ax=ax, width=2.0)
                    canvas.draw()
                    self.master.update()
                    time.sleep(0.1)

        final_path = []
        for node in self.graph.nodes:
            if self.parent[node] != -1:
                final_path.append((self.parent[node], node))

        for i in range(len(final_path)):
            edge = final_path[i]
            for j, matrix_step in enumerate(self.matrix):
                if matrix_step[edge[1]] == self.dist[edge[1]] and matrix_step[edge[0]] != float("inf"):
                    nx.draw_networkx_edges(self.graph, pos, edgelist=[edge], edge_color='r', ax=ax, width=2.0)
                    canvas.draw()
                    self.master.update()
                    time.sleep(0.2)

        messagebox.showinfo("Algorithm Completed", f"Bellman-Ford algorithm completed.")

    def display_analysis(self, execution_time):
        analysis_text = f"Algorithm: Bellman-Ford\n\nExecution Time: {round(execution_time, 4)} seconds\n\n"
        analysis_text += "Final Distance Labels:\n"
        for node, dist in self.dist.items():
            analysis_text += f"Node {node}: {dist}\n"

        messagebox.showinfo("Algorithm Analysis", analysis_text)

    def generate_adjacency_matrix(self):
        matrix_frame = ttk.Frame(self.graph_frame)
        matrix_frame.grid(row=2, column=2, rowspan=7, padx=10)

        #ttk.Label(matrix_frame, text="Adjacency Matrix", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        nodes = sorted(list(self.graph.nodes))
        rows, cols = len(nodes) + 1, len(nodes) + 1

        for i in range(rows):
            for j in range(cols):
                if i == 0 and j == 0:
                    ttk.Label(matrix_frame, text="Node", font=("Helvetica", 10, "bold")).grid(row=i, column=j, padx=5, pady=5)
                elif i == 0:
                    ttk.Label(matrix_frame, text=str(nodes[j - 1]), font=("Helvetica", 10, "bold")).grid(row=i, column=j, padx=5, pady=5)
                elif j == 0:
                    ttk.Label(matrix_frame, text=str(nodes[i - 1]), font=("Helvetica", 10, "bold")).grid(row=i, column=j, padx=5, pady=5)
                else:
                    matrix_value = self.get_matrix_value(nodes[i - 1], nodes[j - 1])
                    ttk.Label(matrix_frame, text=str(matrix_value), font=("Helvetica", 10), width=5).grid(row=i, column=j, padx=5, pady=5)

    def get_matrix_value(self, source, target):
        if source == target:
            return 0
        if target in self.graph[source]:
            return self.graph[source][target]["weight"]
        else:
            return float("inf")

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        pos = nx.spring_layout(self.graph, k=0.3, iterations=50)
        for node, (node_x, node_y) in pos.items():
            if x - 10 <= node_x <= x + 10 and y - 10 <= node_y <= y + 10:
                messagebox.showinfo("Node Information", f"Node: {node}\nDistance: {self.dist[node]}\nParent: {self.parent[node]}")

    def solve_real_life_problem(self):
        # Example: Solving a real-life problem using the graph.
        # You can replace this with your own problem-solving logic.
        self.graph = nx.Graph()
        self.graph.add_nodes_from(["Home", "Work", "Grocery", "Gym", "Park"])
        self.graph.add_weighted_edges_from([("Home", "Work", 5), ("Home", "Grocery", 2), ("Work", "Gym", 3), ("Work", "Park", 4)])

        messagebox.showinfo("Real-Life Problem Solved", "Optimal path found using the graph.")

        self.refresh_graph()

    def generate_predefined_graph(self):
        graph_type = self.graph_type_var.get()
        if graph_type == "Undirected":
            self.graph = nx.Graph()
            self.graph.add_nodes_from([1, 2, 3, 4, 5])
            self.graph.add_weighted_edges_from([(1, 2, 1), (1, 3, 2), (2, 3, 3), (3, 4, 1), (4, 5, 2)])
        else:
            self.graph = nx.DiGraph()
            self.graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
            self.graph.add_weighted_edges_from([(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 5, 4), (5, 6, 5), (6, 7, 6),
                                   (7, 1, -7), (1, 3, 2), (2, 4, 3), (3, 5, 4), (4, 6, 5), (5, 7, 6)])
        self.refresh_graph()


    def add_node(self):
        node_id = simpledialog.askstring("Input", "Enter node ID:")
        if node_id is not None:
            try:
                node_id = int(node_id)
                self.graph.add_node(node_id)
                self.refresh_graph()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter a valid node ID.")

    def add_edge(self):
        edge_str = simpledialog.askstring("Input", "Enter edge (format: source, target, weight):")
        try:
            src, target, weight = map(int, edge_str.split(","))
            self.graph.add_edge(src, target, weight=weight)
            self.refresh_graph()
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please enter valid edge information.")

    def remove_node(self):
        node_id = simpledialog.askstring("Input", "Enter node ID to remove:")
        try:
            node_id = int(node_id)
            self.graph.remove_node(node_id)
            self.refresh_graph()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid node ID.")

    def remove_edge(self):
        edge_str = simpledialog.askstring("Input", "Enter edge to remove (format: source, target):")
        try:
            src, target = map(int, edge_str.split(","))
            self.graph.remove_edge(src, target)
            self.refresh_graph()
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid input. Please enter valid edge information.")

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".graph", filetypes=[("Graph files", "*.graph")])
        if file_path:
            nx.write_gpickle(self.graph, file_path)
            messagebox.showinfo("Save Graph", "Graph saved successfully.")

    def load_graph(self):
        file_path = filedialog.askopenfilename(filetypes=[("Graph files", "*.graph")])
        if file_path:
            self.graph = nx.read_gpickle(file_path)
            self.refresh_graph()

    def clear_graph(self):
        self.graph = nx.Graph()  # or nx.DiGraph() for directed graph
        self.refresh_graph()

    def refresh_graph(self):
        self.canvas.delete("all")

        # Increase canvas size
        canvas_width = 1200
        canvas_height = 800
        self.canvas.config(width=canvas_width, height=canvas_height)

        # Use circular layout for better visualization
        pos = nx.circular_layout(self.graph)

        # Increase node size
        node_size = 300

        nx.draw_networkx_nodes(self.graph, pos, ax=None, node_size=node_size)
        labels = nx.get_edge_attributes(self.graph, 'weight')

        if isinstance(self.graph, nx.DiGraph):
            nx.draw_networkx_edges(self.graph, pos, ax=None, arrows=True, width=2.0)
        else:
            nx.draw_networkx_edges(self.graph, pos, ax=None, width=2.0)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, ax=None)

        for node, (x, y) in pos.items():
            self.canvas.create_oval(x - node_size / 2, y - node_size / 2, x + node_size / 2, y + node_size / 2, fill="blue")
            self.canvas.create_text(x, y, text=str(node), font=("Helvetica", 12, "bold"))

        for (source, target), weight in labels.items():
            x, y = (pos[source] + pos[target]) / 2
            self.canvas.create_text(x, y, text=str(weight), font=("Helvetica", 10))



if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()
