# -*- coding: UTF-8 -*-
import csv
from datetime import*
import time
import random
import sys
if sys.platform == "win32" or "win64":
    import ctypes
import Tkinter, tkFileDialog
from button_class import*

# Programmed by CKB, THE CHAIRMAN OF THE MIGHTY TANU TUVA SSR

# hide welcome message cuz it is annoying
import os

with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame as pg
    sys.stdout = oldstdout

schedule = []
active = []
playlist = []

if sys.platform == "win32" or "win64":
    musics_path = os.getcwd()[0:-4] + "musics\\"
    icon_path = os.getcwd() + "\\icon\\"
elif sys.platform == "darwin":
    musics_path = os.getcwd()[:-4] + "/musics/"
    icon_path = os.getcwd() + "/icon/"

def load_schedule():
    with open('schedule.csv') as schedule_csv:
        rows = csv.reader(schedule_csv)
        for row in rows:
            if row[0:4] != ["HOUR", "MINUTE", "MUSIC","NOT_ACTIVE"]:

                schedule.append((int(row[0]), int(row[1])))
                if row[3] == "True":    
                    active.append(True)
                else:
                    active.append(False)

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

def write_schedule():
    with open('schedule.csv', 'w') as schedule_csv:
        writer = csv.writer(schedule_csv)
        writer.writerow(["HOUR", "MINUTE", "MUSIC","NOT_ACTIVE"])
        for i in range(len(schedule)):
            writer.writerow([schedule[i][0], schedule[i][1], playlist[i], button_list[i].pressed])

load_schedule()

previous_time = (datetime.now().hour, datetime.now().minute)

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
                    (163, height*3/4 - 57), [["",""]])
button_red.pressed = True
button_comm = button(bg, [icon_path + "button_comm.png", icon_path + "button_comm_pressed.png"], 
                    (163, height*3/4 + 23), [["",""]])

def button_list_inital():
    global button_list, button_delete, button_list_y, button_list_y_max

    button_list = [button(bg, [icon_path + "unpressed.png", icon_path + "pressed.png"], 
                        (680, height*3/4 - 57 + 65*i), [["%02d:%02d"%schedule[i],"%02d:%02d"%schedule[i]], [playlist[i],playlist[i]]],
                        font = ["Calibri","Lucida Console"], font_size = [40,17], text_pos = [(0,-7),(0,15)], 
                        font_color=[[(40,40,40),(100,100,100)],[(40,40,40),(100,100,100)]], pressed=active[i]) for i in range(len(schedule))]
    button_list.append(button(bg, [icon_path + "unpressed_plus.png", icon_path + "pressed_plus.png"], 
                        (680, height*3/4 - 57 + 65*len(button_list)), [["",""]], font = ["Calibri"], font_size = [80], text_pos = [(0,0)]))

    button_delete = [button(surface=bg, image_path=[icon_path + "delete.png", icon_path + "delete.png"], 
                        pos=(845, height*3/4 - 53 + 65*i), text=[["",""]]) for i in range(len(schedule))]

    button_list_y = 0
    button_list_y_max = len(button_list)*65 - 160


button_list_inital()

