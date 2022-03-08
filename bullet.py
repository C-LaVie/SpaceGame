import pygame


class Bullet:
    def __init__(self, Img, CoorX, CoorY, SpeedY,power=25):
        self.SpeedY = SpeedY
        if self.SpeedY > 40: self.SpeedY = 40
        self.CoorX = CoorX
        self.CoorY = CoorY
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Img
        self.power = power
        self.sprite.rect = self.sprite.image.get_rect()
        self.ptsValue = 10

    def UpdateBullet(self, x, y, delta=False):
        if delta:
            self.CoorX += x
            self.CoorY += y
        else:
            self.CoorX = x
            self.CoorY = y

        self.sprite.rect[0] = self.CoorX
        self.sprite.rect[1] = self.CoorY
