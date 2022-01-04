import random


class Noise:
    def __init__(self, sizex, sizey):
        self.generateNoise(sizex, sizey)

    def generateNoise(self, sizex, sizey):
        self.noiseSizeX = sizex
        self.noiseSizeY = sizey
        self.randomNoise = [random.random() for _ in range(self.noiseSizeX * self.noiseSizeY)]
        self.__generatePerlinNoise()


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


height, width = 100, 100
noise = [random.random() for _ in range(height * width)]
ave = sum(noise) / (len(noise))
for y in range(height):
    for x in range(width):
        if noise[y * width + x] >= ave:
            print("#", end="")
        else:
            print(".", end="")
    print()

print("\n\n\n\n")
noic = Noise(100, 100)
ave = sum(noic.perlinNoise) / (len(noic.perlinNoise))
for y in range(noic.noiseSizeY):
    for x in range(noic.noiseSizeX):
        if noic.perlinNoise[y * noic.noiseSizeX + x] >= ave:
            print("#", end="")
        else:
            print(".", end="")
    print()
