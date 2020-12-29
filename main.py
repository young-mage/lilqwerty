from data_structs import string_data

import pygame as pg
import random
import time
import numpy as np
pg.init()

WIN_WIDTH = 400
WIN_HEIGHT = 200

words_file = open("words_alpha.txt", "r")
word_list = words_file.read().splitlines()
words_file.close()

window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("lil qwerty")
font = pg.font.SysFont("Arial", 100)
annot_font = pg.font.SysFont("Arial", 20)

wpm_render = annot_font.render("wpm: 0", True, (0, 0, 0))
mstk_render = annot_font.render("mistakes: 0", True, (0, 0, 0))
wrds_render = annot_font.render("total: 0", True, (0, 0, 0))
pg.display.set_icon(pg.image.load("icon.png"))

word_timings = []
wpm = 0
mistakes = 0
words_total = 0


# init_char_renders: string -> list<Surface>
# takes in a word and returns an array of Surfaces to render the characters individually
def init_char_renders(word):
    chars = list(word)
    textscreens = []
    for c in chars:
        textscreens.append(font.render(c, True, (0, 0, 0)))
    return textscreens


# render_word: int int list<Surface>
# takes in a list of surfaces and renders them at specified position
def render_word(x, y, char_renders):
    current_x = x
    for scr in char_renders:
        window.blit(scr, (current_x, y))
        current_x += scr.get_width()


# change_char_color: list<Surface> list<char> int (int int int) -> list<Surface>
# takes a list of chars and respective rendered character surfaces and changes a specific character to a given new color
def change_char_color(chars, char_renders, index, color):
    new_renders = char_renders
    new_renders[index] = font.render(chars[index], True, color)
    return new_renders


# render_width: list<Surface> -> int
# given a list of character Surfaces, return their total length
def render_width(renders):
    total_len = 0
    for r in renders:
        total_len += r.get_width()
    return total_len


# init_string_data: string -> string_data
# takes a string and returns a corresponding new string_data object
def init_string_data(word):
    renders = init_char_renders(word)
    width = render_width(renders)
    return string_data(word, renders, width)


meta = init_string_data(random.choice(word_list))

keys = pg.key.get_pressed()
already_pressed = np.zeros(len(keys), dtype=bool)

current_time = time.time_ns()
mistaken_on_this_character = False

run = True
while run:
    pg.time.delay(10)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    for i in range(len(keys)):
        # if the right key is pressed
        if (keys[i] and (not already_pressed[i])
                and pg.key.name(i) == meta.chars[meta.current_index]):
            meta.char_screens = change_char_color(meta.chars,
                                                  meta.char_screens,
                                                  meta.current_index,
                                                  (0, 255, 0))
            meta.current_index += 1
            mistaken_on_this_character = False
            # if the word is thereby finished
            if (meta.current_index == meta.max_len):
                time_delta = (time.time_ns() - current_time) / (10**9)
                if (len(word_timings) >= 10): word_timings.pop(0)
                word_timings.append(time_delta)
                wpm = int(60 / np.mean(word_timings))
                meta = init_string_data(random.choice(word_list))
                wpm_render = annot_font.render("wpm: " + str(wpm), True,
                                               (0, 0, 0))
                words_total += 1
                wrds_render = annot_font.render("total: " + str(words_total),
                                                True, (0, 0, 0))
                current_time = time.time_ns()
            already_pressed[i] = True

        #if the wrong key is pressed
        if (keys[i] and (not already_pressed[i])
                and pg.key.name(i) != meta.chars[meta.current_index]
                and (not mistaken_on_this_character)):
            mistakes += 1
            mstk_render = annot_font.render("mistakes: " + str(mistakes), True,
                                            (0, 0, 0))
            meta.char_screens = change_char_color(meta.chars,
                                                  meta.char_screens,
                                                  meta.current_index,
                                                  (255, 0, 0))
            mistaken_on_this_character = True

        # update the already_presssed list
        if (keys[i]):
            already_pressed[i] = True
        else:
            already_pressed[i] = False

    pg.draw.rect(window, (230, 230, 230), (0, 0, WIN_WIDTH, WIN_HEIGHT))
    render_word(WIN_WIDTH / 2 - meta.width / 2, 54, meta.char_screens)
    window.blit(wpm_render, (0, 0))
    window.blit(mstk_render, (WIN_WIDTH / 2 - mstk_render.get_width() / 2, 0))
    window.blit(wrds_render, (WIN_WIDTH - mstk_render.get_width(), 0))
    pg.display.update()

pg.quit()
