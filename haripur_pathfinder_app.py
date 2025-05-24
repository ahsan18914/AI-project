import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math
import matplotlib.pyplot as plt
import networkx as nx

# ------------------- Graph Data -------------------
haripur_graph = {
    'Main Bazar': {'Haripur City': 2},
    'Haripur City': {'TIP University': 8, 'Chongi': 5, 'Hattar': 15, 'Main Bazar': 2},
    'TIP University': {'Khalabat': 12},
    'Chongi': {'Kotnajibullah': 6},
    'Kotnajibullah': {'Hattar': 7},
    'Khalabat': {'Ghazi': 10},
    'Hattar': {},
    'Ghazi': {}
}

haripur_coordinates = {
    'Main Bazar': (-1, 0),
    'Haripur City': (0, 0),
    'TIP University': (2, 2),
    'Chongi': (1, -1),
    'Kotnajibullah': (2, -2),
    'Hattar': (4, -2),
    'Khalabat': (4, 2),
    'Ghazi': (6, 2)
}

# ------------------- Heuristic Function -------------------
def heuristic(node1, node2):
    x1, y1 = haripur_coordinates[node1]
    x2, y2 = haripur_coordinates[node2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# ------------------- A* Algorithm -------------------
def a_star(start, goal):
    queue = [(heuristic(start, goal), 0, start, [start])]
    visited = {}
    while queue:
        est_total, cost_so_far, current, path = heapq.heappop(queue)
        if current == goal:
            return path
        if current in visited and visited[current] <= cost_so_far:
            continue
        visited[current] = cost_so_far
        for neighbor, edge_cost in haripur_graph[current].items():
            new_cost = cost_so_far + edge_cost
            priority = new_cost + heuristic(neighbor, goal)
            heapq.heappush(queue, (priority, new_cost, neighbor, path + [neighbor]))
    return None

# ------------------- Draw Graph -------------------
def draw_graph(path=None):
    G = nx.Graph()
    for node in haripur_graph:
        for neighbor, weight in haripur_graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = haripur_coordinates
    labels = nx.get_edge_attributes(G, 'weight')
    edge_colors = ['red' if path and (u in path and v in path and abs(path.index(u) - path.index(v)) == 1)
                   else 'black' for u, v in G.edges()]

    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_size=10,
            edge_color=edge_colors, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Haripur City Map - Shortest Path")
    plt.show()

# ------------------- GUI -------------------
def find_path():
    start = start_var.get()
    goal = goal_var.get()
    if start == goal:
        messagebox.showwarning("Warning", "Start and goal cannot be the same.")
        return
    if start not in haripur_graph or goal not in haripur_graph:
        messagebox.showerror("Error", "Invalid locations selected.")
        return
    path = a_star(start, goal)
    if path:
        messagebox.showinfo("Path Found", " → ".join(path))
        draw_graph(path)
    else:
        messagebox.showerror("No Path", "No path found between selected locations.")

# ------------------- Main Application -------------------
root = tk.Tk()
root.title("Haripur Shortest Path Finder")
root.geometry("400x300")
root.config(bg="white")

tk.Label(root, text="Select Start Location", bg="white", font=("Arial", 12)).pack(pady=10)
start_var = tk.StringVar()
start_dropdown = ttk.Combobox(root, textvariable=start_var, values=list(haripur_graph.keys()), state='readonly')
start_dropdown.pack()

tk.Label(root, text="Select Destination", bg="white", font=("Arial", 12)).pack(pady=10)
goal_var = tk.StringVar()
goal_dropdown = ttk.Combobox(root, textvariable=goal_var, values=list(haripur_graph.keys()), state='readonly')
goal_dropdown.pack()

tk.Button(root, text="Find Shortest Path", command=find_path, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

root.mainloop()
