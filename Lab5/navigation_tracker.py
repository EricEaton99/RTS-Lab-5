# import threading
import time




class NavController:
    """
    idea: list of paths each connected
    each path has a:
        direction (nsew)
        pose (xy)
        path_length
        path_far_dist
        open_side

6x12
    """

    def __init__(self, path):
        self.path = path
        self.path_index = 0

        # self.running = True
        # self.thread = threading.Thread(target=self._execute_instructions)
        # self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def turn(self):
        self.path_index += 1
        return self.path_index < len(self.path)
        

    def get_pose(self):
        if self.path_index >= len(self.path):
            return False
        return self.path[self.path_index]

    # def print_pose()



DEFAULT_PATH = [
    ['f', 5],
    ['l', 2],
    ['l', 2],
    ['r', 4],
    ['l', 2],
    ['l', 5],
    ['r', 1],
    ['r', 7],
    ['r', 3],
    ['r', 7],
    ['l', 2],
    ['l', 3],
    ['l', 3],
    ['l', 1],
    ['r', 2],
    ['r', 2],
    ['r', 5],
    # ['w', [5,0], 5, 0, 'f'],
    # ['s', [0,0], 2, 0, 'f'],
    # ['e', [0,2], 2, 0, 'f'],
    # ['s', [2,2], 4, 2, 'f'],
    # ['e', [2,6], 2, 1, 'f'],
    # ['n', [4,6], 5, 1, 'r'],
    # ['e', [4,1], 1, 0, 'f'],
    # ['s', [5,1], 7, -1, 'r'],
]

# def new_direction(direction):
#     mapy = 


# Example usage
if __name__ == "__main__":
    # pose_defined = ['w', [5,0], 5, 0, 'f'],



    navCtrl = NavController(DEFAULT_PATH)
    print(navCtrl.get_pose())
    while navCtrl.turn():
        pose = navCtrl.get_pose()
        # pose_defined = ['w', [5,0], 5, 0, 'f'],
        print(navCtrl.get_pose())

    
