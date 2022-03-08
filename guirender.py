import pygame


class GUI:
    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.fontGO = pygame.font.Font("freesansbold.ttf", 52)
        self.ScoreTextX = 10
        self.ScoreTextY = 10
        self.LevelTextX = 600
        self.LevelTextY = 10

    def RenderScore(self, score):
        score = self.font.render(f"Score: {score}", True, (255, 255, 255))
        return score

    def RenderLevel(self, level):
        score = self.font.render(f"Level: {level}", True, (255, 255, 255))
        return score

    def RenderText(self, text, color=(255, 255, 255)):
        render = self.font.render(text, True, color)
        return render

    def RenderGameOver(self):
        score = self.fontGO.render(f"GAME OVER", True, (255, 10, 30))
        return score

    def RenderRestart(self):
        score = self.font.render(f"Press space button to retry", True, (255, 10, 30))
        return score
