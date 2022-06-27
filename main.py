from re import sub
import pygame
from pygame import MOUSEBUTTONUP, mixer 

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0,0,0)
white = (255, 255, 255)
gray = (128, 128, 128)
light_gray = (170, 170, 170)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
cobalt_blue = (158, 171, 197)
light_blue = (167, 208, 217)
silver = (198, 190, 186)
platinum = (233, 230, 224)
dutch = (224, 210, 183)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 20)
drums = pygame.image.load(r'C:\Users\danie\game\Images\Drums.png')
kanye = pygame.image.load(r'C:\Users\danie\game\Images\Kanye.png')
windows = pygame.image.load(r'C:\Users\danie\game\Images\Windows.png')
title = pygame.image.load(r'C:\Users\danie\game\Images\Title.png')
title2 = pygame.image.load(r'C:\Users\danie\game\Images\Title2.png')

index = 100
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False
selection = 0
start_menu = True
selected = False

sounds_text = [['Hi Hat', 'Snare', 'Kick', 'Crash', 'Clap', 'Tom'],['Kanye Yo', 'Kanye No', 'Kanye Like', 'Justin', 'Kanye Uhh','Kanye Ah'], 
['Error', 'Chord', 'Error 2', 'Login', 'Ding', 'USB']]

# load in sounds

hi_hat = mixer.Sound('sounds\hi hat.WAV')
snare = mixer.Sound('sounds\snare.WAV')
kick = mixer.Sound('sounds\kick.WAV')
crash = mixer.Sound('sounds\crash.WAV')
clap = mixer.Sound('sounds\clap.WAV')
tom = mixer.Sound('sounds\\tom.WAV')
kanye_yo = mixer.Sound('sounds\Kanye_yo.WAV')
kanye_no = mixer.Sound('sounds\Kanye_no.WAV')
kanye_like = mixer.Sound('sounds\Kanye_like.WAV')
kanye_justin = mixer.Sound('sounds\Kanye_justin.WAV')
kanye_uhh = mixer.Sound('sounds\Kanye_uhh.WAV')
kanye_ah = mixer.Sound('sounds\Kanye_ah.WAV')
error = mixer.Sound('sounds\Error.WAV')
chord = mixer.Sound('sounds\chord.WAV')
error_2 = mixer.Sound('sounds\Error_2.WAV')
login = mixer.Sound('sounds\Login.WAV')
ding = mixer.Sound('sounds\Ding.WAV')
usb = mixer.Sound('sounds\\Usb.WAV')
pygame.mixer.set_num_channels(instruments * 4)