console = False
def set_time_console_initial():
    global icon_colon, box_hour, box_minute, box_browse, button_browse, button_save, button_cancel, focus
    
    icon_colon = button(bg, [icon_path + "console_time_colon.png", icon_path + "console_time_colon.png"],
                    (width/2-35,height/2-80), [[":",":"]], font=["DSEG7 Modern Regular"], font_size=[100], font_color=[[(0,0,200),(0,0,200)]])
    box_hour = button(bg, [icon_path + "console_time_up.png", icon_path + "console_time_down.png"],
                    (width/2-197,height/2-80), [["88","88"],["!!","!!"]], font=["DSEG7 Modern Regular","DSEG7 Modern Regular"], font_size=[100,100], font_color=[[(150,150,150),(150,150,150)],[(0,0,200),(0,0,160)]], text_pos=[[0,0],[0,0]])
    box_minute = button(bg, [icon_path + "console_time_up.png", icon_path + "console_time_down.png"],
                    (width/2+15,height/2-80), [["88","88"],["!!","!!"]], font=["DSEG7 Modern Regular","DSEG7 Modern Regular"], font_size=[100,100], font_color=[[(150,150,150),(150,150,150)],[(0,0,200),(0,0,160)]], text_pos=[[0,0],[0,0]])
    box_browse = button(bg, [icon_path + "browse_up.png", icon_path + "browse_up.png"],
                    (width/2-250,height/2+60), [["bell.mp3","bell.mp3"]], font_size=[30], offset="left", font_color=[[(80,80,80),(40,40,40)]])
    button_browse = button(bg, [icon_path + "console_up.png", icon_path + "console_down.png"],
                    (width/2+120,height/2+60), [["Browse","Browse"]], font_size=[30])
    button_save = button(bg, [icon_path + "console_up.png", icon_path + "console_down.png"],
                    (width/2+10,height*3/4-55), [["Save","Save"]], font_size=[30])
    button_cancel = button(bg, [icon_path + "console_up.png", icon_path + "console_down.png"],
                    (width/2-130,height*3/4-55), [["Cancel","Cancel"]], font_size=[30])
    focus = "console"

def set_time_console_draw():
    background = pg.draw.rect(bg, (180,180,180), [width/4,height/4,width/2,height/2], 0)
    icon_colon.draw()
    box_hour.draw()
    box_minute.draw()
    box_browse.draw()
    button_browse.draw()
    button_save.draw()
    button_cancel.draw()

    font = pg.font.SysFont("Lucida console", 50)
    text1 = font.render("Add New Ring", True, (30, 30, 30), None)
    text_rect1 = text1.get_rect(center=(width/2, height/4+50))

    bg.blit(text1, text_rect1)


def set_time_console_detect():
    global focus, console
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        focus = "console"
        box_hour.pressed = False
        box_minute.pressed = False
        box_browse.pressed = False
        signal = box_hour.detect(event.pos)
        if signal == "pressed":
            focus = "hour"
            for i in [0,1]:
                box_hour.text[1][i] = "!!"

        signal = box_minute.detect(event.pos)
        if signal == "pressed":
            focus = "minute"
            for i in [0,1]:
                box_minute.text[1][i] = "!!"

        signal = box_browse.detect(event.pos)
        if signal == "pressed":
            focus = "browse"
        
        signal = button_browse.detect(event.pos)

        if signal == "pressed":

            button_browse.draw()
            screen.blit(bg, (0, 0))
            pg.display.update()
            time.sleep(0.08)

            root = Tkinter.Tk()
            root.withdraw()
            filename = tkFileDialog.askopenfilename(title = "Browse your .mp3 file", filetypes=(("mp3 files", "*.mp3"), ("All files", "*.*") ))
            filename = filename.split('/')[-1]
            for i in [0,1]:
                box_browse.text[0][i] = filename
            button_browse.pressed = False

        signal = button_save.detect(event.pos)
        if signal == "pressed":

            button_cancel.draw()
            screen.blit(bg, (0, 0))
            pg.display.update()
            time.sleep(0.08)
            schedule.append((int(box_hour.text[1][0]), int(box_minute.text[1][0])))
            playlist.append(box_browse.text[0][0])
            active.append(False)
            button_list_inital()
            write_schedule()
            console = False 

        signal = button_cancel.detect(event.pos)
        if signal == "pressed":

            button_cancel.draw()
            screen.blit(bg, (0, 0))
            pg.display.update()
            time.sleep(0.08)
            console = False

    if event.type == pg.KEYDOWN:
        #print(event.unicode)
        if focus == "hour":
            if event.unicode == u"\u0008":
                for i in [0,1]:
                    for j in [1,0]:
                        if box_hour.text[1][i][j] != "!":
                            if j == 1:
                                box_hour.text[1][i] = box_hour.text[1][i][0] + "!"
                                break
                            elif j == 0:
                                box_hour.text[1][i] = "!!"
                                break

            elif event.unicode.encode('utf-8').isdigit():
                for i in [0,1]:
                    for j in [0,1]:
                        if box_hour.text[1][i][j] == "!":
                            if j == 0 and int(event.unicode.encode('utf-8')) <= 2:
                                box_hour.text[1][i] = event.unicode.encode('utf-8') + "!"
                                break
                            elif j == 1:
                                if (box_hour.text[1][i][0] == "2" and int(event.unicode.encode('utf-8')) <= 3 ) or box_hour.text[1][i][0] in ["0","1"] :
                                    box_hour.text[1][i] = box_hour.text[1][i][0] + event.unicode.encode('utf-8')
                                    box_hour.pressed = False
                                    box_minute.pressed = True
                                    focus = "minute"
                                    break


        elif focus == "minute":
            if event.unicode == u"\u0008":
                for i in [0,1]:
                    for j in [1,0]:
                        if box_minute.text[1][i][j] != "!":
                            if j == 1:
                                box_minute.text[1][i] = box_minute.text[1][i][0] + "!"
                                break
                            elif j == 0:
                                box_minute.text[1][i] = "!!"
                                break

            elif event.unicode.encode('utf-8').isdigit():
                for i in [0,1]:
                    for j in [0,1]:
                        if box_minute.text[1][i][j] == "!":
                            if j == 0 and int(event.unicode.encode('utf-8')) <= 5:
                                box_minute.text[1][i] = event.unicode.encode('utf-8') + "!"
                                break
                            elif j == 1 and box_minute.text[1][i][0] != "!":
                                box_minute.text[1][i] = box_minute.text[1][i][0] + event.unicode.encode('utf-8')
                                break


        elif focus == "browse":
            if event.unicode == u"\u0008":
                for i in [0,1]:
                    box_browse.text[0][i] = box_browse.text[0][i][:-1]
            else:
                
                for i in [0,1]:
                    box_browse.text[0][i] += event.unicode.encode('utf-8') 


