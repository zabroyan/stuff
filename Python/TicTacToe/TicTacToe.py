import pygame as pg
import sys
import time
from pygame.locals import *

width = 400
height = 400
white = (255, 255, 255)
line_color = (0, 0, 0)

board = [[None] * 3, [None] * 3, [None] * 3]
player = 'X'
count = 0
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

x_img = pg.image.load("x.png")
y_img = pg.image.load("o.png")

x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))


def game_initiating_window():
    screen.fill(white)
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_info()


def draw_info():
    if not is_win() and count < 9:
        message = player + "'s turn"
    elif not is_win() and count == 9:
        message = "In a draw!"
    else:
        message = player + " won!"
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, white)

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def is_win():
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6),
                         4)
            return True

    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            return True

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
        return True

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
        return True
    return False


def draw_cell(row, col):
    global player
    posx = posy = 0
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30

    board[row - 1][col - 1] = player
    if player == 'X':
        screen.blit(x_img, (posy, posx))
    else:
        screen.blit(o_img, (posy, posx))
    pg.display.update()


def user_click():
    global player, count
    x, y = pg.mouse.get_pos()
    if x < width / 3:
        col = 1

    elif x < width / 3 * 2:
        col = 2

    elif x < width:
        col = 3

    else:
        col = None

    if y < height / 3:
        row = 1

    elif y < height / 3 * 2:
        row = 2

    elif y < height:
        row = 3

    else:
        row = None

    if row and col and board[row - 1][col - 1] is None:
        count += 1
        draw_cell(row, col)
        if not is_win():
            if player == 'X':
                player = 'O'
            else:
                player = 'X'


def game():
    global player
    while True:
        for event in pg.event.get():
            draw_info()
            if is_win():
                pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                user_click()
        pg.display.update()
        CLOCK.tick(fps)


game_initiating_window()
game()
