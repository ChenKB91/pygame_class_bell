# -*- coding: UTF-8 -*-
import csv
from datetime import*
import time
import random
# from ctypes import windll
import ctypes
from button_class import*

# Programmed by CKB, THE CHAIRMAN OF THE MIGHTY TANU TUVA SSR

# hide welcome message
# because it is annoying
import os
import sys
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    import pygame as pg

    # enable stdout
    sys.stdout = oldstdout

#                                        $$\                                  $$\
#                                        $$ |                                 $$ |
#  $$$$$$$\  $$$$$$$\ $$\    $$\       $$$$$$\    $$$$$$\  $$$$$$\   $$$$$$$\ $$$$$$$\
# $$  _____|$$  _____|\$$\  $$  |      \_$$  _|  $$  __$$\ \____$$\ $$  _____|$$  __$$\
# $$ /      \$$$$$$\   \$$\$$  /         $$ |    $$ |  \__|$$$$$$$ |\$$$$$$\  $$ |  $$ |
# $$ |       \____$$\   \$$$  /          $$ |$$\ $$ |     $$  __$$ | \____$$\ $$ |  $$ |
# \$$$$$$$\ $$$$$$$  |   \$  /           \$$$$  |$$ |     \$$$$$$$ |$$$$$$$  |$$ |  $$ |
#  \_______|\_______/     \_/             \____/ \__|      \_______|\_______/ \__|  \__|

schedule = []
playlist = []

if sys.platform == "win32" or "win64":
    musics_path = os.getcwd()[0:-4] + "musics\\"
    icon_path = os.getcwd() + "\\icon\\"
elif sys.platform == "darwin":
    musics_path = os.getcwd()[:-4] + "/musics/"
    icon_path = os.getcwd() + "/icon/"


def refresh_schedule():
    with open('schedule.csv') as schedule_csv:
        rows = csv.reader(schedule_csv)
        for row in rows:
            if row[0:3] != ["HOUR", "MINUTE", "MUSIC"]:

                schedule.append((int(row[0]), int(row[1])))

                if row[2][-3:] == "mp3":
                    playlist.append(row[2])

                elif row[2][-3:] == "csv":
                    with open(musics_path + row[2]) as prob_csv:
                        probability = 0
                        threshold = random.random()*100   # 0-100
                        prob_rows = csv.reader(prob_csv)
                        for prob_row in prob_rows:
                            if prob_row != ["MUSIC", "PROBABILITY (%)"]:
                                probability += float(prob_row[1])
                                if probability >= threshold:
                                    playlist.append(prob_row[0])
                                    break


refresh_schedule()
refresh_time = (23, 59)


#   $$\     $$\                                 $$\                                  $$\
#   $$ |    \__|                                $$ |                                 $$ |
# $$$$$$\   $$\ $$$$$$\$$$$\   $$$$$$\        $$$$$$\    $$$$$$\  $$$$$$\   $$$$$$$\ $$$$$$$\
# \_$$  _|  $$ |$$  _$$  _$$\ $$  __$$\       \_$$  _|  $$  __$$\ \____$$\ $$  _____|$$  __$$\
#   $$ |    $$ |$$ / $$ / $$ |$$$$$$$$ |        $$ |    $$ |  \__|$$$$$$$ |\$$$$$$\  $$ |  $$ |
#   $$ |$$\ $$ |$$ | $$ | $$ |$$   ____|        $$ |$$\ $$ |     $$  __$$ | \____$$\ $$ |  $$ |
#   \$$$$  |$$ |$$ | $$ | $$ |\$$$$$$$\         \$$$$  |$$ |     \$$$$$$$ |$$$$$$$  |$$ |  $$ |
#    \____/ \__|\__| \__| \__| \_______|         \____/ \__|      \_______|\_______/ \__|  \__|


previous_time = (datetime.now().hour, datetime.now().minute)
# musics_path = os.getcwd()[0:-4] + "musics\\"
# icon_path = os.getcwd() + "\\icon\\"


# pygame trash
pg.init()
width, height = 1080, 720
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Cyka Blyat")
bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill((0, 0, 0))
frame = pg.draw.rect(bg, (255, 255, 255), [0, 0, width, height], 10)
c = pg.time.Clock()
aji_ico = pg.image.load(icon_path + "alarm.png")
pg.display.set_icon(aji_ico)


# button

button_red = button(bg, [icon_path + "button_small.png", icon_path + "button_small_green.png"],
                    (163, height*3/4 - 57), ["",""])
button_red.pressed = True
button_comm = button(bg, [icon_path + "button_comm.png", icon_path + "button_comm_pressed.png"], 
                    (163, height*3/4 + 23), ["",""])


