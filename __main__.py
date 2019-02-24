import curses

from time import time
from random import randint
from settings import *


class Game:
    wait_time = INIT_WAIT_TIME_SEC
    score = 0
    level = 0
    last_lv_score = 0
    last_bonus_t = 0
    t = -1
    car = 0
    is_alive = True

    stage2board = (
        '  ',  # 0
        f'{OBJ} ',  # 1
        f' {OBJ}',  # 2
    )

    def __init__(self):
        self.stage = [0] * N_START_BLANK
        self.win_board = curses.newwin(ROW, COL + 1, 0, 0)
        self.win_score = curses.newwin(1, len('999 99') + 1, ROW, 0)

    def gen_next_row(self):
        if self.stage[-1] == 0:
            next_row = randint(0, 2)
        else:
            next_row = randint(0, 1)
            if self.stage[-1] == 2 and next_row == 1:
                next_row = 2
        self.stage.append(next_row)

    def check_death(self):
        if self.car + 1 == self.stage[self.t]:
            self.is_alive = False
        self.paint()

    def paint(self):
        while len(self.stage) < self.t + ROW:
            self.gen_next_row()

        for y, r in enumerate(reversed(self.stage[self.t:])):
            self.win_board.addstr(y, 0, self.stage2board[r], curses.color_pair(1))
        self.win_board.addstr(ROW - 1, self.car, CAR, curses.color_pair(1))
        self.win_score.addstr(0, 0, f'{self.score} {self.level}', curses.color_pair(1))

    def update_state(self):
        self.t += 1
        if self.t and self.t % SCORE_EVERY_CLOCK == 0:
            self.score += 1
        if self.score % LV_EVERY_SCORE == 0 and (
                self.last_lv_score != self.score):
            self.last_lv_score = self.score
            self.level += 1
            self.wait_time *= STEP_MULTIPLIER

    def switch_car(self):
        if self.car + 1 == self.stage[self.t + 1] and (
                self.last_bonus_t != self.t):
            self.last_bonus_t = self.t
            self.score += 1
            self.last_lv_score = self.score
        self.car = (1, 0)[self.car]
        self.check_death()

    def check_input(self):
        self.win_score.refresh()
        c = self.win_board.getch()
        if c == (OR, OL)[self.car]:
            self.switch_car()
        elif c == OQ:
            exit()

    def end(self):
        # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.win_board.timeout(-1)
        while self.win_board.getch() != OQ:
            pass

    def run(self):
        while self.is_alive:
            wake_time = time() + self.wait_time

            self.update_state()
            self.check_death()

            while self.is_alive and time() < wake_time:
                self.win_board.timeout(max(0, int((wake_time - time()) * 1000)))
                self.check_input()

        self.end()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    Game().run()


curses.wrapper(main)
