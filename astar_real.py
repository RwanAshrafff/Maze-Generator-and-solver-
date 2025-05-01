
import pygame
from queue import PriorityQueue
from queue import deque
from random import*
import random
#ROWS = 0
#ROWS =  int(input("Enter no. of rows: "))

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze generator and solver application")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:#node(each cell)
	def __init__(self, row, col, width,CR,total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = CR
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])
		
	
Colors = []
def Check_color(x,y):#function to add the barrier position
	Colors.append((x,y))

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def A_star_algorithm(draw,grid,start,end): #A star
    count=0
    open_set=PriorityQueue() # helps to get smallest element out of it 
    open_set.put((0,count,start)) # pytting the start node in the open set 
    came_from={} #to know where we came from
    g_score={spot:float("inf") for row in grid for spot in row } # we initialize it with inf (means infinity )
    g_score[start]=0
    f_score={spot:float("inf") for row in grid for spot in row }
    f_score[start]=h(start.get_pos(),end.get_pos()) 
    open_set_hash={start} # to keep track of elements inside the queue or not 
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit() #a way to exit the game if the user quit 
        current=open_set.get()[2] #2 because i just need the node 
        open_set_hash.remove(current)
        if current==end: 
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True # we Find the path
        for neighbor in current.neighbors:
            temp_g_score=g_score[current]+1
            if temp_g_score<g_score[neighbor]:
                # to find a better path
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos()) 
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current!=start: 
            current.make_closed()
    return False



#algorithms
def DFS_algorithm(draw, grid, start, end):  # DFS
    stack = [start]  # using stack for DFS
    came_from = {}  # to know where we came from
    visited = set()  # to keep track of visited nodes
    visited.add(start)
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # a way to exit the game if the user quits
                
        current = stack.pop()
        
        if current == end:  # we found the path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                stack.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()
        
        draw()
        if current != start:
            current.make_closed()
    
    return False


def bfs_algorithm(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {spot: False for row in grid for spot in row}
    visited[start] = True

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # right, left, down, up

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True  # Path found

        for direction in directions:
            neighbor_row = current.row + direction[0]
            neighbor_col = current.col + direction[1]

            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
                neighbor = grid[neighbor_row][neighbor_col]

                if not visited[neighbor] and not neighbor.is_barrier():  # Directly checking if the node is a wall
                    queue.append(neighbor)
                    visited[neighbor] = True
                    came_from[neighbor] = current
                    neighbor.make_open()#green

        draw()
		

        if current != start:
            current.make_closed() #red
    
    return False  # No path found

def make_grid(rows, width,new_grid = True,mode = 0):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap,CR=WHITE, total_rows=rows)
			grid[i].append(spot)

	if mode == 0:
		grid = edit_grid(rows,grid,width,new_grid)

	return grid

Num_Bar = 5
counter = 0
def edit_grid(rows,grid,width,new_grid = True):
	global Num_Bar
	global counter
	
	for i in range(rows):
		counter = 0
		
		for j in range(rows):
			if(counter == Num_Bar):
				break
			
			if(new_grid):#new grid means that there is no barrier
				Rand = random.randrange(rows)#from 0 to rows-1
				
				spot = grid[i][Rand]#grid[row][random coloumn in the row]
				
				spot.make_barrier()
				counter += 1
				Check_color(i,Rand)#store values of barriers
				
			else:
			
				if((i,j) in Colors):

					spot = grid[i][j]#blit the stored barriers from the barrier random generator
					spot.make_barrier()

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width,ROWS,algo_mode,mode):
	# ROWS = 50
	
	grid = make_grid(ROWS, width,True ,mode)

	start = None
	end = None

	run = True
	
	while run:
		try:
			draw(win, grid, ROWS, width)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					if not start and spot != end:
						start = spot
						start.make_start()
		
					elif not end and spot != start:
						end = spot
						end.make_end()

					elif mode ==1 and spot != end and spot != start:
						spot.make_barrier()
		
				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and start and end:
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)
								
						if algo_mode == 0:
							A_star_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
							start.make_start()
						if algo_mode ==1:
							bfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
							start.make_start()
						if algo_mode == 2:
							DFS_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
							start.make_start()
					if mode == 0:	#Automatic
						if event.key == pygame.K_c:# If "c" key is pressed clear the grid and generate another one
							Colors.clear()
							start = None
							end = None
							grid = make_grid(ROWS, width)
						
						if event.key == pygame.K_1:#Rest the grid and change to A* algorithm
								
								algo_mode = 0
								
								start = None
								end = None
								grid = make_grid(ROWS, width,False)#false to store the old grid
								
						
						if event.key == pygame.K_2:#Rest the grid and change to BFS algorithm
								algo_mode = 1
								
								start = None
								end = None
								grid = make_grid(ROWS, width,False)
						
						if event.key == pygame.K_3:#Rest the grid and change to DFS algorithm
								algo_mode = 2
								
								start = None
								end = None
								grid = make_grid(ROWS, width,False)
					else:#Manual
						if event.key == pygame.K_c:# If "c" key is pressed clear the grid and generate another one
						
							start = None
							end = None
							grid = make_grid(ROWS, width,True,mode)
						
						if event.key == pygame.K_1:#Rest the grid and change to A* algorithm
								
								algo_mode = 0
							
								start = None
								end = None
								grid = make_grid(ROWS, width,False,mode)
								
						
						if event.key == pygame.K_2:#Rest the grid and change to BFS algorithm
								algo_mode = 1
								
								start = None
								end = None
								grid = make_grid(ROWS, width,False,mode)
						
						if event.key == pygame.K_3:#Rest the grid and change to DFS algorithm
								algo_mode = 2
								
								start = None
								end = None
								grid = make_grid(ROWS, width,False,mode)
		except:
			continue
				

	pygame.quit()

#main(WIN, WIDTH,ROWS)