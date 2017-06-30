import urllib.request
import urllib.parse
import re
import random

# The code also work for ahead levels: Dungeon Master and Cavern Master
# after you modify the following `name` to 'index.php?' / 'cavern.php?'
name = 'cave.php?'
di = ["West", "North", "East", "South"]
dx = [0, -1, 0, 1]  # delta x for di
dy = [-1, 0, 1, 0]  # delta y for di

class Cavern:
    url = "http://www.hacker.org/challenge/misc/d/"
    cookie = "......"
    header = {'Cookie': cookie}
    map = []            # map
    op = []             # option
    ops = 0             # num of option
    potion = 0          # num of potion
    level = 0           # Dungeon Level
    lv = 0              # level of me
    hp = 0              # hit points
    exp = 0             # EXP
    cnt = 0             # total step
    maxlevel = 0        # max Dungeon Level
    avgstep = 1000000   # average step per level
    weapon = [0, 0]     # level of weapon
    res = 'NULL'        # responce of website
    dire = 0            # diretion
    findit = False      # found downstair
    ct = 10             # core centre is (ct, ct)
    px = py = ct        # positon (px, py)
    minx = miny = ct    # minimum of px & py
    maxx = maxy = ct    # maximum of px & py
    stepcnt = '0'

    def __init__(self):
        # self.init_map()
        self.act()

    def init_map(self):
        self.px = self.py = self.ct
        self.minx = self.miny = self.ct
        self.maxx = self.maxy = self.ct
        self.map = []
        for i in range(self.ct << 1):
            self.map.append(['x'] * (self.ct << 1))

    def print_map(self):
        for i in range(self.minx - 1, self.maxx + 2):
            print("".join(self.map[i][self.miny - 1: self.maxy + 2]))

    def weapon_parser(self, weainfo):  # transfer the weapon name to [weapon.level, weapon.effect]
        if '+' not in weainfo:
            return [0, 0]
        wea = re.findall('Level\s(\d*?)\s\w*?\s\+(\d*?)$', weainfo)
        if wea and len(wea[0]) == 2:
            return [int(wea[0][0]), int(wea[0][1])]
        if not wea:
            wea = re.findall('Level\s(\d*?)\s\w*?$', weainfo)
            if wea:
                return [int(wea[0]), 0]
            return [0, 0]

    def page(self, d=0, attack=False):
        if d > 0:
            url1 = self.url + self.op[d - 1][0].replace('"', '')
            if self.op[d - 1][1] in di:
                print("[Chose] %s" % self.op[d - 1][1])
                '''
                # create a map just for watching
                # 
                dd = di.index(self.op[d - 1][1])
                self.map[self.px][self.py] = self.stepcnt
                self.stepcnt = chr((ord(self.stepcnt) - 47) % 10 + 48)
                self.px += dx[dd]
                self.py += dy[dd]
                self.map[self.px][self.py] = 'O'
                self.minx = min(self.minx, self.px)
                self.maxx = max(self.maxx, self.px)
                self.miny = min(self.miny, self.py)
                self.maxy = max(self.maxy, self.py)'''
        else:
            url1 = self.url + name
        req = urllib.request.Request(url=url1, headers=self.header)
        res = urllib.request.urlopen(req)
        self.res = res.read().decode(errors='replace')

        # Meet the boss
        if "stands before you" in self.res:
            print(self.res)
            su = input('Meet the boss!!!\n\n\n')

        if "try again" in self.res or self.cnt > 1920:
            print("\n\n*** Died. Restart.")
            self.act()
            raise Exception

        # Information Update
        self.op = re.findall('<a\shref=(.*?)>(.*?)</a>', self.res)
        self.ops = len(self.op)
        if attack:
            p = re.findall('<td>(.*?)</td>', self.res)
            self.hp = int(p[1])
        else:
            mystep = re.findall("Time\sunderground:\s(\d*?)<br>", self.res)
            if mystep:
                self.cnt = int(mystep[0])
            self.level = int(re.findall('<h2>Dungeon\sLevel\s(\d*?)</h2><p>', self.res)[0])

    def print_option(self):
        print("Choose:")
        for i in range(self.ops):
            print(" [%d] %s %s" % (i + 1, self.op[i][1], self.op[i][0].replace(name, '')))
        print()

    def pick_tres(self):
        x = 0
        for i in range(self.ops):
            if 'tres' in self.op[i][0]:
                x = i
                break
        if r'<a href="' + name + 'tres=1">Level ' in self.res:
            # Weapon
            wea = re.findall('Pick\sup\streasure.*?>(.*?)</a><br></h2>', self.res)[0]
            newwea = self.weapon_parser(wea)
            if wea and newwea > self.weapon:  # strategy for picking weapon
                self.page(x + 1)
        else:
            # Potion
            po = re.findall('Pick\sup\streasure.*?>(.*?)\spotion.*?</a><br>', self.res)
            if self.potion < 3 and ("Magenta" in po or "Turquoise" in po):  # strategy for picking potion 
                self.page(x + 1)

    def fight(self):
        print('Fighting...', end='')
        if self.potion > 0 and (self.level > self.weapon[0] or self.weapon[1] < 2):  # strategy for using potion 
            self.page(random.randint(1, self.potion), attack=True)
        print(' HP: ', end='')
        while True:
            if 'You killed the monster!' in self.res:
                break
            print('%d' % self.hp, end=" ")
            self.page(self.ops, attack=True)
        print()
        if "Pick up treasure" in self.res:
            self.pick_tres()
        p = re.findall('<td>(.*?)</td>', self.res)
        self.lv = int(p[0])
        self.exp = int(p[2])
        self.weapon = self.weapon_parser(p[3])

    def act(self, d=0):
        self.page(d)
        # attack
        if 'monster' in self.res:
            print("===============\nLevel %s" % self.level)
            print("Step: {}   Avg step: {}   Max level: {}".format(self.cnt, self.avgstep, self.maxlevel))
            inve = re.findall('>(.*?)\spotion\s(.*?)</a><br>', self.res)
            self.potion = len(inve)
            self.fight()
            print("Lv.{}   Exp: {}   Weapon: {}   Potion: {}".format(self.lv, self.exp, self.weapon, self.potion))
            # self.print_map()
            print()

    def downstair(self):
        self.findit = False
        self.act(self.ops)
        self.maxlevel = max(self.maxlevel, self.level)
        if self.level > 0:
            self.avgstep = self.cnt / self.level
        # self.init_map()

    def found(self):  # found "Down Stairs" and hang around it
        for i in range(self.ops):
            if self.op[i][1] in di:
                self.dire = di.index(self.op[i][1])
                break
        while True:
            if self.level + 2 < self.lv or (self.level + 1 < self.lv and self.level < 3) or self.level > 23: # Nekomata 
                if "m=d" in self.op[self.ops - 1][0]:
                    if self.level < 24 or self.cnt > 1840:
                        self.downstair()
                        return
            self.dire = (self.dire + 2) % 4
            for i in range(self.ops):
                if di[self.dire] == self.op[i][1]:
                    self.act(i + 1)
                    break

    def go_straight(self, direction):  # go along the direction
        flag = True
        while flag:
            if "m=d" in self.op[self.ops - 1][0]:
                self.found()
                return True
            flag = False
            for i in range(self.ops):
                if direction == self.op[i][1]:
                    self.act(i + 1)
                    flag = True
                    break
        return False

    def get_dire_num(self):  # get a list of four directions
        num = [0, 0, 0, 0]
        for x in self.op:
            if x[1] in di:
                num[di.index(x[1])] = 1
        return num


proxy_support = urllib.request.ProxyHandler({'http': 'localhost:1080'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
ca = Cavern()

while True:
    try:
        if ca.op[0][1] == 'try again' or ca.cnt > 1920:
            ca.op[0] = (name + 'reset=1', 'try again')
            ca.act(1)
            continue

        nod = ca.get_dire_num()
        sumnod = sum(nod)
        #        in the middle -> left border
        # lower border(middle) -> bottom left corner
        # upper border(middle) -> top left corner
        if sumnod == 4 or (sumnod == 3 and nod[0] == 1):
            if ca.go_straight('West'):
                continue
            nod = ca.get_dire_num()
            sumnod = sum(nod)

        #  left border -> top left corner
        if sumnod == 3:
            if ca.go_straight('North'):
                continue
            nod = ca.get_dire_num()
            sumnod = sum(nod)

        # top left corner or bottom left corner
        yd = "North" if nod[1] == 1 else "South"
        xd = 2 if nod[2] == 1 else 0
        while True:
            if ca.go_straight(di[xd]):
                break
            xd = (xd + 2) % 4
            for i in range(ca.ops):
                if yd == ca.op[i][1]:
                    ca.act(i + 1)
                    break
    except:
        pass