button_list = [button(bg, [icon_path + "buttonup.png", icon_path + "buttondown.png"], 
                    (680, height*3/4 - 57 + 65*i), ["%02d:%02d"%schedule[i],"%02d:%02d"%schedule[i]]) for i in range(len(schedule))]
button_list_y = 0
button_list_y_max = len(schedule)*65 - 160


# volume trash
volume_down = 0x0a
volume_up = 0x09
volume_mute = 0x08


# ring function
def play_ring(ring):
    r = random.random()
    if button_red.pressed == True:
        # for i in range(50):
        #     windll.user32.PostMessageA(
        #         windll.user32.GetForegroundWindow(), 0x319, 0, volume_down*0x10000)
        # for i in range(35):
        #     windll.user32.PostMessageA(
        #         windll.user32.GetForegroundWindow(), 0x319, 0, volume_up*0x10000)

        pg.mixer.init()
        pg.mixer.music.load(musics_path+ring)
        pg.mixer.music.play()

# soviet anthem init


# trash
running = True
fps = 25
seg = ':'
a = 0

time_color = (0, 255, 0)
# main loop
while running:
    a += 1
    now = datetime.now()
    if (now.hour, now.minute) != previous_time:
        if (now.hour, now.minute) in schedule:
            print("\rLatest bell time:   %d:%d" % (now.hour, now.minute))
            play_ring(playlist[schedule.index((now.hour, now.minute))])
        elif (now.hour, now.minute) == refresh_time:
            running = False

        previous_time = (now.hour, now.minute)

    if a % fps == 0:
        a = 0
        if seg == ':':
            seg = ' '
        else:
            seg = ':'

    if button_comm.pressed == True:
        time_color = (255, 0, 0)
    else:
        time_color = (0, 255, 0)

    bg.fill((0, 0, 0))

    # draw button
    button_red.draw()
    button_comm.draw()
    for i in button_list:
        if i.pos[1]+60 > height*3/4 - 63 and i.pos[1] < height*3/4 + 103:
            i.draw()
    [pg.draw.rect(bg, (0,0,0), [674, height*3/4 - 143 + i, 191, 80], 0) for i in [0,246]]
    button_list_box = pg.draw.rect(bg, (170,170,170), [674, height*3/4 - 63, 191, 166], 2)


    # clock
    frame = pg.draw.rect(bg, (255, 255, 255), [0, 0, width, height], 10)
    font = pg.font.SysFont("DSEG7 Modern Regular", 150)
    text1 = font.render("88:88:88", True, (30, 30, 30), None)
    text_rect1 = text1.get_rect(center=(width/2, height/2))
    bg.blit(text1, text_rect1)
    text = font.render("%02d%s%02d%s%02d" % (
        now.hour, seg, now.minute, seg, now.second), True, time_color, None)
    text_rect = text.get_rect(center=(width/2, height/2))
    bg.blit(text, text_rect)


    wrnfont = pg.font.SysFont("Lucida Console", 50)

    msg = wrnfont.render("Bell Ring", True, (170,170,170), None)
    bg.blit(msg, (250,height*3/4-45))

    msg = wrnfont.render("Communism", True, (170,170,170), None)
    bg.blit(msg, (250,height*3/4+35))


    screen.blit(bg, (0, 0))
    pg.display.update()

    c.tick(fps)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            button_red.detect(event.pos)

            signal = button_comm.detect(event.pos)
            if signal == "pressed":
                pg.mixer.init()
                pg.mixer.music.load(musics_path+"soviet_anthem.mp3")
                pg.mixer.music.play()
                # ctypes.windll.user32.SystemParametersInfoA(
                #     20, 0, icon_path + "aji_purple_propaganda_supernova.jpg", 0)

            elif signal == "unpressed":
                pg.mixer.music.stop()
                # ctypes.windll.user32.SystemParametersInfoA(
                #     20, 0, icon_path + "cabbage.jpg", 0) 


            if button_list_box.collidepoint(event.pos):
                [i.detect(event.pos) for i in button_list]


        elif event.type == pg.MOUSEBUTTONDOWN and event.button in [4,5]: 

            if button_list_box.collidepoint(event.pos):

                if event.button == 5 and button_list_y < button_list_y_max:
                    button_list_y += 20
                    if button_list_y > button_list_y_max:
                        button_list_y = button_list_y_max

                if event.button == 4 and button_list_y > 0:
                    button_list_y -= 20
                    if button_list_y < 0:
                        button_list_y = 0

                for i in range(len(button_list)):
                    button_list[i].pos = (680, height*3/4 - 57 + 65*i - button_list_y)