sounds = [[hi_hat, snare, kick, crash, clap, tom],[kanye_yo, kanye_no, kanye_like, kanye_justin, kanye_uhh, kanye_ah], [error, chord, error_2, login, ding, usb]]

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                sounds[selection][i].play()
            if i == 1:
                sounds[selection][i].play()
            if i == 2:
                sounds[selection][i].play()
            if i == 3:
                sounds[selection][i].play()
            if i == 4:
                sounds[selection][i].play()
            if i == 5:
                sounds[selection][i].play()


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200 , WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render(sounds_text[selection][0], True, colors[actives[0]])
    screen.blit(hi_hat_text, (30,30))
    snare_text = label_font.render(sounds_text[selection][1], True, colors[actives[1]])
    screen.blit(snare_text, (30,130))
    kick_text = label_font.render(sounds_text[selection][2], True, colors[actives[2]])
    screen.blit(kick_text, (20,230))
    crash_text = label_font.render(sounds_text[selection][3], True, colors[actives[3]])
    screen.blit(crash_text, (30,330))
    clap_text = label_font.render(sounds_text[selection][4], True, colors[actives[4]])
    screen.blit(clap_text, (30,430))
    crash_text = label_font.render(sounds_text[selection][5], True, colors[actives[5]])
    screen.blit(crash_text, (30,530))

    for i in range(6):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100 + 100)), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH-200) // beats) + 205, (j * 100) + 5, ((WIDTH-200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH-200) // beats) + 200, (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)

            pygame.draw.rect(screen, black, [i * ((WIDTH-200) // beats) + 200, (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 2, 5)

            boxes.append((rect, (i, j)))
        
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200)//beats)+ 200, 0, ((WIDTH - 200)//beats), instruments * 100], 5, 3)
    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a Name for Current Beat', True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    screen.blit(saving_txt, (WIDTH//2 - 80, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, (380, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT -100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rect

def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('LOAD MENU: Select a Beat to Load', True, white)
    loading_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_txt = label_font.render('Load Beat', True, white)
    screen.blit(loading_txt, (WIDTH//2 - 80, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 500, HEIGHT * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete Beat', True, white)
    screen.blit(delete_text, (WIDTH // 2 - 490, HEIGHT * 0.87 + 30))
    screen.blit(menu_text, (380, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT -100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loaded_rectangle = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, light_gray, [190, 100 + index*50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8: beat_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14:-3]
            loaded_clicks_rows = list(loaded_clicks_string.split('], ['))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int (loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    return exit_btn, loading_btn, delete_btn, loaded_rectangle, loaded_info

def draw_start_menu():
    pygame.draw.rect(screen, silver, [0, 0, WIDTH, HEIGHT])
    #menu_text = label_font.render('Beat Maker: Choose a version', True, white)
    original_rect = pygame.draw.rect(screen, dutch, [WIDTH // 2 - 150, HEIGHT * 0.25, 250, 100], 0, 5)
    original_txt = label_font.render('Original', True, white)
    screen.blit(original_txt, (WIDTH//2 - 90, HEIGHT * 0.25 + 30))
    kanye_rect = pygame.draw.rect(screen, dutch, [WIDTH // 2 - 150, HEIGHT * 0.25 + 150, 250, 100], 0, 5)
    kanye_txt = label_font.render('Kanye', True, white)
    screen.blit(kanye_txt, (WIDTH//2 - 75, HEIGHT * 0.25 + 180))
    screen.blit(title2, (400, 60))
    windows_rect = pygame.draw.rect(screen, dutch, [WIDTH // 2 - 150, HEIGHT * 0.25 + 300, 250, 100], 0, 5)
    windows_txt = label_font.render('Windows', True, white)
    screen.blit(windows_txt, (WIDTH//2 - 95, HEIGHT * 0.25 + 330))
    screen.blit(drums, (WIDTH // 2 + 200, HEIGHT * 0.25 + 150))
    screen.blit(kanye, (100,80))
    screen.blit(windows, (230,500))


    return original_rect, kanye_rect, windows_rect

run = True
while run:
    
    #main menu
    if start_menu:
        original_rect, kanye_rect, windows_rect = draw_start_menu()

    if selected:                
        timer.tick(fps)
        screen.fill(black)
        boxes = draw_grid(clicked, active_beat, active_list)

        #lower menu buttons
        play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
        play_text = label_font.render('Play/Pause', True, white)
        screen.blit(play_text, (60, HEIGHT-130))
        
        if playing:
            play_text2 = medium_font.render('Playing', True, dark_gray)
        else:
            play_text2 = medium_font.render('Pause', True, dark_gray)
        screen.blit(play_text2, (60, HEIGHT-90))
        
        #bpm stuff
        bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
        bpm_text = medium_font.render('Beats Per Minute', True, white)
        screen.blit(bpm_text, (315, HEIGHT - 130))
        bpm_text2 = label_font.render(f'{bpm}', True, white)
        screen.blit(bpm_text2, (370, HEIGHT - 100))
        bpm_add_rect =pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
        bpm_sub_rect =pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
        add_text = medium_font.render('+5', True, white)
        sub_text = medium_font.render('-5', True, white)
        screen.blit(add_text, (523, HEIGHT - 135))
        screen.blit(sub_text, (525, HEIGHT - 85))

        # beats stuff
        beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
        beats_text = medium_font.render('Beats In Loop', True, white)
        screen.blit(beats_text, (632, HEIGHT - 130))
        beats_text2 = label_font.render(f'{beats}', True, white)
        screen.blit(beats_text2, (688, HEIGHT - 100))
        beats_add_rect =pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
        beats_sub_rect =pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
        add_text2 = medium_font.render('+1', True, white)
        sub_text2 = medium_font.render('-1', True, white)
        screen.blit(add_text2, (823, HEIGHT - 135))
        screen.blit(sub_text2, (825, HEIGHT - 85))

        # instrument rects
        instrument_rects = []
        for i in range(instruments):
            rect = pygame.rect.Rect((0, i * 100), (200, 100))
            instrument_rects.append(rect)

        #save and load stuff
        save_button = pygame.draw.rect(screen, gray, [900, HEIGHT  - 150, 200, 48], 0, 5)
        save_text = label_font.render('Save Beat', True, white)
        screen.blit(save_text, (920, HEIGHT - 140))
        load_button = pygame.draw.rect(screen, gray, [900, HEIGHT  - 100, 200, 48], 0, 5)
        load_text = label_font.render('Load Beat', True, white)
        screen.blit(load_text, (920, HEIGHT - 90))
        #clear board
        clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT  - 150, 200, 100], 0, 5)
        clear_text = label_font.render('Clear Board', True, white)
        screen.blit(clear_text, (1157, HEIGHT - 115))

    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
        #playing = False
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rectangle, loaded_info = draw_load_menu(index)
        #playing = False



    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if selected:
            if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu and not start_menu:
                for i in range(len(boxes)):
                    if boxes[i][0].collidepoint(event.pos):
                        coords = boxes[i][1]
                        clicked[coords[1]][coords[0]] *= -1
            if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu and not start_menu:
                if play_pause.collidepoint(event.pos):
                    if playing:
                        playing = False
                    elif not playing:
                        playing = True
                elif bpm_add_rect.collidepoint(event.pos):
                    bpm += 5
                elif bpm_sub_rect.collidepoint(event.pos):
                    bpm -= 5
                elif beats_add_rect.collidepoint(event.pos):
                    beats += 1
                    for i in range(len(clicked)):
                        clicked[i].append(-1)

                elif beats_sub_rect.collidepoint(event.pos):
                    beats -= 1
                    for i in range(len(clicked)):
                        clicked[i].pop(-1)
                elif clear_button.collidepoint(event.pos):
                    clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
                elif save_button.collidepoint(event.pos):
                    save_menu = True
                elif load_button.collidepoint(event.pos):
                    load_menu = True
                for i in range(len(instrument_rects)):
                    if instrument_rects[i].collidepoint(event.pos):
                        active_list[i] *= -1
            elif event.type == pygame.MOUSEBUTTONUP:            
                if exit_button.collidepoint(event.pos):
                    save_menu = False
                    load_menu = False
                    playing = True
                    beat_name = ''
                    typing = False
                if load_menu:
                    if loaded_rectangle.collidepoint(event.pos):
                        index = (event.pos[1] - 100) // 50
                    if delete_button.collidepoint(event.pos):
                        if 0 <= index < len(saved_beats):
                            saved_beats.pop(index)
                    if loading_button.collidepoint(event.pos):
                        if 0 <= index < len(saved_beats):
                            beats = loaded_info[0]
                            bpm = loaded_info[1]
                            clicked = loaded_info[2]
                            index = 100
                            load_menu = False
                if save_menu:
                    if entry_rectangle.collidepoint(event.pos):
                        if typing:
                            typing = False
                        elif not typing:
                            typing = True
                    if saving_button.collidepoint(event.pos):
                        file = open('saved_beats.txt', 'w')
                        saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                        for i in range(len(saved_beats)):
                            file.write(str(saved_beats[i]))
                        file.close()
                        save_menu = False
                        typing = False
                        beat_name = ''
            if event.type == pygame.TEXTINPUT and typing:
                beat_name += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                    beat_name = beat_name[:-1]

        if not selected and event.type == pygame.MOUSEBUTTONUP:
            if original_rect.collidepoint(event.pos):
                    selection = 0
                    selected = True
                    start_menu = False
            if kanye_rect.collidepoint(event.pos):
                    selection = 1
                    selected = True
                    start_menu = False
            if windows_rect.collidepoint(event.pos):
                    selection = 2
                    selected = True
                    start_menu = False


    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True


    
    pygame.display.flip()
pygame.quit()

