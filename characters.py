import pygame
import math
from gameobject import GameObject


class PacMan(GameObject):
    def __init__(self, speed, color, spawnX, spawnY, currX, currY, rad, xDir=-1, yDir=0):
        self.speed = speed
        self.xDir = xDir
        self.yDir = yDir
        self.color = color
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.currX = currX
        self.currY = currY
        self.rad = rad
        pygame.draw.circle(screen, (255, 255, 0), (self.spawnX, self.spawnY), self.rad)

    def update(self, keysDown, screenWidth, screenHeight):
        if keysDown(pygame.K_LEFT):
            self.xDir = -1
            self.yDir = 0

        if keysDown(pygame.K_RIGHT):
            self.xDir = 1
            self.yDir = 0

        if keysDown(pygame.K_UP):
            self.xDir = 0
            self.yDir = 1
            
        if keysDown(pygame.K_DOWN):
            self.xDir = 0
            self.yDir = -1
        

        super(PacMan, self).update(screenWidth, screenHeight)

    def move(self):
        self.currX += self.xDir * self.speed
        self.currY += self.yDir * self.speed