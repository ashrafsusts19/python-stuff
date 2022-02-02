import pygame as pg
from math import tan
from copy import deepcopy

class Vec3d:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z


class Triangle:
    def __init__(self, v1, v2, v3):
        self.points = [v1, v2, v3]


class Mesh:
    def __init__(self):
        self.tris = []


class Matrix:
    def __init__(self, rows, cols):
        self.matrix = [[0 for i in range(cols)] for j in range(rows)]
        self.rows = rows
        self.cols = cols

    def inputFromList(self, lst):
        for i in range(self.rows * self.cols):
            self.matrix[i // self.cols][i % self.cols] = lst[i]

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise Exception
            lst = []
            for si in range(self.rows):
                for oj in range(other.cols):
                    tot = 0
                    for i in range(self.cols):
                        tot += self.matrix[si][i] * other.matrix[i][oj]
                    lst.append(tot)
            mat = Matrix(self.rows, other.cols)
            mat.inputFromList(lst)
            return mat
        elif isinstance(other, int) or isinstance(other, float):
            lst = []
            for i in range(self.rows):
                for j in range(self.cols):
                    lst.append(self.matrix[i][j] * other)
            mat = Matrix(self.rows, self.cols)
            mat.inputFromList(lst)
            return mat

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            lst = []
            for i in range(self.rows):
                for j in range(self.cols):
                    lst.append(self.matrix[i][j] * other)
            mat = Matrix(self.rows, self.cols)
            mat.inputFromList(lst)
            return mat

    def __str__(self):
        return str(self.matrix)


class GraphicsEngine:
    def __init__(self, screen):
        self.screen = screen
        self.canvas = pg.Surface((self.screen.get_width(), self.screen.get_height()))
        self.clock = pg.time.Clock()
        self.matProj = Matrix(4, 4)
        self.onEngineStart()
        self.createMesh()
        self.zincrement = 0

    def multiplyMatrixVector(self, vec, mat):
        vec2 = Vec3d()
        vec2.x = vec.x * mat.matrix[0][0] + vec.y * mat.matrix[1][0] + vec.z * mat.matrix[2][0] + mat.matrix[3][0]
        vec2.y = vec.x * mat.matrix[0][1] + vec.y * mat.matrix[1][1] + vec.z * mat.matrix[2][1] + mat.matrix[3][1]
        vec2.z = vec.x * mat.matrix[0][2] + vec.y * mat.matrix[1][2] + vec.z * mat.matrix[2][2] + mat.matrix[3][2]
        w = vec.x * mat.matrix[0][3] + vec.y * mat.matrix[1][3] + vec.z * mat.matrix[2][3] + mat.matrix[3][3]
        if w != 0:
            vec2.x /= w
            vec2.y /= w
            vec2.z /= w
        return vec2

    def onEngineStart(self):
        self.fNear = 0.1
        self.fFar = 1000
        self.ffov = 90
        self.fAspectRatio = self.canvas.get_height() / self.canvas.get_width()
        self.fFovRad = 1 / tan(self.ffov * 0.5 / 180 * 3.141582654)
        self.matProj.inputFromList([self.fAspectRatio * self.fFovRad, 0, 0, 0,
                                    0, self.fFovRad, 0, 0,
                                    0, 0, self.fFar / (self.fFar - self.fNear), 1,
                                    0, 0, (-self.fNear * self.fFar) * (self.fFar - self.fNear), 0])

    def createMesh(self):
        self.meshCube = Mesh()
        self.meshCube.tris = [
            Triangle(Vec3d(0, 0, 0), Vec3d(0, 1, 0), Vec3d(1, 1, 0)),
            Triangle(Vec3d(0, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 0, 0)),
            Triangle(Vec3d(1, 1, 0), Vec3d(1, 1, 1), Vec3d(1, 0, 0)),
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 1, 1), Vec3d(1, 0, 1)),
            Triangle(Vec3d(0, 1, 0), Vec3d(0, 1, 1), Vec3d(1, 1, 1)),
            Triangle(Vec3d(0, 1, 0), Vec3d(1, 1, 1), Vec3d(1, 1, 0)),
            Triangle(Vec3d(0, 0, 1), Vec3d(1, 0, 1), Vec3d(0, 1, 1)),
            Triangle(Vec3d(0, 1, 1), Vec3d(1, 0, 1), Vec3d(1, 1, 1)),
            Triangle(Vec3d(0, 0, 0), Vec3d(0, 0, 1), Vec3d(0, 1, 0)),
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 1, 0)),
            Triangle(Vec3d(0, 0, 0), Vec3d(1, 0, 0), Vec3d(0, 0, 1)),
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 0, 1), Vec3d(0, 0, 1)),
        ]

    def drawTriangle(self, canvas, triangle):
        pg.draw.line(canvas, "#ffffff", (triangle.points[0].x, triangle.points[0].y),
                     (triangle.points[1].x, triangle.points[1].y), 1)
        pg.draw.line(canvas, "#ffffff", (triangle.points[1].x, triangle.points[1].y),
                     (triangle.points[2].x, triangle.points[2].y), 1)
        pg.draw.line(canvas, "#ffffff", (triangle.points[2].x, triangle.points[2].y),
                     (triangle.points[0].x, triangle.points[0].y), 1)

    def drawloop(self):
        self.screen.fill("#000000")
        self.canvas.fill("#000000")
        for triangle in self.meshCube.tris:
            triTranslated = deepcopy(triangle)
            for i in range(3):
                triTranslated.points[i].x -= self.zincrement - 3
                triTranslated.points[i].y += self.zincrement - 3
                triTranslated.points[i].z += 3
            v1 = self.multiplyMatrixVector(triTranslated.points[0], self.matProj)
            v2 = self.multiplyMatrixVector(triTranslated.points[1], self.matProj)
            v3 = self.multiplyMatrixVector(triTranslated.points[2], self.matProj)

            v1.x, v1.y = v1.x + 1, v1.y + 1
            v2.x, v2.y = v2.x + 1, v2.y + 1
            v3.x, v3.y = v3.x + 1, v3.y + 1

            v1.x *= 0.5 * self.canvas.get_width()
            v2.x *= 0.5 * self.canvas.get_width()
            v3.x *= 0.5 * self.canvas.get_width()

            v1.y *= 0.5 * self.canvas.get_height()
            v2.y *= 0.5 * self.canvas.get_height()
            v3.y *= 0.5 * self.canvas.get_height()

            triProjected = Triangle(v1, v2, v3)
            self.drawTriangle(self.canvas, triProjected)
        self.screen.blit(self.canvas, (0, 0))
        pg.display.update()

    def mainloop(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.zincrement += 0.01
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
            self.drawloop()





pg.init()
screen = pg.display.set_mode((800, 600))
gameEngine = GraphicsEngine(screen)
gameEngine.mainloop()
