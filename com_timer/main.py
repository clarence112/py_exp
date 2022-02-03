import win32gui, wmi, win32process
c = wmi.WMI()

import pygame, sys
pygame.init()

from ctypes import Structure, windll, c_uint, sizeof, byref

def get_app_name():
    try:
        _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            return exe
    except:
        return None

print(get_app_name())

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return float(millis / 1000.0)

def recalcRates():
    global rate1
    global rate2
    global changeover
    rate1 = (rate1Readable / 60) / 60
    rate2 = (rate2Readable / 60) / 60
    changeover = (changeoverHours * 60) * 60

#price in cents to reduce the effect of floating point errors
rate1Readable = 1000
rate2Readable = 1500
changeoverHours = 1

recalcRates()

timeout = 10
focus = "Gravit Designer.exe"

workTimer = 0
price = 0

dispsurf = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pay Timer")
clock = pygame.time.Clock()

bigfont = pygame.font.Font("OpenSans-SemiBold.ttf", 32)

while True:
    delta = (clock.tick(1) / 1000)
    idle = get_idle_duration()

    dispsurf.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    if (idle < timeout):
        if focus == get_app_name():
            workTimer += delta
            if workTimer < changeover:
                price += (delta * rate1)
                dispsurf.blit(bigfont.render("rate 1", False, (255, 255, 255)), (50, 200))
            else:
                price += (delta * rate2)
                dispsurf.blit(bigfont.render("rate 2", False, (255, 255, 255)), (50, 200))

    dispsurf.blit(bigfont.render(str(idle), False, (255, 255, 255)), (50, 50))
    dispsurf.blit(bigfont.render("$" + str(round(price) / 100), False, (255, 255, 255)), (50, 100))
    dispsurf.blit(bigfont.render(str(workTimer), False, (255, 255, 255)), (50, 150))

    pygame.display.flip()