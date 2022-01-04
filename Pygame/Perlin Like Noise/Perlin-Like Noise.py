import pygame as pg
import random


class Game:
    running = False
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pg.Surface((self.screen.get_width(), self.screen.get_height()))
        self.generateNoise(self.canvas.get_width())

    def generateNoise(self, size):
        self.noiseSize = size
        self.randomNoise = [random.random() for _ in range(self.noiseSize)]
        self.noiseWidth = self.canvas.get_width() / self.noiseSize
        self.__generatePerlinNoise()
        self.drawPerlinNoise()

    def __generatePerlinNoise(self):
        nCount = self.noiseSize
        nOctaves = len(bin(nCount)) - 2
        self.perlinNoise = []
        for i in range(nCount):
            sum = 0
            mplier = 1
            tMplier = 0
            for j in range(nOctaves):
                nPitch = nCount >> j
                sample1 = (i // nPitch) * nPitch
                sample2 = (sample1 + nPitch) % nCount
                diff = (i - sample1) / nPitch
                tMplier += mplier
                sum += (self.randomNoise[sample1] * (1 - diff) + self.randomNoise[sample2] * diff) * mplier
                mplier *= 0.5
            self.perlinNoise.append(sum / tMplier)

    def drawPerlinNoise(self):
        self.canvas.fill("#000000")
        for i in range(self.noiseSize):
            startx = i * self.noiseWidth
            starty = (1 - self.perlinNoise[i]) * self.canvas.get_height()
            height = self.perlinNoise[i] * self.canvas.get_height()
            pg.draw.rect(self.canvas, "#ffffff", (startx, starty, self.noiseWidth, height))

    def drawloop(self):
        self.screen.fill("#000000")
        self.screen.blit(self.canvas, (0, 0))
        pg.display.update()


    def mainloop(self):
        self.running = True
        while self.running:
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_SPACE:
                        self.generateNoise(self.canvas.get_width())
            self.drawloop()


pg.init()
screen = pg.display.set_mode((800, 400))

game = Game(screen)
game.mainloop()