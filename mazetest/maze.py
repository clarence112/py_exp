import pygame, random

feild = []
next = []
last = None
for i in range(100):
    a = []
    for h in range(100):
        a.append(0)
    feild.append(a)

class tile():
    def __init__(self, pos):
        self.pos = pos
        self.stage = 0
        self.test()
        global last
        last = self

    def test(self):
        global feild
        global next
        if (self.pos[0] - 1) < 0:
            self.l = 0
        elif feild[self.pos[0] - 1][self.pos[1]] == 0:
            self.l = random.randint(0, 1)
            if self.l == 1:
                next.append((self.pos[0] - 1, self.pos[1]))
        else:
            self.l = feild[self.pos[0] - 1][self.pos[1]].r

        if (self.pos[0] + 1) > 99:
            self.r = 0
        elif feild[self.pos[0] - 1][self.pos[1]] == 0:
            self.r = random.randint(0, 1)
            if self.r == 1:
                next.append((self.pos[0] + 1, self.pos[1]))
        else:
            self.r = feild[self.pos[0] - 1][self.pos[1]].l

        if (self.pos[1] - 1) < 0:
            self.u = 0
        elif feild[self.pos[0] - 1][self.pos[1]] == 0:
            self.u = random.randint(0, 1)
            if self.u == 1:
                next.append((self.pos[0], self.pos[1] - 1))
        else:
            self.u = feild[self.pos[0] - 1][self.pos[1]].d

        if (self.pos[1] + 1) > 99:
            self.d = 0
        elif feild[self.pos[0] - 1][self.pos[1]] == 0:
            self.d = random.randint(0, 1)
            if self.d == 1:
                next.append((self.pos[0], self.pos[1] + 1))
        else:
            self.d = feild[self.pos[0] - 1][self.pos[1]].u

    def draw(self):
        global screen
        self.stage += 1
        x = self.pos[0] * 3
        y = self.pos[1] * 3 
        if self.stage == 1:
            screen.set_at((x + 1, y + 1), (0, 0, 0))
        elif self.stage == 2:
            if self.l == 1:
                screen.set_at((x, y + 1), (0, 0, 0))
        elif self.stage == 3:
            if self.r == 1:
                screen.set_at((x + 2, y + 1), (0, 0, 0))
        elif self.stage == 4:
            if self.u == 1:
                screen.set_at((x + 1, y), (0, 0, 0))
        elif self.stage == 5:
            if self.d == 1:
                screen.set_at((x + 1, y + 2), (0, 0, 0))
            return(True)
        return(False)

screen = pygame.display.set_mode((300, 300))
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
feild[49][49] = tile((49, 49))
feild[49][48] = tile((49, 48))
pygame.display.flip()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit(0)

    if last.draw():
        pass
#        if len(next) > 0:
#            i = next.pop()
#            feild[i[0]][i[1]] = tile(i)

    pygame.display.flip()