import pygame
import numpy as np
import sys
import math
from colour import Color
pygame.init()
pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP])
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 800
TILE = (205,193,180)
OUTLINE = (187,173,160)
BACKGROUND = (250,248,239)
GRID = 4
TILE_SIZE = int((WIDTH/GRID))
BLOBS = []
display = pygame.display.set_mode((WIDTH, HEIGHT + 100))
board = np.zeros((GRID, GRID), dtype=classmethod)
DISALLOWED = [-1, 4]
ANIMATIONS = []
def drawTime(text, font_size, x, y, color, tileSize, combine):
    font = pygame.font.Font("bitlow.ttf", font_size)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect(center=(x + tileSize/2, y + tileSize/2))
    display.blit(text, text_rect)

class Animation:
    def __init__ (self, start, end, duration, cube, color):
        self.start: tuple = pygame.Vector2(start)
        self.end: tuple = pygame.Vector2(end)
        self.duration: int = duration
        self.cube: tuple = cube
        self.color: tuple = color
    def update(self, dt):
        deltaLen = self.end - self.start
        print(deltaLen)
    
    def draw(self):
        pygame.draw.rect(display, self.color, self.cube)
          
          
class Blobs:
    def __init__(self, x, y, value):
        self.location: tuple = pygame.Vector2(x, y)
        self.direction: tuple = pygame.Vector2(0, 0)
        self.value: int = value
        self.moving: bool = False
        self.move: bool = True
        self.combines: int = 1
        self.moveLenght: int = 0
        
    def update(self, event, grid):       
        if not self.moving:
            self.direction: tuple = pygame.Vector2(0, 0)  
            if event.type == pygame.TEXTINPUT:
                self.moving = True
                if event.text == "w":
                    self.direction.y = -1
                    self.move = False
                    
                elif event.text == "a":
                    self.direction.x = -1
                    self.move = False
                    
                elif event.text == "s":
                    self.direction.y = 1
                    self.move = False
                    
                elif event.text == "d":
                    self.direction.x = 1
                    self.move = False
                    
        if self.moving: 
            if int(self.location[1] + self.direction[1]) not in DISALLOWED and int(self.location[0] + self.direction[0]) not in DISALLOWED:
                if type(grid[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])]) == int:
                    grid[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])] = grid[int(self.location[1])][int(self.location[0])]
                    grid[int(self.location[1])][int(self.location[0])] = 0
                    self.moveLenght += 1
                else:
                    if grid[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])].value == grid[int(self.location[1])][int(self.location[0])].value:
                        grid[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])].value += grid[int(self.location[1])][int(self.location[0])].value
                        grid[int(self.location[1])][int(self.location[0])] = 0
                        self.combines += 1
                    self.moving = False
                    return grid

            self.location[0] = self.location[0] + self.direction[0]
            self.location[1] = self.location[1] + self.direction[1]
            if self.location[0] > 3:
                self.location[0] = 3
                self.moving = False
            elif self.location[0] < 0:
                self.location[0] = 0
                self.moving = False
            elif self.location[1] < 0:
                self.location[1] = 0
                self.moving = False
            elif self.location[1] > 3:
                self.location[1] = 3
                self.moving = False

        return grid        
    
    def drawBlob(self):
        pygame.draw.rect(display, (100, 100, 100), (self.location[0] * TILE_SIZE, self.location[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        drawTime(self.value, 100, self.location[0] * TILE_SIZE, self.location[1] * TILE_SIZE, (255, 255, 255), TILE_SIZE, self.combines)   
         
def drawGrid():
    for x in range(GRID):
        for y in range(GRID):
            pygame.draw.rect(display, OUTLINE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)
            
def newBlob(amount):
    for _ in range(amount):
        x = np.random.randint(0, GRID)
        y = np.random.randint(0, GRID)
        if board[y][x] == 0:
            board[y][x] = Blobs(x, y, np.random.choice([2, 4]))
        else:
            if np.all(board) != 0:
                print("oh shit")
                return
            newBlob(1)
newBlob(1)
while 1:
    if len(ANIMATIONS) > 0:
        ANIMATION = True
    if len(ANIMATIONS) == 0:
        ANIMATION = False 
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and not ANIMATION:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                pass
                #newBlob(1)
                
    display.fill(TILE, (0, 0, WIDTH, HEIGHT))
    #draw "blobs":
    if not ANIMATION:
        for y in board:
            for x in y:
                if type(x) != int:
                    board = x.update(event, board)
                    print(x.location, x.moveLenght)
                    x.drawBlob()       
                             
    if ANIMATION:
        for ani in ANIMATIONS:
            ani.update(dt)
            ani.draw()
            if ani.finished:
                ANIMATIONS.remove(ani)
                
    display.fill(BACKGROUND, (0, WIDTH, WIDTH, 100))
    drawGrid()        
    pygame.display.flip()
   # print(board)