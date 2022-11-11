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
class Blobs:
    def __init__(self, x, y, value):
        self.location: tuple = pygame.Vector2(x, y)
        self.direction: tuple = pygame.Vector2(0, 0)
        self.value: int = value
        self.moving: bool = False

    def update(self, event):  
        if not self.moving:
            self.direction: tuple = pygame.Vector2(0, 0)  
            if event.type == pygame.TEXTINPUT:
                self.moving = True
                if event.text == "w":
                    self.direction.y = -1
                if event.text == "a":
                    self.direction.x = -1
                if event.text == "s":
                    self.direction.y = 1
                if event.text == "d":
                    self.direction.x = 1
                    
        if self.moving:
            try:
                if board[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])] != 0:
                    print("hey")
                    self.moving = False
                if board[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])] == 0:
                    board[int(self.location[1] + self.direction[1])][int(self.location[0] + self.direction[0])] = board[int(self.location[1])][int(self.location[0])]
                    board[int(self.location[1])][int(self.location[0])] = 0
            except Exception as e:
                print(e)
                    
            self.location[0] = self.location[0] + self.direction[0]
            self.location[1] = self.location[1] + self.direction[1]     
            if self.location[0] > 3:
                self.location[0] = 3
                self.moving = False
            if self.location[0] < 0:
                self.location[0] = 0
                self.moving = False
            if self.location[1] < 0:
                self.location[1] = 0
                self.moving = False
            if self.location[1] > 3:
                self.location[1] = 3
                self.moving = False
                
        print(self.direction)
    def drawBlob(self):
        pygame.draw.rect(display, (100, 100, 100), (self.location[0] * TILE_SIZE, self.location[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))   
         
def drawGrid():
    for x in range(GRID):
        for y in range(GRID):
            pygame.draw.rect(display, OUTLINE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)
            
def newBlob(amount):
    for _ in range(amount):
        x = np.random.randint(0, GRID)
        y = np.random.randint(0, GRID)
        board[y][x] = Blobs(x, y, np.random.choice([2, 4]))

newBlob(1)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    display.fill(TILE, (0, 0, WIDTH, HEIGHT))
    #draw "blobs":
    for y in board:
        for x in y:
            if x != 0:
                x.update(event)
                x.drawBlob()     
               
    display.fill(BACKGROUND, (0, WIDTH, WIDTH, 100))
    drawGrid()        
    pygame.display.flip()