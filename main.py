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
    def __init__(self, x, y, tileSize, display):
        self.x: int = x
        self.y: int = y
        self.tileSize: int = tileSize
        self.display: pygame.surface = display  
        self.direction: tuple = pygame.Vector2(0, 0)  
        self.moving: bool = False    
        
    def update(self, dt, event):  
        if not self.moving: 
            if event.type == pygame.TEXTINPUT:
                self.moving = True
                if event.text == "w":
                    self.direction.y = 1
                if event.text == "a":
                    self.direction.x = -1
                if event.text == "s":
                    self.direction.y = -1
                if event.text == "d":
                    self.direction.x = 1    
        
def createTiles():
    for x in range(GRID):
        for y in range(GRID):
            TILES.append(Tile(x, y, TILE_SIZE, display, TILE, OUTLINE))    
            
def newSquare():
    x = np.random.randint(0, 4)
    y = np.random.randint(0, 4)       
    for tile in TILES:
        if tile.x == x and tile.y == y:
            if tile.active:
                newSquare()
            if not tile.active:
                tile.active = True
                SQUARES.append(Squares(x, y, TILE_SIZE, display)) 
                
createTiles()
newSquare()
while 1:
    dt = clock.tick(240) / 250
    display.fill(TILE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    for squares in SQUARES:
        squares.update(dt, event)        
    for tile in TILES:
        tile.drawTile()
        
    pygame.display.flip()