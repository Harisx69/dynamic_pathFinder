import tkinter as tk
from tkinter import ttk
import heapq
import random
import time
import math

CELL_SIZE = 25
SPAWN_PROBABILITY = 0.03

class Node:
    def __init__(self, position):
        self.position = position
        self.g = float('inf')
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")

        self.rows = 20
        self.cols = 20

        self.algorithm = tk.StringVar(value="A*")
        self.heuristic_type = tk.StringVar(value="Manhattan")

        self.dynamic_mode = tk.BooleanVar()

        self.create_ui()
        self.create_grid()

    def create_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(control_frame, text="Rows").pack()
        self.rows_entry = tk.Entry(control_frame)
        self.rows_entry.insert(0, "20")
        self.rows_entry.pack()

        tk.Label(control_frame, text="Columns").pack()
        self.cols_entry = tk.Entry(control_frame)
        self.cols_entry.insert(0, "20")
        self.cols_entry.pack()

        tk.Button(control_frame, text="Create Grid", command=self.reset_grid).pack(pady=5)

        tk.Label(control_frame, text="Algorithm").pack()
        ttk.Combobox(control_frame, textvariable=self.algorithm,
                     values=["A*", "GBFS"]).pack()

        tk.Label(control_frame, text="Heuristic").pack()
        ttk.Combobox(control_frame, textvariable=self.heuristic_type,
                     values=["Manhattan", "Euclidean"]).pack()

        tk.Checkbutton(control_frame, text="Dynamic Mode",
                       variable=self.dynamic_mode).pack()

        tk.Button(control_frame, text="Random Map (30%)",
                  command=lambda: self.generate_random_map(0.3)).pack(pady=5)

        tk.Button(control_frame, text="Start Search",
                  command=self.start_search).pack(pady=5)

        self.metrics_label = tk.Label(control_frame, text="Metrics")
        self.metrics_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.RIGHT)

    def create_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        self.grid[0][0] = 2
        self.grid[self.goal[0]][self.goal[1]] = 3

        self.canvas.config(width=self.cols * CELL_SIZE,
                           height=self.rows * CELL_SIZE)

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.toggle_obstacle)

    def reset_grid(self):
        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())
        self.create_grid()

    def generate_random_map(self, density):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start or (r, c) == self.goal:
                    continue
                if random.random() < density:
                    self.grid[r][c] = 1
                else:
                    self.grid[r][c] = 0
        self.draw_grid()

    def toggle_obstacle(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE
        if (r, c) == self.start or (r, c) == self.goal:
            return
        self.grid[r][c] = 1 if self.grid[r][c] == 0 else 0
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "white"
                if self.grid[r][c] == 1:
                    color = "black"
                elif (r, c) == self.start:
                    color = "orange"
                elif (r, c) == self.goal:
                    color = "purple"

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="gray")

    def heuristic(self, a, b):
        if self.heuristic_type.get() == "Manhattan":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        else:
            return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def get_neighbors(self, node):
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        neighbors = []
        for d in directions:
            nr = node[0] + d[0]
            nc = node[1] + d[1]
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] != 1:
                    neighbors.append((nr, nc))
        return neighbors

    def start_search(self):
        self.nodes_visited = 0
        start_time = time.time()
        self.path = self.search(self.start, self.goal)
        end_time = time.time()

        if self.path:
            self.animate_path()
            path_cost = len(self.path)
        else:
            path_cost = 0

        exec_time = (end_time - start_time) * 1000
        self.metrics_label.config(
            text=f"Visited: {self.nodes_visited}\n"
                 f"Path Cost: {path_cost}\n"
                 f"Time: {exec_time:.2f} ms"
        )

    def search(self, start, goal):
        open_list = []
        heapq.heapify(open_list)

        nodes = {}
        start_node = Node(start)
        start_node.g = 0
        start_node.h = self.heuristic(start, goal)
        start_node.f = start_node.h if self.algorithm.get() == "GBFS" else start_node.g + start_node.h

        heapq.heappush(open_list, start_node)
        nodes[start] = start_node

        closed = set()

        while open_list:
            current = heapq.heappop(open_list)
            self.nodes_visited += 1

            if current.position == goal:
                return self.reconstruct_path(current)

            closed.add(current.position)

            for neighbor_pos in self.get_neighbors(current.position):
                if neighbor_pos in closed:
                    continue

                if neighbor_pos not in nodes:
                    nodes[neighbor_pos] = Node(neighbor_pos)

                neighbor = nodes[neighbor_pos]
                tentative_g = current.g + 1

                if tentative_g < neighbor.g:
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor_pos, goal)
                    if self.algorithm.get() == "GBFS":
                        neighbor.f = neighbor.h
                    else:
                        neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    heapq.heappush(open_list, neighbor)

        return None

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]

    def animate_path(self):
        self.current_index = 0
        self.current_path = self.path
        self.move_agent()

    def move_agent(self):
        if self.current_index >= len(self.current_path):
            return

        pos = self.current_path[self.current_index]
        if pos != self.start and pos != self.goal:
            r, c = pos
            self.canvas.create_rectangle(
                c * CELL_SIZE, r * CELL_SIZE,
                c * CELL_SIZE + CELL_SIZE,
                r * CELL_SIZE + CELL_SIZE,
                fill="green"
            )

        if self.dynamic_mode.get():
            self.spawn_obstacle()

        self.current_index += 1
        self.root.after(100, self.move_agent)

    def spawn_obstacle(self):
        if random.random() < SPAWN_PROBABILITY:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) not in self.current_path and (r, c) != self.goal:
                self.grid[r][c] = 1
                self.draw_grid()

            if (r, c) in self.current_path[self.current_index:]:
                new_start = self.current_path[self.current_index - 1]
                self.start = new_start
                self.path = self.search(self.start, self.goal)
                self.current_index = 0
                self.current_path = self.path


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()