import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    stdscr.clear()
    stdscr.addstr(0, 0, "Hello World", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getch()
    

wrapper(main)
