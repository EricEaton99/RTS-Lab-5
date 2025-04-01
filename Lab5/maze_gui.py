import matplotlib.pyplot as plt
import numpy as np

class MazeGUI:
    def __init__(self, maze_grid, path=None):
        self.maze_grid = np.array(maze_grid)
        self.fig, self.ax = plt.subplots(figsize=(6, 10))
        self.robot_position = None  # (row, col)
        self.path = path  # List of (row, col) tuples for the path
        self.obstacle_positions = []  # List of (row, col) where obstacles are detected

    def draw_maze(self):
        self.ax.clear()
        rows, cols = self.maze_grid.shape
        
        # Draw grid
        for r in range(rows+1):
            self.ax.axhline(y=r, color='black', linewidth=0.5)
        for c in range(cols+1):
            self.ax.axvline(x=c, color='black', linewidth=0.5)
        
        # Fill walls
        for r in range(rows):
            for c in range(cols):
                if self.maze_grid[r, c] == 1:  # Wall
                    self.ax.add_patch(plt.Rectangle((c, rows - r - 1), 1, 1, color='gray', alpha=0.7))
                elif self.maze_grid[r, c] == 2:  # Start
                    self.ax.text(c + 0.5, rows - r - 0.5, 'S', ha='center', va='center', fontsize=12, fontweight='bold')
                elif self.maze_grid[r, c] == 3:  # Finish
                    self.ax.text(c + 0.5, rows - r - 0.5, 'F', ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Draw path with dashed lines if provided
        if self.path:
            path_xs = []
            path_ys = []
            for r, c in self.path:
                path_xs.append(c + 0.5)
                path_ys.append(rows - r - 0.5)
            self.ax.plot(path_xs, path_ys, 'k--', linewidth=1.5)
        
        # Draw robot if position is set
        if self.robot_position:
            r, c = self.robot_position
            self.ax.add_patch(plt.Circle((c + 0.5, rows - r - 0.5), 0.3, color='blue'))
        
        # Draw detected obstacles
        for r, c in self.obstacle_positions:
            self.ax.add_patch(plt.Rectangle((c, rows - r - 1), 1, 1, color='red', alpha=0.7))
        
        self.ax.set_xlim(0, cols)
        self.ax.set_ylim(0, rows)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        plt.tight_layout()
    
    def update_robot_position(self, new_position):
        self.robot_position = new_position
        path.append(new_position)
        self.draw_maze()
    
    def detect_obstacle(self): #direction
        
        if not self.robot_position:
            return
        r, c = self.robot_position
        
        # if direction == "s":
        #     obstacle_pos = (r + 1, c)
            
        # elif direction == "n":
        #     obstacle_pos = (r - 1,c)
            
        # elif direction == "w":
        #     obstacle_pos= (r, c-1)
        
        # elif direction == "e":
        #     obstacle_pos = (r, c+1)
        obstacle_pos = [1, 3]
       
        # Ensure obstacle position is within maze boundaries
        if 0 <= obstacle_pos[0] < self.maze_grid.shape[0] and 0 <= obstacle_pos[1] < self.maze_grid.shape[1]:
            self.obstacle_positions.append(obstacle_pos)
        
        self.draw_maze()
    
    def show(self):
        self.draw_maze()
        plt.show()

# Create maze layout based on your image
# 0 = empty, 1 = wall, 2 = start, 3 = finish
corners = [
    [1,6],[1,1],[4,1], [4,4],[6,4]
]

maze = [
    [1, 1, 1, 1, 1, 1, 1,1],
    [1, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 1, 1, 1, 0,1],
    [1, 0, 0, 0, 0, 1, 2,1],
    [1, 1, 1, 1, 0, 1, 0,1],
    [3, 0, 0, 0, 0, 1, 0,1],
    [1, 1, 1, 1, 1, 1, 0,1]
]

# Define the path shown by dashed lines in the image
path = [
]

full_path = [
    (7,6),(6,6),(5,6),(4,6),(3,6),(2,6),(1,6),(1,5),(1,4),(1,3),(1,2),(1,1),(2,1),(3,1),(4,1),(4,2),(4,3),(4,4),(5,4),(6,4),(6,3),(6,2),(6,1),
    (6,4)
]


        
# Create and show the maze
gui = MazeGUI(maze, path)
gui.show()