# volume trash
volume_down = 0x0a
volume_up = 0x09
volume_mute = 0x08


# ring function
def play_ring(ring):
    r = random.random()
    if button_red.pressed == True:
        if sys.platform == "win32" or "win64":
            for i in range(50):
                ctypes.windll.user32.PostMessageA(
                    ctypes.windll.user32.GetForegroundWindow(), 0x319, 0, volume_down*0x10000)
            for i in range(35):
                ctypes.windll.user32.PostMessageA(
                    ctypes.windll.user32.GetForegroundWindow(), 0x319, 0, volume_up*0x10000)

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
            if button_list[schedule.index((now.hour, now.minute))].pressed == False:
                play_ring(playlist[schedule.index((now.hour, now.minute))])

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
    for i in button_delete:
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

    if console == True:
        set_time_console_draw()

    screen.blit(bg, (0, 0))
    pg.display.update()

    c.tick(fps)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if console == True:
            set_time_console_detect()
        else:
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
                    [i.detect(event.pos) for i in button_list[:-1]]
                    signal = button_list[-1].detect(event.pos)
                    if signal == "pressed":
                        button_list[-1].draw()
                        pg.draw.rect(bg, (0,0,0), [674, height*3/4 + 103, 191, 60], 0)
                        button_list_box = pg.draw.rect(bg, (170,170,170), [674, height*3/4 - 63, 191, 166], 2)
                        screen.blit(bg, (0, 0))
                        pg.display.update()
                        time.sleep(0.08)
                        button_list[-1].pressed = False
                        set_time_console_initial()
                        console = True

                    for i in range(len(button_delete)):
                        signal = button_delete[i].detect(event.pos)
                        if signal == "pressed":
                            del schedule[i], playlist[i]
                            button_list_inital()
                            break
                    active = [i.pressed for i in button_list[:-1]]
                    write_schedule()


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
                    for i in range(len(button_delete)):
                        button_delete[i].pos = (845, height*3/4 - 53 + 65*i - button_list_y)
        
