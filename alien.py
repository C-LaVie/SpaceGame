import time

import pygame
import random


class Alien:
    def __init__(self, alienImg, CoorX, CoorY, boundXMin, boundXMax, boundYMin, boundYMax, Level):
        # self.AlienImg = alienImg
        self.nbInvisibleFrame = 0
        self.actionList = []
        self.SpeedX = 2
        self.SpeedY = 2
        self.Level = 1
        self.AlienRecoveryAction = 30
        self. ptsValue = (random.randrange(100)+1)*self.Level
        self.alienFrameCount = 0
        self.FirePower = 25
        self.boundXMax = boundXMax
        self.boundYMax = boundYMax
        self.boundXMin = boundXMin
        self.boundYMin = boundYMin
        self.health = 25

        self.CoorX = CoorX
        self.CoorY = CoorY
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = alienImg
        self.sprite.rect = self.sprite.image.get_rect()
        self.MaxAction = 2
        # add more later like heath, armor etc....

        for i in range(Level):
            self.LevelUp()

    def GetIsAlive(self):
        return self.health != 0

    def SetDamage(self,damage):
        if self.nbInvisibleFrame == 0:
            self.health -= damage
            self.nbInvisibleFrame = 0 # not etra damage for 60 frames
            if self.health < 0: self.health = 0
            return True
        else:
            return False

    def LevelUp(self):
        self.SpeedX += 1
        self.SpeedY += 1
        self.Level += 1
        self.AlienRecoveryAction -= 1
        self.MaxAction +=1
        # need to give limits
        if self.SpeedX >= 8: self.SpeedX = 8
        if self.SpeedY >= 8: self.SpeedY = 8
        if self.AlienRecoveryAction < 1: self.AlienRecoveryAction = 1
        if self.MaxAction >= 6: self.MaxAction = 6

    def UpdateAlien(self, x, y, delta=False):
        if delta:
            self.CoorX += x
            self.CoorY += y
        else:
            self.CoorX = x
            self.CoorY = y
        # check if the coordinate are in our boundary
        if self.CoorX < self.boundXMin: self.CoorX = self.boundXMin
        if self.CoorX > (self.boundXMax - self.sprite.rect[2]): self.CoorX = (self.boundXMax - self.sprite.rect[2])
        if self.CoorY < self.boundYMin: self.CoorY = self.boundYMin  # bound at bottom screen part
        if self.CoorY > (self.boundYMax - self.sprite.rect[3]): self.CoorY = (self.boundYMax - self.sprite.rect[3])
        self.sprite.rect[0] = self.CoorX  # = pygame.Rect(self.CoorX, self.CoorY, 64, 64)
        self.sprite.rect[1] = self.CoorY

    def ChooseActions(self):
        self.actionList.clear()
        random.seed(time.time()+random.randrange(1,100000))
        # 5 actions possible: left, right, up, down, fire
        choiceList = ['left', 'right', 'up', 'down', 'fire']
        choiceWeights = [0.2, 0.2, 0.15, 0.25, 0.1]
        if self.CoorY >= self.boundYMax- self.sprite.rect[3]:
            choiceWeights[3] = 0.05
        self.actionList = random.choices(choiceList, weights=choiceWeights, k=self.MaxAction)
        return self.actionList

    def RecallLastAction(self):
        return self.actionList
