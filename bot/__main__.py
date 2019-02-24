from mss import mss
import numpy as np
from PIL import Image
import pyautogui

from time import sleep
from nfs.settings import *


class Bot:
    pos = -1
    board = None

    def __init__(self, sct):
        self.sct = sct

    def get_mock_coordinates(self):
        self.ul = pyautogui.Point(x=159, y=184)
        self.ur = pyautogui.Point(x=185, y=184)
        self.lr = pyautogui.Point(x=184, y=430)
        self.ll = pyautogui.Point(x=157, y=430)

    def get_coordinates(self):
        input('Upper left')
        self.ul = pyautogui.position()
        input('Upper right')
        self.ur = pyautogui.position()
        input('Lower right')
        self.lr = pyautogui.position()
        input('Lower left')
        self.ll = pyautogui.position()

        print(self.ul)
        print(self.ur)
        print(self.lr)
        print(self.ll)

    def get_min_coordinates(self):
        xs, ys = zip(self.ul, self.ur, self.lr, self.ll)
        self.left = min(xs)
        self.upper = min(ys)
        self.right = max(xs)
        self.lower = max(ys)

    def update_board(self):
        sct_img = self.sct.grab((self.left, self.upper, self.right, self.lower))
        im_orig = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        # im_orig.thumbnail((2, 99))  # unknown ROW
        im_small = im_orig.resize((COL, ROW))
        im = im_small.convert('L')

        # im_orig.show()
        # im_small.show()
        # im.show()
        # exit()

        new_board = np.asarray(im)
        if self.board is None:
            self.board = new_board
        else:
            # self.board = np.mean((new_board, self.board, np.vstack((new_board[0], self.board[:-1]))),
            self.board = np.mean((new_board, self.board),
            # self.board = np.mean((new_board,),
                                 axis=0)

    def move(self, target):
        if self.pos != target:
            self.pos = target
            pyautogui.press((L, R)[target])

    def react(self):
        next_pos = self.board[-2].argmin()
        # if self.board[-1, next_pos] == self.board[-2:].max():
        #     return
        self.move(next_pos)

    def run(self):
        # self.get_coordinates()
        self.get_mock_coordinates()
        self.get_min_coordinates()
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0

        while True:
            self.update_board()
            # print(self.board[-2:])
            # print('=====')
            self.react()
            sleep(SLEEP_TIME)


with mss() as sct:
    Bot(sct).run()
