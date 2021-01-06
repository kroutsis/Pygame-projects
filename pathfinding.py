#Konstantinos Routsis
import pygame as pg
import sys, math, time, heapq

pg.init()
pg.font.init()

SIZE = WIDTH, HEIGHT = 658, 658
BLOCK_SIZE = 20
COLLUMNS = 30#int(WIDTH / BLOCK_SIZE)
ROWS = 30#int(HEIGHT / BLOCK_SIZE) 

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 204
YELLOW = 255, 255, 0

screen = pg.display.set_mode(SIZE)

class Maze:

    walls = []
    borders = []
    
    for i in range(30):
        walls.append((i,0))
        walls.append((i,29))
        walls.append((0,i))
        walls.append((29,i))
    borders.extend(walls)

    def create_grid(self):
        screen.fill(BLACK)
        for i in range(ROWS):
            for j in range(COLLUMNS):
                if (i, j) not in self.walls:
                    pg.draw.rect(screen, WHITE, (i*(BLOCK_SIZE+2), j*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))

    def build_wall(self, x, y):
        if (x, y) not in self.borders:
            if (x, y) not in self.walls:
                self.walls.append((x, y))
                pg.draw.rect(screen, BLACK, (x*(BLOCK_SIZE+2), y*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
            else:
                self.walls.remove((x, y))
                pg.draw.rect(screen, WHITE, (x*(BLOCK_SIZE+2), y*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))

class Pathfinding(Maze):

    class Node:
        def __init__(self, parent, pos=None):
            self.pos = pos
            self.parent = parent
            
            self.g = 0
            self.h = 0
            self.f = 0
            
        def __eq__(self, other):
            return self.pos == other.pos

    def __init__(self, start, target):
        self.open_nodes = []
        self.closed_nodes = []
        self.unexplored_nodes = []
        self.explored_nodes = {}
        self.queue = []

        self.start = start
        self.target = target

        self.start_node = self.Node(None, self.start)
        self.target_node = self.Node(None, self.target)
        self.update_grid()

    def get_neighbours(self, current_node):
        neighbour_nodes_pos = [(current_node.pos[0]-1, current_node.pos[1]-1),
                               (current_node.pos[0], current_node.pos[1]-1),
                               (current_node.pos[0]+1, current_node.pos[1]-1),
                               (current_node.pos[0]+1, current_node.pos[1]),
                               (current_node.pos[0]+1, current_node.pos[1]+1),
                               (current_node.pos[0], current_node.pos[1]+1),
                               (current_node.pos[0]-1, current_node.pos[1]+1),
                               (current_node.pos[0]-1, current_node.pos[1])]
        return neighbour_nodes_pos

    def create_graph(self):
        graph = {}
        for i in range(ROWS):
            for j in range(COLLUMNS):
                if (i, j) not in Maze.walls:# and (i, j) != start:
                    current_node = self.Node(None, (i,j))
                    graph[current_node.pos] = {}
                    neighbour_nodes_pos = self.get_neighbours(current_node)
                          
                    for neighbour in neighbour_nodes_pos:
                        if neighbour[0] == current_node.pos[0] or neighbour[1] == current_node.pos[1]:
                            graph[current_node.pos][neighbour] = 10
                        else:
                            graph[current_node.pos][neighbour] = 14
        return graph

    def a_star(self):
        self.open_nodes.append(self.start_node)
        
        while self.open_nodes:
            
            current_node = self.open_nodes[0]
            for node in self.open_nodes:
                if node.f < current_node.f:
                    current_node = node
            
            self.open_nodes.remove(current_node)
            self.closed_nodes.append(current_node)
            
            if current_node == self.target_node:
                path = []
                temp = current_node
                while temp is not None:
                    path.append(temp.pos)
                    temp = temp.parent
                self.show_path(path)  
                return True
            
            child_nodes_list = []
            neighbour_nodes_pos = self.get_neighbours(current_node)

            for child_pos in neighbour_nodes_pos:
                if child_pos in Maze.walls:
                    continue
                else:
                    child_node = self.Node(current_node, child_pos)
                child_nodes_list.append(child_node)
            
            for child_node in child_nodes_list:
                if child_node in self.closed_nodes:
                    continue

                if child_node.pos[0] == current_node.pos[0] or child_node.pos[1] == current_node.pos[1]:
                    child_node.g = current_node.g + 10
                else:
                    child_node.g = current_node.g + 14
                
                x = abs(child_node.pos[0] - self.target_node.pos[0])
                y = abs(child_node.pos[1] - self.target_node.pos[1])
                if x == y:
                    child_node.h = x*14
                elif x > y:
                    child_node.h = y*14+(x-y)*10
                elif x < y:
                    child_node.h = x*14+(y-x)*10
      
                #child_node.g = current_node.g + 1
                #child_node.h = 0 #Algorithm becomes Dijkstras
                #child_node.h = abs(child_node.pos[0] - self.target_node.pos[0]) + abs(child_node.pos[1] - self.target_node.pos[1])
                #child_node.h = ((child_node.pos[0] - self.target_node.pos[0])**2) + ((child_node.pos[1] - self.target_node.pos[1])**2)
                
                child_node.f = child_node.g + child_node.h
                
                for node in self.open_nodes:
                    if node == child_node and node.g < child_node.g:
                        continue

                if child_node not in self.open_nodes:
                    self.open_nodes.append(child_node)
                    
            self.update_grid() 
            pg.display.flip()   

    def dijstra(self):
        graph = self.create_graph()
        unexplored_nodes = {node: math.inf for node in graph}
        start_node_pos = self.start_node.pos
        current_node = self.start_node
        current_node.f = 0
        unexplored_nodes[current_node.pos] = current_node.f

        self.queue = [(current_node.f, current_node.pos)]
        while self.queue:
            current_node.f, current_node.pos = heapq.heappop(self.queue)
            self.explored_nodes[current_node.pos] = current_node.f
            
            if current_node.pos == self.target_node.pos:
                path = []
                while current_node.pos != start_node_pos:
                    min_distance = self.explored_nodes[current_node.pos]
                    for i in graph[current_node.pos].keys():
                        if i not in self.explored_nodes:
                            continue
                        if min_distance > self.explored_nodes[i]:
                            min_distance = self.explored_nodes[i]
                            parrent_node = i
                    path.append(current_node.pos)
                    current_node.pos = parrent_node
                    
                path.append(self.start_node.pos)
                self.show_path(path)
                return True

            if current_node.f > unexplored_nodes[current_node.pos]:
                continue

            for neighbour, distance in graph[current_node.pos].items():
                if neighbour not in unexplored_nodes:
                    continue
                new_distance = current_node.f + distance
                if unexplored_nodes[neighbour] is math.inf or new_distance < unexplored_nodes[neighbour]:
                    unexplored_nodes[neighbour] = new_distance
                    heapq.heappush(self.queue, (new_distance, neighbour))

            self.update_grid() 
            pg.display.flip() 
        
    def update_grid(self):
        screen.fill(BLACK)
        for i in range(ROWS):
            for j in range(COLLUMNS):
                if (i, j) not in Maze.walls:
                    pg.draw.rect(screen, WHITE, (i*(BLOCK_SIZE+2), j*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE)) 
        
        pg.draw.rect(screen, BLUE, (self.start[0]*(BLOCK_SIZE+2), self.start[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
        pg.draw.rect(screen, RED, (self.target[0]*(BLOCK_SIZE+2), self.target[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
        
        for node in self.open_nodes:
            pg.draw.rect(screen, GREEN, (node.pos[0]*(BLOCK_SIZE+2), node.pos[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
        for node in self.closed_nodes:
            pg.draw.rect(screen, RED, (node.pos[0]*(BLOCK_SIZE+2), node.pos[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
        
        for node in self.explored_nodes:
            pg.draw.rect(screen, RED, (node[0]*(BLOCK_SIZE+2), node[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
        for node in self.queue:
            pg.draw.rect(screen, GREEN, (node[1][0]*(BLOCK_SIZE+2), node[1][1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))

    def show_path(self, path):
        for node in path:
            pg.draw.rect(screen, BLUE, (node[0]*(BLOCK_SIZE+2), node[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
            pg.display.flip()
            time.sleep(.02)

class Controls:

    clickcount = 0

    def get_tile_position(self):
        pos = pg.mouse.get_pos()
        x = pos[0] // 22
        y = pos[1] // 22
        return x, y
        
    def event_handler(self, m):
        global start
        global target
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.clickcount == 0:
                    start = self.get_tile_position()
                    pg.draw.rect(screen, BLUE, (start[0]*(BLOCK_SIZE+2), start[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
                    self.clickcount += 1
                elif self.clickcount == 1:
                    temp = self.get_tile_position()
                    if temp != start:
                        target = temp
                        pg.draw.rect(screen, RED, (target[0]*(BLOCK_SIZE+2), target[1]*(BLOCK_SIZE+2), BLOCK_SIZE, BLOCK_SIZE))
                        self.clickcount += 1
                else:
                    x, y = self.get_tile_position()
                    if (x, y) != start and (x, y) != target:
                        m.build_wall(x, y)
            if event.type == pg.KEYDOWN:
                p = Pathfinding(start, target)
                if event.key == pg.K_1:
                    if p.a_star():
                        time.sleep(2)
                if event.key == pg.K_2:
                    if p.dijstra():
                        time.sleep(2) 
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_SPACE:
                    p = Pathfinding(start, target)

    def run(self):
        m = Maze()
        m.create_grid()
        while True:
            self.event_handler(m)
            pg.display.flip()

if __name__=="__main__":

    print("\n---- INSTRUCTIONS ----\n")
    print("Click to place Start Node, Target Node and Mazes Walls")
    print("Press 1 to use A*(star) searching algorithm")
    print("Press 2 to use Dijkstra's searching algorithm")
    print("Press SPACE to clear Grid")
    print("Press Q to Quit")
    
    c = Controls()
    c.run()