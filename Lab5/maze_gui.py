import matplotlib.pyplot as plt
import numpy as np
import time

class MazeGUI:
    def __init__(self, maze_grid, path=None):
        self.maze_grid = np.array(maze_grid)
        self.fig, self.ax = plt.subplots(figsize=(6, 10))
        self.robot_position = None  # (row, col)
        self.path = path  # List of (row, col) tuples for the path
        self.obstacle_positions = []  # List of (row, col) where obstacles are detected
        self.key_callbacks = {}  # Dictionary to store key-callback pairs
        self.running = True
        self.thread = threading.Thread(target=self._listen_for_keys)
        self.thread.start()

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
        plt.pause(0.1)  # Allows for real-time updates

    def update_robot_position(self, new_position):
        self.robot_position = new_position
        self.path.append(new_position)
        self.draw_maze()
    
    def detect_obstacle(self, direction):
        if not self.robot_position:
            return
        r, c = self.robot_position
        
        if direction == "south":
            obstacle_pos = (r + 1, c)
        elif direction == "north":
            obstacle_pos = (r - 1, c)
        elif direction == "west":
            obstacle_pos = (r, c - 1)
        elif direction == "east":
            obstacle_pos = (r, c + 1)
       
        # Ensure obstacle position is within maze boundaries
        if 0 <= obstacle_pos[0] < self.maze_grid.shape[0] and 0 <= obstacle_pos[1] < self.maze_grid.shape[1]:
            self.obstacle_positions.append(obstacle_pos)
        
        self.draw_maze()
    
    def animate_movement(self, movement_path, delay=0.5):
        for pos in movement_path:
            self.update_robot_position(pos)
            time.sleep(delay)  # Pause before moving to the next position

    def show(self):
        self.draw_maze()
        plt.show()
    
    def stop(self):
        self.running = False
        self.robot_stop()
        self.raspi.stop()
        self.thread.join()

# Create maze layout
maze = [
    [0, 0, 0, 0, 0, 2],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [3, 0, 0, 0, 0, 0]
]

# Define the path the robot will follow
full_path = [
    (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2),
    (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4), (1, 5),
    (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (8, 4), (8, 3), (8, 2), (7, 2),
    (7, 1), (7, 0), (8, 0), (9, 0), (10, 0), (10, 1), (10, 2), (10, 3), (9, 3), (9, 4),
    (9, 5), (10, 5), (11, 5), (11, 4), (11, 3), (11, 2), (11, 1)
]




if __name__ == "__main__":
    # Create the maze GUI
    gui = MazeGUI(maze, [])

    # Animate robot movement
    gui.animate_movement(full_path, delay=0.3)

    # Show the final state
    gui.show()