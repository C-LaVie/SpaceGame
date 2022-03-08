import pygame


class Player:
    def __init__(self, Img, CoorX, CoorY, boundXMin, boundXMax, boundYMin, boundYMax):
        # self.AlienImg = alienImg
        self.SpeedX = 5
        self.SpeedY = 5
        self.fireSpeed = 10  # nb frame before next shoot
        self.boundXMax = boundXMax
        self.boundYMax = boundYMax
        self.boundXMin = boundXMin
        self.boundYMin = boundYMin
        self.health = 100
        self.MaxHealth = 150
        self.Level = 1
        self.nbBullets = 0
        self.MaxBullets = 10
        # self.PlayerImg = Img
        self.CoorX = CoorX
        self.CoorY = CoorY
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Img
        self.sprite.rect = self.sprite.image.get_rect()
        self.nbInvisibleFrame = 0
        self.FirePower = 50

    def FireBullet(self):
        if self.nbBullets < self.MaxBullets:
            self.nbBullets += 1
            # need to play the bullet sound
            return True
        else:
            return False

    def ReloadBullet(self):
        self.nbBullets -= 1
        if self.nbBullets < 0: self.nbBullets = 0

    def LevelUp(self):
        self.SpeedX += 1
        self.SpeedY += 1
        self.Level += 1
        self.fireSpeed -= 2
        self.MaxBullets += 2
        self.nbBullets = 0
        self.MaxHealth += 50

        # need to give limits
        if self.SpeedX > 10: self.SpeedX = 10
        if self.SpeedY > 10: self.SpeedY = 10
        if self.fireSpeed < 1: self.fireSpeed = 1
        if self.MaxHealth > 500: self.MaxHealth = 500
        if self.MaxBullets > 30: self.MaxBullets = 30

        self.Healing(100)

    def GetIsAlive(self):
        return self.health != 0

    def SetDamage(self, damage):
        if self.nbInvisibleFrame == 0:
            self.health -= damage
            self.nbInvisibleFrame = 30  # not etra damage for 60 frames
            if self.health < 0: self.health = 0
            return True
        else:
            return False

    def UpdatePlayer(self, x, y, delta=False):
        if self.nbInvisibleFrame > 0:
            self.nbInvisibleFrame -= 1

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

    def Healing(self, value):
        self.health += value
        if self.health > self.MaxHealth:
            self.health = self.MaxHealth
