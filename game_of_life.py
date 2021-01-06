#Konstantinos Routsis
import pygame as pg
import random

BOARD_SIZE = WIDTH, HEIGHT = 1280, 840
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 180, 255, 100
CELL_SIZE = 8
MAX_FPS = 14

class game_of_life:
    
    def __init__(self):
        pg.init()
        pg.display.set_caption('Game of Life')
        #icon = pg.image.load('gameolife.png')
        #pg.display.set_icon(icon)
        self.screen = pg.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pg.display.flip()
        self.last_update_completed = 0
        self.desired_ms_between_updates = (1.0 / MAX_FPS) * 1000.0
        self.num_col = int(WIDTH / CELL_SIZE)
        self.num_row = int(HEIGHT / CELL_SIZE)
        self.active_grid = 0
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.paused = False
        
    def init_grids(self):
        #self.grids = [[[0] * self.num_row for i in range(self.num_col)], [[0] * self.num_row for i in range(self.num_col)]] 
        self.grids.append([[0] * self.num_row for i in range(self.num_col)])
        self.grids.append([[0] * self.num_row for i in range(self.num_col)])
        
    def set_grid(self, val = None):
        '''
        set_grid():random
        set_grid(None):random
        set_grid(1):all alive
        set_grid(0):all dead
        '''
        for col in range(self.num_col):
            for row in range(self.num_row):
                if val is None:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = val
                self.grids[self.active_grid][col][row] = cell_value

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def draw_grid(self):
        self.clear_screen()
        for col in range(self.num_col):
            for row in range(self.num_row):
                if self.grids[self.active_grid][col][row] == 0:
                    color = DEAD_COLOR
                elif self.grids[self.active_grid][col][row] == 1:
                    color = ALIVE_COLOR
                
                rectangle_point = pg.draw.rect(self.screen,
                                                   color,
                                                   (int(col * CELL_SIZE + (CELL_SIZE / 2)),
                                                    int(row * CELL_SIZE + (CELL_SIZE / 2)),
                                                    int(CELL_SIZE / 2),
                                                    int(CELL_SIZE / 2)),
                                                   0)
                '''
                circle_point = pg.draw.circle(self.screen,
                                                  color, 
                                                  (int(col * CELL_SIZE + (CELL_SIZE / 2)),
                                                   int(row * CELL_SIZE + (CELL_SIZE / 2))),
                                                  int(CELL_SIZE / 2),
                                                  0)
                '''                                  
        pg.display.flip() #put into mem
        
    def check_cell_neighbours(self, col_index, row_index):
        
        def get_cell(col, row):
            try:
                cell_value = self.grids[self.active_grid][col][row]
            except:
                cell_value = 0
            return cell_value
        
        num_alive_neighbours = 0
        num_alive_neighbours += get_cell(col_index - 1, row_index - 1)
        num_alive_neighbours += get_cell(col_index, row_index - 1)
        num_alive_neighbours += get_cell(col_index + 1, row_index - 1)
        num_alive_neighbours += get_cell(col_index - 1, row_index)
        num_alive_neighbours += get_cell(col_index + 1, row_index)
        num_alive_neighbours += get_cell(col_index - 1, row_index + 1)
        num_alive_neighbours += get_cell(col_index, row_index + 1)
        num_alive_neighbours += get_cell(col_index + 1, row_index + 1)
        #life and death rules
        if self.grids[self.active_grid][col_index][row_index] == 1: #alive
            if num_alive_neighbours > 3: #overpopulation
                return 0
            if num_alive_neighbours < 2: #underpopulation
                return 0 
            if (num_alive_neighbours == 3 or num_alive_neighbours == 4) and self.grids[self.active_grid][col_index][row_index] == 1:
                return 1
        elif self.grids[self.active_grid][col_index][row_index] == 0: #dead
            if num_alive_neighbours == 3:
                return 1
        return self.grids[self.active_grid][col_index][row_index]
        
    def update(self):
        #check current generation state, prepare next generation
        #swap grids
         for col in range(self.num_col):
            for row in range(self.num_row):
                next_gen_state = self.check_cell_neighbours(col, row)
                self.grids[self.inactive_grid()][col][row] = next_gen_state
         self.active_grid = self.inactive_grid()
        
    def inactive_grid(self):
       return (self.active_grid + 1) % 2
                
    def cap_frame_rate(self):
        now = pg.time.get_ticks()
        ms_since_last_update = now - self.last_update_completed
        sleep_time = self.desired_ms_between_updates - ms_since_last_update
        if sleep_time > 0:
            pg.time.delay(int(sleep_time))
        self.last_update_completed = now
        
    def draw_cells(self, x, y, act):
        selected_row = int(y / CELL_SIZE)
        selected_col = int(x / CELL_SIZE)
        #print(selected_col, selected_row)
        if self.grids[self.active_grid][selected_col][selected_row] == 1 and act == 0: #alive cells
            self.grids[self.active_grid][selected_col][selected_row] = 0
            self.draw_grid()
        elif self.grids[self.active_grid][selected_col][selected_row] == 0 and act == 1: #dead cells
            self.grids[self.active_grid][selected_col][selected_row] = 1
            self.draw_grid()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.unicode == 's' or event.unicode == ' ': #toggle pause
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                if event.unicode == 'r': #randomize / restart
                    self.set_grid(None)
                    if self.paused:
                        self.paused = False
                if event.unicode == 'e': #empty grid
                    self.set_grid(0)
                    self.paused = True
                    self.draw_grid()
                if event.unicode == 'f': #full grid
                    self.set_grid(1)
                    self.paused = True
                    self.draw_grid()
                if event.unicode == 'q': #exit game
                    pg.quit()
                    exit()
            if pg.mouse.get_pressed() == (1,0,0): #create new cells
                mx, my = pg.mouse.get_pos()
                self.draw_cells(mx, my, 1)
            elif pg.mouse.get_pressed() == (0,0,1): #kill existing cells
                mx, my = pg.mouse.get_pos()
                self.draw_cells(mx, my, 0)
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def run(self):
        while True:
            self.event_handler()
            if self.paused:
                continue
            self.update()
            self.draw_grid()
            self.cap_frame_rate()

if __name__ == "__main__":
    game = game_of_life()
    game.run()