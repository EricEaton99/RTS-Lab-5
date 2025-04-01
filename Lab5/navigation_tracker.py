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



def update_direction(direction, turn):
    mapy = {}
    mapy['e'] = 0
    mapy['n'] = 1
    mapy['w'] = 2
    mapy['s'] = 3

    dmappy = {}
    dmappy['f'] = 1
    dmappy['l'] = 1
    dmappy['r'] = -1

    unmappy = ['e','n','w','s']

    new_direction = mapy[direction] + dmappy[turn]
    new_direction %= 3

    return unmappy[new_direction]

def update_pose(start_pose, direction, distance):
    mapy = {}
    mapy['n'] = [0,1]
    mapy['s'] = [0,-1]
    mapy['w'] = [-1,0]
    mapy['e'] = [1,0]

    d_pose = mapy[direction]
    dif_pose = d_pose * distance
    return [start_pose[0] + dif_pose[0], start_pose[1] + dif_pose[1]]



START_POSE = ['w', [5,0], 5, 0, 'f', "forward"]

def update_start_pose(pose):
    START_POSE[1] = update_pose(START_POSE[1], START_POSE[0], pose[1])
    START_POSE[0] = update_direction( START_POSE[0], pose[0])
    START_POSE[2] = pose[1]
    START_POSE[3] = 0
    START_POSE[4] = 'f'
    START_POSE[5] = pose[0]

    print(START_POSE)





# Example usage
if __name__ == "__main__":
    navCtrl = NavController(DEFAULT_PATH)
    pose = navCtrl.get_pose()

    print(START_POSE)

    while navCtrl.turn():
        update_start_pose(pose)

    
