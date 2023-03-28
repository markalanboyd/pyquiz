import curses

def draw_menu(stdscr):
    # Clear the screen
    stdscr.clear()

    # Get the size of the terminal
    height, width = stdscr.getmaxyx()

    # Draw the border
    border = curses.newwin(height, width, 0, 0)
    border.border()

    # Draw the menu options
    menu_items = ['NEW GAME', 'STATS', 'SETTINGS', 'EXIT']
    x_pos = int((width - max(map(len, menu_items))) / 2)  # Center the menu horizontally
    y_pos = int(height / 2) - 2  # Center the menu vertically
    for index, item in enumerate(menu_items):
        x = x_pos - 4 if index == 0 else x_pos  # Indent the first menu item
        y = y_pos + index
        stdscr.addstr(y, x, item)

    # Draw the cursor
    cursor_pos = 0
    cursor_x = x_pos - 2
    cursor_y = y_pos
    stdscr.addstr(cursor_y + cursor_pos, cursor_x, '>')

    # Refresh the screen
    stdscr.refresh()

    # Handle keyboard input
    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and cursor_pos > 0:
            # Move the cursor up
            stdscr.addstr(cursor_y + cursor_pos, cursor_x, ' ')
            cursor_pos -= 1
            stdscr.addstr(cursor_y + cursor_pos, cursor_x, '>')

        elif key == curses.KEY_DOWN and cursor_pos < len(menu_items) - 1:
            # Move the cursor down
            stdscr.addstr(cursor_y + cursor_pos, cursor_x, ' ')
            cursor_pos += 1
            stdscr.addstr(cursor_y + cursor_pos, cursor_x, '>')

        elif key == ord('\n'):
            # Call the selected function
            if cursor_pos == 0:
                new_game()
            elif cursor_pos == 1:
                stats()
            elif cursor_pos == 2:
                settings()
            elif cursor_pos == 3:
                exit()

def new_game():
    # Code for the "New Game" screen goes here
    pass

def stats():
    # Code for the "Stats" screen goes here
    pass

def settings():
    # Code for the "Settings" screen goes here
    pass

def main():
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Draw the menu
    draw_menu(stdscr)

    # Clean up curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()
