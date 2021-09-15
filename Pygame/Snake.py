import random
import pygame as pg
from string import ascii_letters, digits

class MainMenu():
    poscursor = 0
    def __init__(self, sup, canvas):
        self.sup = sup
        self.canvas = canvas
        self.midx = self.canvas.get_width()/2
        self.midy = self.canvas.get_height()/2
        self.font = pg.font.SysFont("comicsans", 50, False, False)
        self.options = ["Start", "Map Editor", "Options", "Records", "Quit"]
        self.textcanvas()

    def textcanvas(self):
        width = max([self.font.size(i)[0] for i in self.options])
        height = (self.font.get_height()+20 )* len(self.options)
        self.opcanvas = pg.Surface((width, height))
        opcanrec = self.opcanvas.get_rect()
        opcanrec.center = (self.midx, self.midy)
        self.opcanx, self.opcany = opcanrec.x, opcanrec.y

    def drawtext(self, canvas, text, x, y):
        text_box = self.font.render(text, 1, "#ffffff")
        text_box_rec = text_box.get_rect()
        text_box_rec.center = (x, y)
        canvas.blit(text_box, (text_box_rec.x, text_box_rec.y))

    def drawoptions(self):
        opcan_midx = self.opcanvas.get_width()/2
        fontsize = self.font.get_height()
        for i, option in enumerate(self.options):
            self.drawtext(self.opcanvas, option, opcan_midx, (fontsize+20)*i+fontsize/2)

    def drawcursor(self):
        fontsize = self.font.get_height()
        self.drawtext(self.canvas, "->", self.opcanx-50, self.opcany + self.poscursor * (fontsize+20)+fontsize/2)

    def drawloop(self):
        self.canvas.fill("#000020")
        self.opcanvas.fill("#000020")
        self.drawoptions()
        self.canvas.blit(self.opcanvas, (self.opcanx, self.opcany))
        self.drawcursor()

    def key_pressed(self, key):
        if key == "UP":
            self.poscursor -= 1
            self.poscursor %= len(self.options)
        elif key == "DOWN":
            self.poscursor += 1
            self.poscursor %= len(self.options)
        elif key == "RETURN":
            if self.options[self.poscursor] == "Quit":
                self.sup.running = False
            if self.options[self.poscursor] in self.sup.GAMEOBJ:
                self.sup.DIR += "/" + self.options[self.poscursor]
                self.poscursor = 0


