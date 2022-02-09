import pygame
import pygame.midi
import serial
import serial.tools.list_ports

pygame.init()
pygame.midi.init()

h = pygame.display.set_mode((100, 100))
stage = 0
selection = 0
disps = [pygame.image.load("mll-1.png"),
         pygame.image.load("mll-2.png"),
         pygame.image.load("mll-3.png"),
         pygame.image.load("mll-4.png")]

devlist = []
for i in range(pygame.midi.get_count()):
    if pygame.midi.get_device_info(i)[2] == 1:
        j = list(pygame.midi.get_device_info(i))
        j.append(i)
        devlist.append(j)

h.blit(disps[3], (0, 0))
pygame.display.flip()

comlist = serial.tools.list_ports.comports()
    
font = pygame.font.Font(pygame.font.get_default_font(), 8)

eventlog = ["", "", "", "", "", "", ""]

def main():
    global eventlog
    global stage
    h.blit(disps[0], (0, 0))
    for i in range(len(eventlog)):
        h.blit(font.render(eventlog[i], False, (169, 169, 169)), (2, 23 + (i * 10)))
        
    pygame.display.flip()
    for i in pygame.event.get():
        if i.type == 12:
            input.close()
            ser.close()
            quit()
        elif i.type == 5:
            if (i.pos[0] >= 53) and (i.pos[1] >= 8) and (i.pos[1] <= 19):
                input.close()
                ser.close()
                stage = 0
                return()
    while input.poll():
        i = input.read(1)[0][0]
        eventlog.append(str(i))
        del(eventlog[0])
        if (i[2] > 0) and (i[1] > 35) and (97 > i[1]):
            ser.write(int((i[1]-36)*3).to_bytes(1, byteorder="little"))

def conf0():
    global selection
    global stage
    h.blit(disps[1], (0, 0))
    h.blit(font.render(str(selection + 1) + " of " + str(len(devlist)), False, (169, 169, 169)), (2, 33))
    h.blit(font.render(devlist[selection][0], False, (169, 169, 169)), (2, 50))
    h.blit(font.render(devlist[selection][1], False, (169, 169, 169)), (2, 60))
    pygame.display.flip()
    for i in pygame.event.get():
        if i.type == 12:
            quit()
        elif i.type == 5:
            if (i.pos[0] >= 41) and (i.pos[1] >= 20) and (i.pos[1] <= 31):
                if selection > 0:
                    selection -= 1
            elif (i.pos[1] >= 32) and (i.pos[1] <= 87):
                stage += 1
            elif (i.pos[1] >= 88):
                if selection < (len(devlist) - 1):
                    selection += 1

def conf1():
    global input
    global selection
    global stage
    input = pygame.midi.Input(devlist[selection][5])
    selection = 0
    stage += 1

def conf2():
    global selection
    global stage
    h.blit(disps[2], (0, 0))
    h.blit(font.render(str(selection + 1) + " of " + str(len(comlist)), False, (169, 169, 169)), (2, 33))
    h.blit(font.render(comlist[selection].device, False, (169, 169, 169)), (2, 50))
    h.blit(font.render(comlist[selection].name, False, (169, 169, 169)), (2, 60))
    pygame.display.flip()
    for i in pygame.event.get():
        if i.type == 12:
            input.close()
            quit()
        elif i.type == 5:
            if (i.pos[0] >= 41) and (i.pos[0] <= 99) and (i.pos[1] >= 20) and (i.pos[1] <= 31):
                if selection > 0:
                    selection -= 1
            elif (i.pos[1] >= 32) and (i.pos[1] <= 87):
                stage += 1
            elif (i.pos[1] >= 88):
                if selection < (len(comlist) - 1):
                    selection += 1

def conf3():
    global ser
    global selection
    global stage
    ser = serial.Serial(comlist[selection].device, 9600)
    stage += 1
    selection = 0
    
while True:
    if stage == 0:
        conf0()
    if stage == 1:
        conf1()
    if stage == 2:
        conf2()
    if stage == 3:
        conf3()
    if stage == 4:
        main()