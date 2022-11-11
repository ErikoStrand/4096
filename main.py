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
TILES = []
SQUARES = []
display = pygame.display.set_mode((WIDTH, HEIGHT + 100))
print(TILE_SIZE)
board = np.zeros((GRID, GRID), dtype=classmethod)
print(board)
class Tile:
    def __init__(self, x, y, tileSize, display, tileColor, outlineColor):
        self.x = x
        self.y = y
        self.tileSize: int = tileSize
        self.display = display
        self.tileColor: tuple = tileColor
        self.outlineColor: tuple = outlineColor
        self.active: bool = False
        
    def drawTile(self):
        pygame.draw.rect(self.display, self.outlineColor, (self.x * self.tileSize, self.y * self.tileSize, self.tileSize, self.tileSize), 6)
        
class Squares:
    def __init__(self, x, y, tileSize, display, value):
        self.location: tuple = pygame.Vector2(x, y)
        self.tileSize: int = tileSize
        self.display: pygame.surface = display  
        self.direction: tuple = pygame.Vector2(0, 0)  
        self.moving: bool = False
        self.rect = pygame.Rect(self.location[0] * self.tileSize, self.location[1] * self.tileSize, self.tileSize, self.tileSize)    
        self.value: int = value
        
    def update(self, dt, event, Board):  
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
            self.location[0] = self.location[0] + (dt * self.direction[0] * 2)
            self.location[1] = self.location[1] + (dt * self.direction[1] * 2)       
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

        self.rect = pygame.Rect(self.location[0] * self.tileSize, self.location[1] * self.tileSize, self.tileSize, self.tileSize)
        print(Board)   
                  
    def drawSquare(self):
        pygame.draw.rect(self.display, (100, 100, 100), self.rect)     
        font = pygame.font.Font("bitlow.ttf", 100)
        width, height = pygame.font.Font.size(font, str(self.value))
        draw = font.render(str(self.value), False, (255, 255, 255))
        display.blit(draw, (self.rect.x + width, self.rect.y + height/2)) 
        
def drawInt(text, font_size, x, y, color):
    font = pygame.font.Font("bitlow.ttf", font_size)
    width, height = pygame.font.Font.size(font, str(text))
    draw = font.render(str(text), False, color)
    display.blit(draw, (x, y - height/2))    
             
def createTiles():
    for x in range(GRID):
        for y in range(GRID):
            TILES.append(Tile(x, y, TILE_SIZE, display, TILE, OUTLINE))
            
def newSquare():
    while len(SQUARES) > 0:
        x = np.random.randint(0, 4)
        y = np.random.randint(0, 4)       
        for square in SQUARES:
            if square.location[0] != x and square.location[1] != y:
                SQUARES.append(Squares(x, y, TILE_SIZE, display, np.random.choice([2, 4]))) 
                return
    else:
        SQUARES.append(Squares(1, 1, TILE_SIZE, display, np.random.choice([2, 4])))    
        
createTiles()
newSquare()
newSquare()
while 1:
    dt = clock.tick(240) / 250
    display.fill(TILE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    for square in SQUARES:
        board[int(square.location[1])][int(square.location[0])] = square
        for y in range(GRID):
            for x in range(GRID):
                if square.location[1] != y and square.location[0] != x:
                    board[y][x] = 0
                
    for count, square in enumerate(SQUARES):
        square.update(dt, event, board)        
        square.drawSquare()      
                
    for tile in TILES:
        tile.drawTile()
        
    pygame.display.flip()