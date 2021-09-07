import pygame as pg
import random

class Root():
    def __init__(self, value):
        self.value = value
        self.child = []

    def addChild(self, value):
        self.child.append(Root(value))
        return self.child[-1]

    def children(self):
        return self.child


class Game():
    isMage = False
    endPoint = 399
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.drawcan()
        self.generate_mage()
        self.isMage = True

    def drawcan(self):
        self.canvas = pg.Surface((402, 402))
        self.canvas.fill("#000000")
        for i in range(21):
            pg.draw.line(self.canvas, "#ffffff", (i * 20, 0), (i * 20, 400), 2)
            pg.draw.line(self.canvas, "#ffffff", (0, i*20), (400, i*20), 2)

    def drawloop(self):
        self.screen.fill("#200000")
        self.screen.blit(self.canvas, (0, 0))
        pg.display.update()

    def main_loop(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_SPACE:
                        if self.isMage:
                            self.solve_mage()
                        else:
                            self.drawcan()
                            self.generate_mage()
                            self.isMage = True
            self.drawloop()

    def surroundings(self, ind):
        res = []
        for i in (ind + 1, ind - 1):
            if i//20 == ind//20:
                res.append(i)
        for i in (ind + 20, ind - 20):
            if 0 <= i < 400:
                res.append(i)
        return res

    def generate_mage(self):
        self.maze = Root(0)
        self.build_tree(0, [], self.maze)

    def build_tree(self, parent, closed, parentTree):
        closed.append(parent)
        children = self.surroundings(parent)
        random.shuffle(children)
        for child in children:
            if child not in closed:
                row = parent // 20
                col = parent % 20
                if abs(parent - child) == 1:
                    pg.draw.line(self.canvas, "#000000", ((col + 1 * (child > parent)) * 20, row*20 + 2),
                                 ((col + 1 * (child>parent)) * 20, (row+1)*20-1), 2)
                else:
                    pg.draw.line(self.canvas, "#000000", (col * 20 + 2, (row + 1 * (child > parent)) * 20),
                                 ((col + 1) * 20 - 1, (row + 1 * (child > parent)) * 20), 2)
                self.drawloop()
                childTree = parentTree.addChild(child)
                self.build_tree(child, closed, childTree)

    def find_solution(self, root, endpoint, path):
        if root.value == endpoint:
            return path
        children = root.children()
        for child in children:
            result = self.find_solution(child, endpoint, path + f"/{child.value}")
            if result is not False:
                return result
        return False

    def solve_mage(self):
        path = self.find_solution(self.maze, self.endPoint, "0")
        if path is False:
            return
        path = path.split("/")
        for ind in path:
            pg.draw.circle(self.canvas, "#ffffff", ((int(ind)%20) * 20 + 10, (int(ind)//20) * 20 + 10), 3)
        for i in range(len(path)-1):
            s, e = int(path[i]), int(path[i+1])
            pg.draw.line(self.canvas, "#ffffff", ((s%20) * 20 + 10, (s//20) * 20 + 10),
                         ((e%20) * 20 + 10, (e//20) * 20 + 10), 1)
        self.isMage = False


pg.init()
screen = pg.display.set_mode((402, 402))
pg.display.set_caption("Mage Generator")
game = Game(screen)
game.main_loop()
