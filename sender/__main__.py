from nfs.settings import *
from . import sender

import sys
import tty
import termios


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


print('READY')

while True:
    c = getch()
    if c == L:
        sender.sendl()
    elif c == R:
        sender.sendr()
    elif c == Q:
        break
