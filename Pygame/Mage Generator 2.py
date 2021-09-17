import pygame as pg
import random

class Root():
    def __init__(self, value, parent = None):
        self.value = value
        self.child = []
        self.parent = parent

    def addChild(self, value):
        self.child.append(Root(value, self))
        return self.child[-1]

    def children(self):
        return self.child


class Game():
    isMage = False
    endPoint = 399
    rows, cols = 20, 20
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.drawcan()
        self.generate_mage()
        self.isMage = True

    def drawcan(self):
        self.start, self.end = None, None
        self.solveCan = None
        self.canvas = pg.Surface((402, 402))
        self.canvas.fill("#000000")
        for i in range(21):
            pg.draw.line(self.canvas, "#ffffff", (i * 20, 0), (i * 20, 400), 2)
            pg.draw.line(self.canvas, "#ffffff", (0, i*20), (400, i*20), 2)

    def drawloop(self):
        self.screen.fill("#200000")
        self.screen.blit(self.canvas, (0, 0))
        if self.solveCan is not None:
            self.screen.blit(self.solveCan, (0, 0))
        if self.start is not None:
            pg.draw.circle(self.screen, "#ffffff", ((self.start%self.cols) * 20 + 10, (self.start//self.cols) * 20 + 10)
                           , 5)
        if self.end is not None:
            pg.draw.rect(self.screen, "#ffffff", ((self.end % self.cols) * 20 + 5, (self.end // self.cols) * 20 + 5,
                                                 10, 10))
        pg.display.update()

    def main_loop(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.MOUSEBUTTONDOWN:
                    pos = self.cursor_grid(eve.pos[0], eve.pos[1])
                    if pos != -1:
                        if eve.button == 1:
                            if self.start == pos:
                                self.start = None
                            else:
                                self.start = pos
                            if self.start == self.end:
                                self.end = None
                        if eve.button == 3:
                            if self.end == pos:
                                self.end = None
                            else:
                                self.end = pos
                            if self.end == self.start:
                                self.start = None
                if eve.type == pg.KEYDOWN:
                    if eve.key == pg.K_SPACE:
                        self.drawcan()
                        self.generate_mage()
                        self.isMage = True
                    if eve.key == pg.K_RETURN:
                        if self.start is None or self.end is None:
                            self.solve_mage()
                        else:
                            self.find_path(self.start, self.end)
            self.drawloop()

    def cursor_grid(self, mx, my):
        col, row = mx//20, my//20
        if col >= self.cols or row >= self.rows:
            return -1
        else:
            return row * self.cols + col

    def find_path(self, start, end):
        if not self.isMage:
            return
        toStart = self.find_solution(self.maze, start, "0")
        toEnd = self.find_solution(self.maze, end, "0")
        if toStart is False or toEnd is False:
            return
        toStart = toStart.split("/")
        toEnd = toEnd.split("/")
        i = 0
        while (i < len(toStart) and i < len(toEnd)) and toStart[i] == toEnd[i]:
            i += 1
        path = []
        ii = len(toStart) - 1
        while ii >= i:
            path.append(toStart[ii])
            ii -= 1
        path.append(toStart[i-1])
        ii = i
        while ii < len(toEnd):
            path.append(toEnd[ii])
            ii += 1
        self.solveCan = pg.Surface((402, 402), pg.SRCALPHA)
        for ind in path:
            pg.draw.circle(self.solveCan, "#ffffff", ((int(ind)%20) * 20 + 10, (int(ind)//20) * 20 + 10), 3)
        for i in range(len(path)-1):
            s, e = int(path[i]), int(path[i+1])
            pg.draw.line(self.solveCan, "#ffffff", ((s%20) * 20 + 10, (s//20) * 20 + 10),
                         ((e%20) * 20 + 10, (e//20) * 20 + 10), 1)

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
                #pg.time.delay(10)
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
        if not self.isMage:
            return
        self.solveCan = pg.Surface((402, 402), pg.SRCALPHA)
        path = self.find_solution(self.maze, self.endPoint, "0")
        if path is False:
            return
        path = path.split("/")
        for ind in path:
            pg.draw.circle(self.solveCan, "#ffffff", ((int(ind)%20) * 20 + 10, (int(ind)//20) * 20 + 10), 3)
        for i in range(len(path)-1):
            s, e = int(path[i]), int(path[i+1])
            pg.draw.line(self.solveCan, "#ffffff", ((s%20) * 20 + 10, (s//20) * 20 + 10),
                         ((e%20) * 20 + 10, (e//20) * 20 + 10), 1)



pg.init()
screen = pg.display.set_mode((402, 402))
pg.display.set_caption("Mage Generator")
game = Game(screen)
game.main_loop()
