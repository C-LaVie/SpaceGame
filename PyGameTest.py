import pygame
from player import Player
from alien import Alien
from guirender import GUI
from bullet import Bullet
import time
import random


class GameSpaceInv:
    def __init__(self, screenTitle="default", screenHeight=600, screenWeight=800):
        self.level = 1
        self.playerFrameCount = 30
        self.bulletImg = None
        self.Score = 0

        self.state = "init"
        self.Explosion = None
        self.prevTime = 0
        self.fps = 0
        self.CurTime = 0

        self.MaxAlienLine = 5

        self.Background = None
        self.listAlien = []
        self.listDeadAlien = []
        self.playerImg = None
        self.AlienImg = None
        self.icon = None

        self.playerBulletsList = []
        self.aliensBulletsList = []

        self.bIsRunning = False

        self.ScreenHeight = screenHeight
        self.ScreenWeight = screenWeight
        self.Tile = screenTitle
        # init pygame
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./asset/Slower-Tempo-2020-03-22_-_A_Bit_Of_Hope_-_David_Fesliyan.mp3")
        self.fpsClock = pygame.time.Clock()
        self.FPS = 30
        # load the game's asset
        self.LoadAsset()
        # creat ethe screen
        self.screen = pygame.display.set_mode((screenWeight, screenHeight))
        # title and caption
        pygame.display.set_caption(self.Tile)
        pygame.display.set_icon(self.icon)
        self.InitPlayer()
        self.InitAlien(4)
        self.gui = GUI()

    def InitPlayer(self):
        self.Player = Player(self.playerImg, 370, 480, 10, 780, 300, 600)

    def InitAlien(self, nbAliens=10):
        self.listAlien.clear()
        self.listDeadAlien.clear()
        count = 0
        nbAliens = nbAliens + self.level
        if nbAliens > 30: nbAliens = 30
        for i in range(nbAliens):
            # check the line and column according the count
            row = int(count % self.MaxAlienLine)
            Col = int(count / self.MaxAlienLine)
            alien = Alien(self.AlienImg, 150 + 100 * row, 100 * (Col + 1), 10, 780, 50, 500, self.level)
            self.listAlien.append(alien)
            count += 1

    # load the asset for the game
    def LoadAsset(self):
        self.icon = pygame.image.load("./asset/galaxy.png")

        self.playerImg = pygame.image.load("./asset/spaceship.png")
        self.playerImg = pygame.transform.scale(self.playerImg, (64, 64))

        self.AlienImg = pygame.image.load("./asset/ufo.png")
        self.AlienImg = pygame.transform.scale(self.AlienImg, (64, 64))
        self.Background = pygame.image.load("./asset/background_2.jpg")
        self.Background = pygame.transform.scale(self.Background, (self.ScreenWeight, self.ScreenHeight))
        self.Explosion = pygame.image.load("./asset/explosion.png")
        self.Explosion = pygame.transform.scale(self.Explosion, (64, 64))

        self.ExplosionAlien = pygame.image.load("./asset/explosionAlien.png")
        self.ExplosionAlien = pygame.transform.scale(self.ExplosionAlien, (64, 64))

        self.bulletImg = pygame.image.load("./asset/bullet.png")
        self.bulletImg = pygame.transform.scale(self.bulletImg, (16, 16))
        self.alienbulletImg = pygame.image.load("./asset/alienBullet.png")
        self.alienbulletImg = pygame.transform.scale(self.alienbulletImg, (16, 16))

    # this method shall be in charge of processing the game event inputs etc..
    def TreatGameEvent(self):
        # treat the event of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.bIsRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "gameover": self.Reset()
                    elif self.state == "play": self.Pause()
                    elif self.state == "pause": self.Play()

                #     if event.key == pygame.K_UP:
                #         self.Player.UpdatePlayer(0,-1,True)
                #     if event.key == pygame.K_DOWN:
                #          self.Player.UpdatePlayer(0,1,True)

            #     if event.key == pygame.K_LEFT:
            #         self.Player.UpdatePlayer(-1,0,True)
            #     if event.key == pygame.K_RIGHT:
            #         self.Player.UpdatePlayer(1,0,True)
            # if event.type == pygame.KEYUP:
            #     pass # do nothing
        # add more event in future

        if self.state == "play":
            # alien gun fire
            for alienBullet in self.aliensBulletsList:
                if alienBullet.CoorY >= self.ScreenWeight:
                    self.aliensBulletsList.remove(alienBullet)
                elif self.checkCollision(alienBullet.sprite, self.Player.sprite):
                    # remove the alien form the alien list and add points to the score
                    #self.GameOver()
                    if self.Player.SetDamage(alienBullet.power):
                        self.aliensBulletsList.remove(alienBullet)

            for playerBullet in self.playerBulletsList:
                if playerBullet.CoorY < 0:
                    self.playerBulletsList.remove(playerBullet)
                    self.Player.ReloadBullet()
                else:
                    for alien in self.listAlien:
                        if self.checkCollision(playerBullet.sprite, alien.sprite):
                            # remove the alien form the alien list and add points to the score
                            if alien.SetDamage(self.Player.FirePower):
                                self.Score += playerBullet.ptsValue
                            if alien.GetIsAlive() == False:
                                self.Score += alien.ptsValue
                                self.listDeadAlien.append(alien)
                                self.listAlien.remove(alien)
                                try:
                                    self.playerBulletsList.remove(playerBullet)
                                except:
                                    print("Error - ListplayerBullet ")
                                self.Player.ReloadBullet()

            keys = pygame.key.get_pressed()

            x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.Player.SpeedX
            y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.Player.SpeedY

            # fire
            if keys[pygame.K_f]:
                if self.playerFrameCount >= self.Player.fireSpeed:
                    newBullet = Bullet(self.bulletImg, self.Player.CoorX, self.Player.CoorY, -5)
                    if self.Player.FireBullet():
                        self.playerBulletsList.append(newBullet)
                        self.playerFrameCount = 0

            self.playerFrameCount += 1

            # Update player position
            self.Player.UpdatePlayer(x, y, True)
            # Check if collision with spaceship
            for alien in self.listAlien:
                if self.checkCollision(self.Player.sprite, alien.sprite):
                    # collision detected, so do something
                    #self.GameOver()
                    self.Player.SetDamage(alien.FirePower)
                    alien.SetDamage(self.Player.FirePower)
                    if alien.GetIsAlive() == False:
                        self.listDeadAlien.append(alien)
                        self.listAlien.remove(alien)

            for alien in self.listAlien:

                # choose what to do

                if alien.alienFrameCount < alien.AlienRecoveryAction:
                    actionList = alien.RecallLastAction()
                    alien.alienFrameCount += 1
                else:
                    actionList = alien.ChooseActions()
                    alien.alienFrameCount = 0

                alienX = 0
                alienY = 0
                for action in actionList:
                    isFire = False
                    if action == 'left':
                        if alienX==0: alienX = -1 * alien.SpeedX
                    if action == 'right':
                        if alienX==0: alienX = alien.SpeedX
                    if action == 'up':
                        if alienY==0: alienY = -1 * alien.SpeedY
                    if action == 'down':
                        if alienY==0: alienY = alien.SpeedY
                    if action == 'fire':
                        # fire only once per second haha otherwise will be hell fire
                        if (alien.alienFrameCount == 0) and isFire == False:
                            isFire = True
                            newBullet = Bullet(self.alienbulletImg, alien.CoorX+ (alien.sprite.rect[2]/2), alien.CoorY, 5)
                            self.aliensBulletsList.append(newBullet)
                    # treat other later

                # update alien spaceship position
                alien.UpdateAlien(alienX, alienY, True)
                # check collision with the player and with other aliens
                if self.checkCollision(self.Player.sprite, alien.sprite):
                    # collision detected, so do something
                    self.Player.SetDamage(alien.FirePower)
                    # self.GameOver()
                else:
                    for alien2 in self.listAlien:
                        if alien2 is not alien:
                            if self.checkCollision(alien2.sprite, alien.sprite):
                                x1 = -1 * x
                                y1 = -1 * y
                                alien.UpdateAlien(x1, y1, True)

            # resolve the gun fire bullet
            for playerBullet in self.playerBulletsList:
                # update the bullet position first
                playerBullet.UpdateBullet(0, playerBullet.SpeedY, True)
            for alienBullet in self.aliensBulletsList:
                # update the bullet position first
                alienBullet.UpdateBullet(0, alienBullet.SpeedY, True)

            # check if the alien list is empty we level up
            if self.Player.GetIsAlive() == False:
                self.GameOver()

            if len(self.listAlien) == 0 and len(self.listDeadAlien) == 0:
                self.NextLevel()


    def DrawPlayer(self):
        # self.screen.blit(self.Player.PlayerImg, (self.Player.CoorX, self.Player.CoorY))
        if self.state != "gameover":
            #check if we are invisible or normal
            if self.Player.nbInvisibleFrame%2 == 0:
                self.screen.blit(self.Player.sprite.image, (self.Player.CoorX, self.Player.CoorY))
        else:
            self.screen.blit(self.Explosion, (self.Player.CoorX, self.Player.CoorY))

    def DrawBackground(self):
        self.screen.blit(self.Background, (0, 0))

    def DrawAliens(self):
        for alien in self.listAlien:
            # self.screen.blit(alien.AlienImg, (alien.CoorX, alien.CoorY))
            self.screen.blit(alien.sprite.image, (alien.CoorX, alien.CoorY))

        # draw the dead alien
        for alien in self.listDeadAlien:
            alien.alienFrameCount +=1
            if alien.alienFrameCount % 3 > 0:
                self.screen.blit(self.ExplosionAlien, (alien.CoorX, alien.CoorY))
            if alien.alienFrameCount > 45:
                try:
                    self.listDeadAlien.remove(alien)
                except:
                    pass

    def DrawAliensBullet(self):
        for bullet in self.aliensBulletsList:
            # self.screen.blit(alien.AlienImg, (alien.CoorX, alien.CoorY))
            self.screen.blit(bullet.sprite.image, (bullet.CoorX, bullet.CoorY))

    def DrawPlayerBullet(self):
        for bullet in self.playerBulletsList:
            # self.screen.blit(alien.AlienImg, (alien.CoorX, alien.CoorY))
            self.screen.blit(bullet.sprite.image, (bullet.CoorX, bullet.CoorY))
        # draw on the bottom right corner the qty of available bullets
        for index in range(self.Player.MaxBullets - self.Player.nbBullets):
            self.screen.blit(self.bulletImg, ((self.ScreenWeight - 32) - (index * 16), 550))



    def DrawScore(self):
        self.screen.blit(self.gui.RenderScore(self.Score), (self.gui.ScoreTextX, self.gui.ScoreTextY))
        if self.state=="gameover":
            self.screen.blit(self.gui.RenderGameOver(), (250, 400))
            self.screen.blit(self.gui.RenderRestart(), (200, 450))

    def DrawLevel(self):
        self.screen.blit(self.gui.RenderLevel(self.level), (self.gui.LevelTextX, self.gui.LevelTextY))

    def DrawHealth(self):
        self.screen.blit(self.gui.RenderText(f"Health: {self.Player.health}"), (10, 40))

    def DrawPause(self):
        self.screen.blit(self.gui.RenderText(f"PAUSE",color=(158,32,90)), (350, 400))


    def DrawFPS(self):
        self.CurTime = time.time()
        fps = 1 / (self.CurTime - self.prevTime)
        self.prevTime = self.CurTime
        self.screen.blit(self.gui.RenderText(f"FPS: {round(fps)}"), (10, 550))
    # this method will redisplay the screen to the player
    def UpdateScreen(self):
        # do something
        # draw background
        self.DrawBackground()

        self.DrawPlayer()
        self.DrawAliens()
        self.DrawAliensBullet()
        self.DrawPlayerBullet()
        # call the display update
        # draw score
        self.DrawLevel()
        self.DrawScore()
        self.DrawHealth()
        self.DrawFPS()
        if self.state == "pause":
            self.DrawPause()

        pygame.display.update()

    def run(self):
        self.bIsRunning = True

        # the main loop of the game
        self.state = "play"
        pygame.mixer.music.play(-1)
        while self.bIsRunning:
            # clear the screen
            # self.screen.fill(((150, 150, 150)))
            # for event in pygame.event.get():
            self.TreatGameEvent()  # event)
            self.UpdateScreen()
            self.fpsClock.tick(self.FPS)

    def checkCollision(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        return col

    def Reset(self):
        self.Score = 0
        self.level = 1
        self.InitPlayer()
        self.InitAlien(4)
        self.playerBulletsList.clear()
        self.aliensBulletsList.clear()
        self.state = "play"
        pygame.mixer.music.play(-1)

    def GameOver(self):
        # self.bIsRunning = False
        self.state = "gameover"
        pygame.mixer.music.fadeout(2000)

    def NextLevel(self):
        self.level += 1
        self.Player.LevelUp()
        self.InitAlien(4)
        self.playerBulletsList.clear()
        self.aliensBulletsList.clear()

    def Pause(self):
        self.state = "pause"
        pygame.mixer.music.pause()

    def Play(self):
        if self.state == "pause":
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(-1)

        self.state = "play"




