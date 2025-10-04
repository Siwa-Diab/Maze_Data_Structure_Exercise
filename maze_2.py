import random
import matplotlib.pyplot as plt

class Maze:
    def __init__(self, d):
        self.d = d
        self.setD = [-1 for _ in range(d*d)]
        self.walls = {(i, j): True for i in range(d*d) for j in [i+1, i+d] if not ((i+1) % d == 0 and j == i+1) and j < d*d}

    def find_path_compression(self, a):
        while self.setD[a] > 0:
            b = self.setD[a]
            if self.setD[b] > 0:
                self.setD[a] = self.setD[b]
            a = b
        return a
    
    def union(self,a,b):
        root_a=self.find_path_compression(a)
        root_b=self.find_path_compression(b)
        if root_a!= root_b:
            if self.setD[root_a]<=self.setD[root_b]:
                self.setD[root_a] = self.setD[root_b] + self.setD[root_a]
                self.setD[root_b] = root_a
            else:
                self.setD[root_b] = self.setD[root_b] + self.setD[root_a]
                self.setD[root_a] = root_b

            # remove wall
            if (a,b) in self.walls: self.walls[(a,b)] = False
            if (b,a) in self.walls: self.walls[(b,a)] = False

def adjacent_elements(d):
    lst = []
    for i in range(0,d*d):
        if (i+1) % d != 0:  # right neighbor
            lst.append([i, i+1])
        if i < (d*d - d):   # bottom neighbor
            lst.append([i, i+d])
    return lst         

def draw_maze_graphical(m):
    d = m.d
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")

    # draw borders
    for i in range(d+1):
        ax.plot([0, d], [i, i], color="black")  # horizontal
        ax.plot([i, i], [0, d], color="black")  # vertical

    # remove walls according to m.walls
    for (a, b), wall in m.walls.items():
        if not wall:  # if wall removed
            ax.plot([], [])  # placeholder
            # figure out orientation
            if b == a+1:  # right neighbor
                x = a % d
                y = d - 1 - (a // d)
                ax.plot([x+1, x+1], [y, y+1], color="white", linewidth=2)
            elif b == a+d:  # bottom neighbor
                x = a % d
                y = d - 1 - (a // d)
                ax.plot([x, x+1], [y, y], color="white", linewidth=2)

    plt.show()

# -----------------
# RUN IT
# -----------------
d=8
m = Maze(d)
adj = adjacent_elements(d)

def union_adj():
    rand = random.choice(adj)
    m.union(rand[0],rand[1])
    if(m.find_path_compression(0) == m.find_path_compression((d*d)-1)):
        return
    else:
        union_adj()

union_adj()
draw_maze_graphical(m)
