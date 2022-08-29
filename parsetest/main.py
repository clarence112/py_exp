import threading, time

enabled = True

class Player():
    frozen = False
    onGround = True
    item4 = False

    def freeze(self, args):
        state = args[0]
        condition = args[1]
        if condition == 0:
            pass
        elif condition == 1:
            if not(self.onGround):
                return(False)
        self.frozen = state
        print("Player frozen: " + str(self.frozen))
        return(True)

    def hasItem(self, args):
        if args[0] == 4:
            return self.item4
        return False

    def frozenGet(self):
        return(self.frozen)

    def frozenSet(state):
        self.frozen = state

player = Player()

class Actor():
    facing = 0
    onGround = True
    pos = [0, 0]
    name = ""

    def __init__(self, name):
        self.name = name

    def translate(self, args):
        if args[3] == 1:
            if self.onGround:
                npos = [self.pos[0] + args[0], self.pos[1] + args[1]]
                print(f"{self.name} moving! oldpos: {self.pos}, newpos: {npos}, duration: {args[2]}")
                pos = npos
                time.sleep(args[2])
        else:
            npos = [self.pos[0] + args[0], self.pos[1] + args[1]]
            print(f"{self.name} moving! oldpos: {self.pos}, newpos: {npos}, duration: {args[2]}")
            pos = npos
            time.sleep(args[2])

    def impulse(self, args):
        if args[2] == 1:
            if self.onGround:
                print(f"{self.name} getting a pysics impulse: {args[0]}, {args[1]}")
        else:
            print(f"{self.name} getting a pysics impulse: {args[0]}, {args[1]}")

    def lookLeft(self, args):
        if args[0] == 1:
            if self.onGround:
                print(f"{self.name} looking left")
                self.facing = 0
        else:
            print(f"{self.name} looking left")
            self.facing = 0

    def lookRight(self, args):
        if args[0] == 1:
            if self.onGround:
                print(f"{self.name} looking right")
                self.facing = 1
        else:
            print(f"{self.name} looking right")
            self.facing = 1

    def animate(self, args):
        if args[1] == 1:
            if self.onGround:
                print(f"{self.name} set animation to {args[0]}")
        else:
            print(f"{self.name} set animation to {args[0]}")

actor1 = Actor("Actor1")

def delay(args):
    print(f"Waiting {args[0]}")
    time.sleep(args[0])

def disable():
    global enabled
    enabled = False
    print("Cutscene disabled")

def dialogue(args):
    print(args[1] + ": " + args[0])
    if args[2] == 0:
        print("(waiting for button)")
        i = input()
    else:
        time.sleep(args[2])

tokens = {
    "true": ["constBool", True],
    "false": ["constBool", False],
    "dialogue": ["func", dialogue, 3],
    "disable": ["func", disable, 0],
    "delay": ["func", delay, 1],
    "PLAYER": ["dict", {
        "setFreeze": ["func", player.freeze, 2],
        "icon": ["constStr", "/path/to/player/icon"],
        "frozen": ["bool", player.frozenGet, player.frozenSet],
        "hasItem": ["func", player.hasItem, 1],
    }],
    "CONDITIONS": ["dict", {
       "always": ["constInt", 0],
       "onGround": ["constInt", 1], 
    }],
    "ACTOR1": ["dict", {
        "translate": ["func", actor1.translate, 4],
        "impulse": ["func", actor1.impulse, 3],
        "lookLeft": ["func", actor1.lookLeft, 1],
        "lookRight": ["func", actor1.lookRight, 1],
        "animate": ["func", actor1.animate, 2],
        "icon": ["constStr", "/path/to/actor1/icon"],
    }],
}

controls = ["if", "else", "together", "loop"]

specials = ["(", ")", "{", "}", " ", ",", "\""]

