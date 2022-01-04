import pygame as pg
import random


class Game:
    running = False
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pg.Surface((self.screen.get_width(), self.screen.get_height()))
        self.generateNoise(self.canvas.get_width(), self.canvas.get_height())

    def generateNoise(self, sizex, sizey):
        self.noiseSizeX = sizex
        self.noiseSizeY = sizey
        self.randomNoise = [random.random() for _ in range(self.noiseSizeX * self.noiseSizeY)]
        self.noiseWidth = self.canvas.get_width() / self.noiseSizeX
        self.noiseHeight = self.canvas.get_height() / self.noiseSizeY
        self.__generatePerlinNoise()
        self.drawPerlinNoise()

    def __generatePerlinNoise(self):
        nCount = min(self.noiseSizeX, self.noiseSizeY)
        nOctaves = len(bin(nCount)) - 2
        self.perlinNoise = []
        for y in range(self.noiseSizeY):
            for x in range(self.noiseSizeX):
                sum = 0
                mplier = 1
                tMplier = 0
                for j in range(nOctaves):
                    nPitch = self.noiseSizeX >> j

                    sampleX1 = (x // nPitch) * nPitch
                    sampleY1 = (y // nPitch) * nPitch

                    sampleX2 = (sampleX1 + nPitch) % self.noiseSizeX
                    sampleY2 = (sampleY1 + nPitch) % self.noiseSizeY

                    diffX = (x - sampleX1) / nPitch
                    diffY = (y - sampleY1) / nPitch

                    sampleTop = (self.randomNoise[sampleY1 * self.noiseSizeX + sampleX1] * (1 - diffX))
                    sampleTop += (self.randomNoise[sampleY1 * self.noiseSizeX + sampleX2] * diffX)

                    sampleBot = (self.randomNoise[sampleY2 * self.noiseSizeX + sampleX1] * (1 - diffX))
                    sampleBot += (self.randomNoise[sampleY2 * self.noiseSizeX + sampleX2] * diffX)


                    tMplier += mplier
                    sum += (sampleTop * (1 - diffY) + sampleBot * diffY) * mplier
                    mplier *= 0.5
                self.perlinNoise.append(sum / tMplier)

    def drawPerlinNoise(self):
        self.canvas.fill("#000000")
        for y in range(self.noiseSizeY):
            for x in range(self.noiseSizeX):
                startx = x * self.noiseWidth
                starty = y * self.noiseHeight
                c = hex(int(255 * self.perlinNoise[y * self.noiseSizeX + x]))[2:]
                if len(c) == 1:
                    c = "0" + c
                color = "#" + c * 3
                try:
                    pg.draw.rect(self.canvas, color, (startx, starty, self.noiseWidth, self.noiseHeight))
                except:
                    print(color)


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
                        self.generateNoise(self.canvas.get_width(), self.canvas.get_height())
            self.drawloop()


pg.init()
screen = pg.display.set_mode((256, 256))

game = Game(screen)
game.mainloop()