class MapMenus():
    poscursor = 0
    drawOpStart = 0

    def __init__(self, sup, canvas):
        self.sup = sup
        self.canvas = canvas
        self.opcan1 = pg.Surface((200, 360))
        self.opcan2 = pg.Surface((200, 200))
        self.capacity = self.opcan1.get_height() // 40
        self.fontsize = 25
        self.font = pg.font.SysFont("comicsans", self.fontsize, False, False)

    #mapgenerate converts map code into map string
    def mapgenerate(self, code):
        code = code.split("-")
        res = ""
        for i in range(len(code)):
            res += str(i%2) * int(code[i])
        return res

    def drawtext(self, canvas, text, x, y):
        text_box = self.font.render(text, 1, "#ffffff")
        canvas.blit(text_box, (x, y))

    def drawoptions(self):
        for i in range(self.drawOpStart, self.drawOpStart+self.capacity):
            if i >= len(self.options):
                break
            self.drawtext(self.opcan1, self.options[i], 5, (self.fontsize + 15) * (i-self.drawOpStart) + 5)

    def drawselectedmap(self):
        map, playerPos = self.mapdata[self.options[self.poscursor]]
        playerPos = int(playerPos)
        for i in range(len(map)):
            if map[i] == "1":
                pg.draw.rect(self.opcan2, "#ffffff", ((i%20)*10+1, (i//20)*10+1, 8, 8))
        pg.draw.rect(self.opcan2, "#ff0000", ((playerPos % 20) * 10 + 1, (playerPos // 20) * 10 + 1, 8, 8))

    def highlightselection(self):
        pg.draw.rect(self.opcan1, "#0000ff", (0, (self.fontsize+15)*(self.poscursor-self.drawOpStart),
                                              self.opcan1.get_width(), self.fontsize))

    def drawslider(self):
        perOption = self.opcan1.get_height()/len(self.options)
        shownOps = min(self.capacity, len(self.options))
        pg.draw.rect(self.canvas, "#000000", (self.opcan1.get_width()+40, 20, 10, self.opcan1.get_height()))
        pg.draw.rect(self.canvas, "#ffffff", (self.opcan1.get_width()+40,
                                              self.drawOpStart * perOption+20,
                                              10, shownOps * perOption ))


class EditorMenu(MapMenus):
    def __init__(self, sup, canvas):
        super().__init__(sup, canvas)
        self.getoptions()

    def getoptions(self):
        self.mapdata = {}
        self.options = []
        for line in self.sup.savedata:
            if line.startswith("map-"):
                line = line[4:].split(",")
                self.mapdata[line[0].strip()] = (self.mapgenerate(line[1].strip()), line[2].strip())
                self.options.append(line[0].strip())
        self.mapdata["+Map"] = (self.mapgenerate("400"), 250)
        self.options.append("+Map")

    def key_pressed(self, key):
        if key == "UP":
            if self.poscursor > 0:
                self.poscursor -= 1
                if self.poscursor < self.drawOpStart:
                    self.drawOpStart -= 1
        elif key == "DOWN":
            if self.poscursor < len(self.options) - 1:
                self.poscursor += 1
                if self.poscursor == self.drawOpStart + self.capacity:
                    self.drawOpStart += 1
        elif key == "RETURN":
            self.sup.GAMEOBJ["GameBuilder"] = MapBuilder(self.sup, self.canvas, self.mapdata[self.options[self.poscursor]],
                                                         self.options[self.poscursor])
            self.sup.DIR += "/GameBuilder"
        elif key == "BACKSPACE":
            self.sup.gobackward()

    def drawloop(self):
        self.canvas.fill("#000020")
        self.opcan1.fill("#000000")
        self.highlightselection()
        self.drawoptions()
        self.drawslider()
        self.opcan2.fill("#000000")
        self.drawselectedmap()
        self.canvas.blit(self.opcan1, (40, 20))
        pg.draw.rect(self.canvas, "#0000ff", (self.canvas.get_width()-241, 19, 202, 202), 1)
        self.canvas.blit(self.opcan2, (self.canvas.get_width()-240, 20))


class LoadMapMenu(MapMenus):
    def __init__(self, sup, canvas):
        super().__init__(sup, canvas)
        self.getoptions()

    def getoptions(self):
        self.mapdata = {}
        self.options = []
        self.mapdata["Classic"] = (self.mapgenerate("400"), 250)
        self.options.append("Classic")
        for line in self.sup.savedata:
            if line.startswith("map-"):
                line = line[4:].split(",")
                self.mapdata[line[0].strip()] = (self.mapgenerate(line[1].strip()), line[2].strip())
                self.options.append(line[0].strip())

    def key_pressed(self, key):
        if key == "UP":
            if self.poscursor > 0:
                self.poscursor -= 1
                if self.poscursor < self.drawOpStart:
                    self.drawOpStart -= 1
        elif key == "DOWN":
            if self.poscursor < len(self.options) - 1:
                self.poscursor += 1
                if self.poscursor == self.drawOpStart + self.capacity:
                    self.drawOpStart += 1
        elif key == "RETURN":
            self.sup.GAMEOBJ["Game"] = GamePlay(self.sup, self.canvas, self.mapdata[self.options[self.poscursor]],
                                                         self.options[self.poscursor])
            self.sup.DIR += "/Game"
        elif key == "BACKSPACE":
            self.sup.gobackward()

    def drawloop(self):
        self.canvas.fill("#000039")
        self.opcan1.fill("#000000")
        self.highlightselection()
        self.drawoptions()
        self.drawslider()
        self.opcan2.fill("#000000")
        self.drawselectedmap()
        self.canvas.blit(self.opcan1, (40, 20))
        pg.draw.rect(self.canvas, "#0000ff", (self.canvas.get_width()-241, 19, 202, 202), 1)
        self.canvas.blit(self.opcan2, (self.canvas.get_width()-240, 20))


class MapBuilder():
    rows, cols = 20, 20
    color = ["#000000", "#ffffff", "#ff0000"]
    letterstring = ascii_letters + digits
    poscursor = 0
    iserror = False
    def __init__(self, sup, canvas, mapdata, mapname):
        if mapname != "+Map":
            self.mapname = mapname
        else:
            self.mapname = ""
        self.imapname = self.mapname
        self.sup = sup
        self.sup.takingMInput = True
        self.canvas = canvas
        self.editcan = pg.Surface((20 * self.cols, 20 * self.rows))
        self.rect_editcan = pg.Rect(0, 0, self.editcan.get_width(), self.editcan.get_height())
        self.fontsize = 25
        self.font = pg.font.SysFont("comicsans", self.fontsize, False, False)
        self.opcan = pg.Surface((200, 400))
        self.options = ["Change Name", "Save", "Exit"]
        self.writefontsize = 20
        self.writefont = pg.font.SysFont("comicsans", self.writefontsize, False, False)
        self.playerpos = (int(mapdata[1])%self.cols, int(mapdata[1])//self.cols)
        self.gridmap = self.decode(mapdata)

    def save(self):
        if len(self.mapname) == 0:
            self.iserror = True
            return
        for i in range(len(self.sup.savedata)):
            if not self.sup.savedata[i].startswith("map-"):
                continue
            line = self.sup.savedata[i][4:].split(",")
            if line[0].strip() == self.mapname and self.mapname != self.imapname:
                self.iserror = True
                return
            if line[0].strip() == self.imapname:
                replaceindex = i

        for i in range(self.rows):
            for j in range(self.cols):
                if self.gridmap[i][j] == 2:
                    playerPos = self.cols * i + j
        # If true it implies that the map already existed
        if len(self.imapname) > 0:
            self.sup.savedata[replaceindex] = f"map-{self.mapname},{self.encode()},{playerPos}\n"
        else:
            self.sup.savedata.append(f"map-{self.mapname},{self.encode()},{playerPos}\n")
        self.sup.saveandrebuild()
        self.imapname = self.mapname

    #Encode isn't the opposite of Decode, encode converts a map list into map code string and returns it
    #Returned code string doesn't carry player position
    def encode(self):
        stmap = ""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.gridmap[i][j] == 1:
                    stmap += "1"
                else:
                    stmap += "0"
        stmapcode = ""
        ind = 0
        check = 1
        while ind < len(stmap):
            check = 1 - check
            tot = 0
            while ind < len(stmap) and stmap[ind] == str(check):
                ind += 1
                tot += 1
            stmapcode += str(tot) + "-"
        stmapcode = stmapcode[:len(stmapcode)-1]
        return stmapcode

    def drawtext(self, canvas, font, text, x, y):
        text_box = font.render(text, 1, "#ffffff")
        text_box_rec = text_box.get_rect()
        text_box_rec.center = (x, y)
        canvas.blit(text_box, (text_box_rec.x, text_box_rec.y))

    def drawoptions(self):
        opcan_midx = self.opcan.get_width()/2
        subopy = (self.opcan.get_height() - len(self.options) * (self.fontsize)) / 2
        pg.draw.rect(self.opcan, "#000000", (opcan_midx - 75, subopy - 1.5 *self.writefontsize - 10,
                                             150, self.writefontsize))
        if self.sup.takinginput:
            pg.draw.rect(self.opcan, "#0000ff", (opcan_midx - 76, subopy - 1.5 * self.writefontsize - 11,
                                                 152, self.writefontsize+2), 1)
        if self.iserror:
            pg.draw.rect(self.opcan, "#ff0000", (opcan_midx - 76, subopy - 1.5 * self.writefontsize - 11,
                                                 152, self.writefontsize + 2), 1)
        self.drawtext(self.opcan, self.writefont, self.mapname, opcan_midx,
                      subopy - self.writefontsize - 10)
        for i, option in enumerate(self.options):
            self.drawtext(self.opcan, self.font, option, opcan_midx, self.fontsize * (i + 0.5) + subopy)

    def drawcursor(self):
        opcan_midx = self.opcan.get_width() / 2
        subopy = (self.opcan.get_height() - len(self.options) * (self.fontsize)) / 2
        self.drawtext(self.opcan, self.font, ">", opcan_midx - self.font.size(self.options[self.poscursor])[0]/2-10,
                      self.fontsize * (self.poscursor + 0.35) + subopy)

    #Decode isn't the opposite of encode, decode converts a [map string, playerpos] into map list and returns it
    def decode(self, mapdata):
        lst = []
        for i in range(self.rows):
            lst.append([int(mapdata[0][self.cols * i + j]) for j in range(self.cols)])
        pPos = (int(mapdata[1]) % self.cols, int(mapdata[1]) // self.cols)
        lst[pPos[1]][pPos[0]] = 2
        return lst

    def drawmap(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.gridmap[i][j] > 0:
                    pg.draw.rect(self.editcan, self.color[self.gridmap[i][j]], (j*20+1, i*20+1, 18, 18))

    def user_input(self, inp):
        if inp in self.letterstring and len(self.mapname) < 15:
            self.mapname += inp

    def key_pressed(self, key):
        if not self.sup.takinginput:
            if key == "UP":
                self.poscursor -= 1
                self.poscursor %= len(self.options)
            elif key == "DOWN":
                self.poscursor += 1
                self.poscursor %= len(self.options)
            elif key == "RETURN":
                if self.options[self.poscursor] == "Change Name":
                    self.sup.takinginput = True
                elif self.options[self.poscursor] == "Save":
                    self.save()
                elif self.options[self.poscursor] == "Exit":
                    self.sup.DIR = "MainMenu"
            elif key.startswith("MOUSE1"):
                key = key.split("-")
                self.mapwallconfig((int(key[1]), int(key[2])))
            elif key.startswith("MOUSE3"):
                key = key.split("-")
                self.mapplayerconfig((int(key[1]), int(key[2])))
        else:
            if key == "BACKSPACE":
                if len(self.mapname) > 0:
                    self.mapname = self.mapname[:len(self.mapname)-1]
            elif key == "RETURN":
                self.sup.takinginput = False

    def mapwallconfig(self, pos):
        if self.rect_editcan.collidepoint(pos):
            gridx = int((pos[0]-self.rect_editcan.x)//(self.editcan.get_width()/20))
            gridy = int((pos[1]-self.rect_editcan.y)//(self.editcan.get_height()/20))
            if self.gridmap[gridy][gridx] != 2:
                self.gridmap[gridy][gridx] = 1 - self.gridmap[gridy][gridx]

    def mapplayerconfig(self, pos):
        if self.rect_editcan.collidepoint(pos):
            gridx = int((pos[0] - self.rect_editcan.x) // (self.editcan.get_width() / 20))
            gridy = int((pos[1] - self.rect_editcan.y) // (self.editcan.get_height() / 20))
            if self.gridmap[gridy][gridx] == 0:
                self.gridmap[self.playerpos[1]][self.playerpos[0]] = 0
                self.gridmap[gridy][gridx] = 2
                self.playerpos = (gridx, gridy)

    def drawloop(self):
        self.canvas.fill("#000020")
        self.editcan.fill("#000000")
        self.drawmap()
        self.opcan.fill("#000020")
        self.drawoptions()
        self.drawcursor()
        self.canvas.blit(self.editcan, (self.rect_editcan.x, self.rect_editcan.y))
        self.canvas.blit(self.opcan, (self.editcan.get_width(), 0))


class GamePlay():
    rows, cols = 20, 20
    color = ["#000000", "#ffffff", "#ff0000"]
    gameover = False
    pause = False
    def __init__(self, sup, canvas, mapdata, mapname):
        self.score = 0
        self.font = pg.font.SysFont("comicsans", 30, 0, 0)
        self.sup = sup
        self.canvas = canvas
        self.speed = (0, 0)
        self.movecounter = 0
        self.framesPmove = self.sup.fps//(self.sup.level * 2)
        self.snakePos = [(int(mapdata[1]) % self.cols, int(mapdata[1]) // self.cols)]
        self.lstMap = self.mapdecode(mapdata)
        self.lstMapFree = self.free_poss()
        self.superFoodPos = None
        self.superFoodTimer = 0
        self.foodPos = self.get_food_pos()
        self.foodseaten = 0
        self.mapname = mapname
        self.gamecan = pg.Surface((400, 400))
        self.statcan = pg.Surface((200, 400))

    def drawtext(self, canvas, text, x, y):
        text_box = self.font.render(text, 1, "#ffffff")
        text_box_rec = text_box.get_rect()
        text_box_rec.center = (x, y)
        canvas.blit(text_box, (text_box_rec.x, text_box_rec.y))

    def mapdecode(self, mapdata):
        lst = []
        for i in range(self.rows):
            lst.append([int(mapdata[0][self.cols * i + j]) for j in range(self.cols)])
        return lst

    def move_next_position(self):
        nPos = ((self.snakePos[-1][0] + self.speed[0]) % self.cols,
                (self.snakePos[-1][1] + self.speed[1]) % self.rows)
        if self.lstMap[nPos[1]][nPos[0]] == 1:
            self.call_gameover()
            return
        if self.superFoodPos is not None and nPos == self.superFoodPos:
            self.eat_super_food()
        if nPos == self.foodPos:
            self.eat_food()
            self.foodseaten += 1
            if self.foodseaten % 5 == 0:
                self.create_super_food()
        else:
            if self.snakePos[0] not in self.lstMapFree:
                self.lstMapFree.append(self.snakePos[0])
            self.snakePos.pop(0)
        if nPos in self.snakePos:
            self.call_gameover()
            return
        self.snakePos.append(nPos)
        for i in self.lstMapFree:
            if i == nPos:
                self.lstMapFree.remove(nPos)
                break

    def get_food_pos(self):
        if len(self.lstMapFree) == 0:
            self.call_gameover()
            return
        if self.superFoodPos is not None:
            if len(self.lstMapFree) > 1:
                potPos = random.choice(self.lstMapFree)
                while potPos == self.superFoodPos:
                    potPos = random.choice(self.lstMapFree)
                return potPos
            else:
                self.superFoodPos = None
                self.superFoodTimer = 0
        return random.choice(self.lstMapFree)

    def create_super_food(self):
        if len(self.lstMapFree) < 2:
            return
        potPos = random.choice(self.lstMapFree)
        while potPos == self.foodPos:
            potPos = random.choice(self.lstMapFree)
        self.superFoodPos = potPos
        self.superFoodTimer = 50 * self.framesPmove

    def eat_super_food(self):
        self.score += self.sup.level * self.superFoodTimer
        self.superFoodPos = None
        self.superFoodTimer = 0

    def eat_food(self):
        self.score += self.sup.level
        self.foodPos = self.get_food_pos()

    def free_poss(self):
        lst = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.lstMap[i][j] == 0:
                    lst.append((j, i))
        for tup in self.snakePos:
            lst.remove(tup)
        return lst

    def call_gameover(self):
        self.gameover = True
        ishighscore = False
        for i in range(len(self.sup.records)):
            if self.sup.records[i] < self.score:
                self.sup.records.insert(i, self.score)
                self.sup.records.pop()
                self.sup.saverecord()
                ishighscore = True
                break
        if i == 0:
            self.gameover_text = f"Snakemaster: {self.score}"
        elif ishighscore:
            self.gameover_text = f"High Score: {self.score}"
        else:
            self.gameover_text = f"Your Score: {self.score}"

    def move_available(self, dx, dy):
        if len(self.snakePos) == 1 or self.snakePos[-2] != (self.snakePos[-1][0] + dx, self.snakePos[-1][1] + dy):
            return True
        return False

    def key_pressed(self, key):
        if not self.gameover:
            if key == "UP" and (self.speed[1] == 0 or len(self.snakePos) == 1):
                self.speed = (0, -1)
                if self.sup.controlType == 0:
                    self.move_next_position()
                    self.movecounter = 0
            elif key == "DOWN" and (self.speed[1] == 0 or len(self.snakePos) == 1):
                self.speed = (0, 1)
                if self.sup.controlType == 0:
                    self.move_next_position()
                    self.movecounter = 0
            elif key == "LEFT" and (self.speed[0] == 0 or len(self.snakePos) == 1):
                self.speed = (-1, 0)
                if self.sup.controlType == 0:
                    self.move_next_position()
                    self.movecounter = 0
            elif key == "RIGHT" and (self.speed[0] == 0 or len(self.snakePos) == 1):
                self.speed = (1, 0)
                if self.sup.controlType == 0:
                    self.move_next_position()
                    self.movecounter = 0
        if key == "BACKSPACE":
            self.sup.gobackward()
        if key == "SPACE":
            self.pause = not self.pause

    def drawboard(self):
        self.gamecan.fill("#000000")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.lstMap[i][j] == 1:
                    pg.draw.rect(self.gamecan, "#ffffff", (j*20+1, i*20+1, 18, 18))
        for i in range(len(self.snakePos)-1):
            pg.draw.rect(self.gamecan, "#a00000", (self.snakePos[i][0] * 20 + 1, self.snakePos[i][1] * 20 + 1, 18, 18))
        pg.draw.rect(self.gamecan, "#ff0000", (self.snakePos[-1][0] * 20 + 1, self.snakePos[-1][1] * 20 + 1, 18, 18))
        pg.draw.rect(self.gamecan, "#00ff00", (self.foodPos[0] * 20 + 5, self.foodPos[1] * 20 + 5, 10, 10))
        if self.superFoodPos is not None:
            if (self.superFoodTimer // 15) % 2 == 0:
                pg.draw.rect(self.gamecan, "#0000ff", (self.superFoodPos[0] * 20 + 5, self.superFoodPos[1] * 20 + 5,
                                                   10, 10))
            else:
                pg.draw.rect(self.gamecan, "#0020ff", (self.superFoodPos[0] * 20 + 1, self.superFoodPos[1] * 20 + 1,
                                                       18, 18))
        self.canvas.blit(self.gamecan, (0, 0))
        self.canvas.blit(self.statcan, (400, 0))

    def drawscore(self):
        self.statcan.fill("#000020")
        self.drawtext(self.statcan, f"Score: {self.score}", self.statcan.get_width()/2, self.statcan.get_height()/2)
        self.drawtext(self.statcan, f"{self.mapname}", self.statcan.get_width() / 2, 20)
        if self.superFoodPos is not None:
            tottime = 50 * self.framesPmove
            pg.draw.rect(self.statcan, "#0020ff", (20, 100, 10, 200*self.superFoodTimer/tottime))

    def drawloop(self):
        if self.pause:
            rec = pg.Rect(0, 0, 100, 30)
            rec.center = (self.canvas.get_width()/2, self.canvas.get_height()/2)
            pg.draw.rect(self.canvas, "#000080", rec)
            self.drawtext(self.canvas, "Paused", self.canvas.get_width()/2, self.canvas.get_height()/2)
            return
        self.canvas.fill("#000000")
        if self.gameover:
            self.drawtext(self.canvas, "Game Over! Press Backspace return",
                          self.canvas.get_width() / 2, self.canvas.get_height() / 2)
            self.drawtext(self.canvas, self.gameover_text, self.canvas.get_width() / 2,
                          self.canvas.get_height() / 2 + 30)
            return
        self.movecounter = (self.movecounter + 1)%self.framesPmove
        if self.movecounter == 0:
            self.move_next_position()
        if self.superFoodPos is not None:
            if self.superFoodTimer > 0:
                self.superFoodTimer -= 1
            else:
                self.superFoodPos = None
        self.drawboard()
        self.drawscore()


class RecordsMenu():
    def __init__(self, sup, canvas):
        self.sup = sup
        self.canvas = canvas
        self.records = self.sup.records
        self.topcan = pg.Surface((300, 400))
        self.botcan = pg.Surface((300, 400))
        self.firstfont = pg.font.SysFont("comicsans", 60, 1, 0)
        self.secondfont = pg.font.SysFont("comicsans", 50, 1, 0)
        self.thirdfont = pg.font.SysFont("comicsans", 40, 1, 0)
        self.deffont = pg.font.SysFont("comicsans", 30, 0, 0)

    def drawtext(self, font, canvas, text, color, x, y):
        text_box = font.render(text, 1, color)
        canvas.blit(text_box, (x, y))

    def drawtoplist(self):
        self.topcan.fill("#000020")
        self.drawtext(self.firstfont, self.topcan, "1) " + str(self.records[0]), "#e6be8a", 20, 100)
        self.drawtext(self.secondfont, self.topcan, "2) " + str(self.records[1]), "#c0c0c0", 20, 180)
        self.drawtext(self.thirdfont, self.topcan, "3) " + str(self.records[2]), "#cd7f32", 20, 250)

    def drawbotlist(self):
        self.botcan.fill("#000020")
        for i in range(3, 10):
            self.drawtext(self.deffont, self.botcan, str(i)+") "+str(self.records[i]), "#ffffff", 20, 20 + (i-3) * 50)

    def drawloop(self):
        self.canvas.fill("#000020")
        self.drawtoplist()
        self.drawbotlist()
        self.canvas.blit(self.topcan, (0, 0))
        self.canvas.blit(self.botcan, (300, 0))

    def key_pressed(self, key):
        if key == "BACKSPACE":
            self.sup.gobackward()

class OptionsMenu():
    poscursor = 0
    def __init__(self, sup, canvas):
        self.sup = sup
        self.canvas = canvas
        self.options = [f"Level: {self.sup.level}", f"Control Type: {self.sup.cTypes[self.sup.controlType]}"]
        self.opfont = pg.font.SysFont("comicsans", 40, 0, 0)
        self.opcan = pg.Surface((400, 50*len(self.options)))
        self.opcan_pos()
        self.get_details()
        self.detfont = pg.font.SysFont("comicsans", 20, 0, 0)
        self.detcan = pg.Surface((400, 40))

    def opcan_pos(self):
        opcanrec = self.opcan.get_rect()
        opcanrec.center = (self.canvas.get_width()/2, self.canvas.get_height()/2)
        self.opcanx, self.opcany = opcanrec.x, opcanrec.y

    def get_details(self):
        self.details = ["Game Difficulty", "Simple- Easier to control, Precise- Requires perfect timing"]

    def drawtext(self, font, canvas, text, x, y):
        text_box = font.render(text, 1, "#ffffff")
        text_box_rec = text_box.get_rect()
        text_box_rec.center = (x, y)
        canvas.blit(text_box, (text_box_rec.x, text_box_rec.y))

    def drawoptions(self):
        opcan_midx = self.opcan.get_width()/2
        fontsize = self.opfont.get_height()
        for i, option in enumerate(self.options):
            self.drawtext(self.opfont, self.opcan, option, opcan_midx, 50*i+fontsize/2)

    def drawcursor(self):
        fontsize = self.opfont.get_height()
        self.drawtext(self.opfont, self.canvas, "->", self.opcanx-50, self.opcany + self.poscursor * 50+fontsize/2)

    def drawdetails(self):
        self.drawtext(self.detfont, self.detcan, self.details[self.poscursor], self.detcan.get_width()/2,
                      self.detcan.get_height()/2)

    def drawloop(self):
        self.canvas.fill("#000020")
        self.opcan.fill("#000020")
        self.drawoptions()
        self.canvas.blit(self.opcan, (self.opcanx, self.opcany))
        self.drawcursor()
        self.detcan.fill("#000000")
        self.drawdetails()
        self.canvas.blit(self.detcan, ((self.canvas.get_width() - self.detcan.get_width())/2,
                                       self.opcany + self.opcan.get_height()))

    def save(self):
        for setting in self.options:
            if setting.startswith("Level:"):
                self.sup.level = int(setting.split(":")[1].strip())
            if setting.startswith("Control Type:"):
                self.sup.controlType = self.sup.cTypes.index(setting.split(":")[1].strip())
        self.sup.save_settings()

    def key_pressed(self, key):
        if key == "UP":
            self.poscursor -= 1
            self.poscursor %= len(self.options)
        elif key == "DOWN":
            self.poscursor += 1
            self.poscursor %= len(self.options)
        elif key == "LEFT":
            if self.options[self.poscursor].startswith("Level:"):
                oldval = int(self.options[self.poscursor].split(":")[1].strip())
                if oldval > 1:
                    self.options[self.poscursor] = "Level: " + str(oldval - 1)
            elif self.options[self.poscursor].startswith("Control Type:"):
                oldtype = self.options[self.poscursor].split(":")[1].strip()
                self.options[self.poscursor] = "Control Type: " + self.sup.cTypes[1 - self.sup.cTypes.index(oldtype)]
        elif key == "RIGHT":
            if self.options[self.poscursor].startswith("Level:"):
                oldval = int(self.options[self.poscursor].split(":")[1].strip())
                if oldval < 15:
                    self.options[self.poscursor] = "Level: " + str(oldval + 1)
            elif self.options[self.poscursor].startswith("Control Type:"):
                oldtype = self.options[self.poscursor].split(":")[1].strip()
                self.options[self.poscursor] = "Control Type: " + self.sup.cTypes[1 - self.sup.cTypes.index(oldtype)]
        elif key == "BACKSPACE":
            self.save()
            self.sup.gobackward()

class Game():
    DIR = "MainMenu"
    totalmaps = 0
    takinginput = False
    fps = 30
    cTypes = ["Simple", "Precise"]
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.canvas = pg.Surface((600, 400))
        try:
            with open("save.ske", "r") as fle:
                self.savedata = fle.readlines()
                for line in self.savedata:
                    if line.startswith("map-"):
                        self.totalmaps += 1
                    elif line.startswith("level-"):
                        self.level = int(line.split("-")[1].strip())
                    elif line.startswith("records-"):
                        self.records = []
                        line = line[8:].split(",")
                        for i in line:
                            self.records.append(int(i.strip()))
                    elif line.startswith("ctype-"):
                        self.controlType = int(line.split("-")[1].strip())
        except:
            with open("save.ske", "w") as fle:
                self.savedata = ["records-0,0,0,0,0,0,0,0,0,0\n", "level-4\n", "ctype-0\n"]
                self.records = [0] * 10
                self.level = 4
                self.controlType = 1
                for line in self.savedata:
                    fle.write(line)
        self.GAMEOBJ = {"MainMenu": MainMenu(self, self.canvas),
                   "Start": LoadMapMenu(self, self.canvas),
                   "Map Editor": EditorMenu(self, self.canvas),
                   "Game": MainMenu(self, self.canvas),
                   "Options": OptionsMenu(self, self.canvas),
                   "Records": RecordsMenu(self, self.canvas)}

    def saverecord(self):
        try:
            for i in range(len(self.savedata)):
                if self.savedata[i].startswith("records-"):
                    rline = i
                    break
            newrecord = "records-"
            for i in self.records:
                newrecord += str(i) + ","
            self.savedata[rline] = newrecord[:len(newrecord)-1] + "\n"
        except:
            newrecord = "records-"
            for i in self.records:
                newrecord += str(i) + ","
            self.savedata.insert(0, newrecord[:len(newrecord)-1] + "\n")
        self.saveandrebuild()

    def save_settings(self):
        for i in range(len(self.savedata)):
            if self.savedata[i].startswith("level-"):
                relevel = i
            if self.savedata[i].startswith("ctype-"):
                retype = i
        try:
            self.savedata[relevel] = "level-" + str(self.level) + "\n"
        except:
            self.savedata.append("level-" + str(self.level) + "\n")
        try:
            self.savedata[retype] = "ctype-"+ str(self.controlType) + "\n"
        except:
            self.savedata.append("ctype-"+ str(self.controlType) + "\n")


    def gobackward(self):
        for i in range(len(self.DIR)-1, -1, -1):
            if self.DIR[i] == "/":
                self.DIR = self.DIR[:i]
                break

    def saveandrebuild(self):
        with open("save.ske", "w") as fle:
            for line in self.savedata:
                fle.write(line)
        self.GAMEOBJ["Options"] = OptionsMenu(self, self.canvas)
        self.GAMEOBJ["Map Editor"] = EditorMenu(self, self.canvas)
        self.GAMEOBJ["Start"] = LoadMapMenu(self, self.canvas)

    def draw_screen(self):
        self.screen.fill("#000020")
        self.GAMEOBJ[self.DIR.split("/")[-1]].drawloop()
        self.screen.blit(self.canvas, (0, 0))
        pg.display.update()

    def game_loop(self):
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            for eve in pg.event.get():
                if eve.type == pg.QUIT:
                    self.running = False
                if eve.type == pg.MOUSEBUTTONDOWN:
                    if eve.button == 1:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("MOUSE1-"+ str(eve.pos[0])+ "-"+
                                                                          str(eve.pos[1]))
                    if eve.button == 3:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("MOUSE3-"+str(eve.pos[0])+ "-"+
                                                                          str(eve.pos[1]))
                if eve.type == pg.KEYDOWN:
                    if self.takinginput:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].user_input(eve.unicode)
                    if eve.key == pg.K_DOWN:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("DOWN")
                    if eve.key == pg.K_UP:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("UP")
                    if eve.key == pg.K_LEFT:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("LEFT")
                    if eve.key == pg.K_RIGHT:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("RIGHT")
                    if eve.key == pg.K_s:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("DOWN")
                    if eve.key == pg.K_w:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("UP")
                    if eve.key == pg.K_a:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("LEFT")
                    if eve.key == pg.K_d:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("RIGHT")
                    if eve.key == pg.K_RETURN:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("RETURN")
                    if eve.key == pg.K_BACKSPACE:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("BACKSPACE")
                    if eve.key == pg.K_SPACE:
                        self.GAMEOBJ[self.DIR.split("/")[-1]].key_pressed("SPACE")

            self.draw_screen()


pg.init()

screen = pg.display.set_mode((600, 400))
game = Game(screen)
game.game_loop()