class parser(threading.Thread):

    pcounter = 0;
    lines = []

    def __init__(self, text):
        super().__init__()
        if type(text) is list:
            lhold = text
        else:
            lhold = text.split("\n")

        for h in range(len(lhold)):
            i = lhold[h]

            i = i.replace("\r", "")
            i = i.split(sep="#", maxsplit=1)[0]
            i = i.strip()

            lhold[h] = i

        lhold2 = []
        for i in lhold:
            if not(i == ""):
                lhold2.append(i)
        lhold = lhold2

        self.lines = lhold

    def _extract(self, line):
        extline = [""]
        i = 0
        while i < len(line):
            h = line[i]

            if h in specials:
                if h == ",":
                    extline.append("")
                elif h == "\"":
                    reader = i + 1
                    sstring = "\""
                    while reader < len(line):
                        j = line[reader]
                        if j == "\\":
                            reader += 1
                            j = line[reader]
                            if j == "r":
                                sstring = sstring + "\r"
                            else:
                                sstring = sstring + j
                        elif j == "\"":
                            break
                        else:
                            sstring = sstring + j
                        reader += 1
                    i = reader
                    extline[-1] = extline[-1] + sstring
                elif h == "(":
                    depth = 1
                    reader = i + 1
                    sstring = ""
                    for j in line[(i + 1):]:
                        if line[reader] == "(":
                            depth += 1
                        elif line[reader] == ")":
                            depth -= 1
                        sstring = sstring + line[reader]
                        if depth == 0:
                            extline.append(self._extract(sstring))
                            extline.append("")
                            i = reader
                            break
                        reader += 1
                else:
                    pass
            else:
                extline[-1] = extline[-1] + h
            i += 1
        if extline[-1] == "":
            del(extline[-1])
        return extline

    def _runner(self, dat):
        i = len(dat) - 1
        while i >= 0:
            h = dat[i]
            if type(h) is list:
                dat[i] = self._runner(h)
            elif type(h) is str:
                if h[0] == "\"":
                    dat[i] = h[1:]
                else:
                    try:
                        dat[i] = float(h)
                    except:
                        h = h.split(".")
                        j = tokens[h[0]]
                        if j[0] in ["constBool", "constStr", "constInt"]:
                            dat[i] = j[1]
                        elif j[0] == "dict":
                            k = j[1][h[1]]
                            if k[0] in ["constBool", "constStr", "constInt"]:
                                dat[i] = k[1]
                            elif k[0] == "dict":
                                raise(Exception)
                            elif k[0] == "func":
                                if k[2] == 0:
                                    dat[i] = k[1]()
                                else:
                                    if len(dat[i + 1]) == k[2]:
                                        dat[i] = k[1](dat[i + 1])
                            else:
                                raise(Exception)
                        elif j[0] == "func":
                            if j[2] == 0:
                                dat[i] = j[1]()
                            else:
                                if len(dat[i + 1]) == j[2]:
                                    dat[i] = j[1](dat[i + 1])
                        else:
                            raise(Exception)
            i -= 1
        return(dat)

    def _runSpecial(self, dat):
        print(dat)
        if dat[0] == "if":
            state = self._runner(dat[1])[0]
            depth = 1
            reader = self.pcounter + 1
            subprog0 = []
            subprog1 = []
            while depth > 0:
                if "}" in self.lines[reader]:
                    depth -= 1
                if ("{" in self.lines[reader]) and (depth > 0):
                    depth += 1
                if depth > 0:
                    subprog0.append(self.lines[reader])
                reader += 1
            if "else" in self.lines[reader - 1]:
                depth = 1
                while depth > 0:
                    if "}" in self.lines[reader]:
                        depth -= 1
                    if ("{" in self.lines[reader]) and (depth > 0):
                        depth += 1
                    if depth > 0:
                        subprog1.append(self.lines[reader])
                    reader += 1
            self.pcounter = reader - 1
            if state:
                p1 = parser(subprog0)
            else:
                p1 = parser(subprog1)
            p1.start()
            p1.join()
        elif dat[0] == "loop":
            num = int(self._runner(dat[1])[0])
            depth = 1
            reader = self.pcounter + 1
            subprog0 = []
            while depth > 0:
                if "}" in self.lines[reader]:
                    depth -= 1
                if ("{" in self.lines[reader]) and (depth > 0):
                    depth += 1
                if depth > 0:
                    subprog0.append(self.lines[reader])
                reader += 1
            if "else" in self.lines[reader - 1]:
                raise(Exception)
            self.pcounter = reader - 1
            subprog1 = []
            for i in range(num):
                for h in subprog0:
                    subprog1.append(h)
            p1 = parser(subprog1)
            p1.start()
            p1.join()
        elif dat[0] == "else":
            raise(Exception)
        elif dat[0] == "together":
            depth = 1
            reader = self.pcounter + 1
            subprog0 = []
            while depth > 0:
                if "}" in self.lines[reader]:
                    depth -= 1
                if ("{" in self.lines[reader]) and (depth > 0):
                    if depth == 1:
                        subprog0.append([])
                    depth += 1
                if depth > 0:
                    if (depth > 1) or ("}" in self.lines[reader]):
                        subprog0[-1].append(self.lines[reader])
                    else:
                        subprog0.append(self.lines[reader])
                reader += 1
            if "else" in self.lines[reader - 1]:
                raise(Exception)
            self.pcounter = reader - 1
            p = []
            for i in subprog0:
                p.append(parser(i))
            for i in p:
                i.start()
            for i in p:
                i.join()

    def run(self):
        running = True
        while running:
            curline = self.lines[self.pcounter]

            dat = self._extract(curline)

            if dat == []:
                pass
            elif dat[0] in controls:
                self._runSpecial(dat)
            else:
                self._runner(dat)

            self.pcounter += 1
            if self.pcounter > len(self.lines) - 1:
                running = False

f = open("testscript.txt")
ft = f.read()
f.close()

player.item4 = (input("Does player have item 4? (y/n)") == "y")

p0 = parser(ft)
p0.start()