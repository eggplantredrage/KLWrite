import curses
import os

def show_menu(stdscr, menu_options, current_option):
    """Display a menu bar at the top of the screen with highlighted option."""
    stdscr.attron(curses.color_pair(1))
    x_offset = 0

    for i, option in enumerate(menu_options):
        if i == current_option:  # Highlight the current menu option
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(0, x_offset, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(0, x_offset, option)

        x_offset += len(option) + 3  # Adjust spacing between options

    # Add the instruction message at the end of the menu bar
    instructions = "Press F10 to navigate and F9 to select"
    stdscr.addstr(0, x_offset, instructions)

    # Add the program name at the end of the menu bar
    program_name = "KLWrite Editor"
    stdscr.addstr(0, x_offset + len(instructions) + 3, program_name)

    stdscr.attroff(curses.color_pair(1))


def get_filename(stdscr, prompt):
    """Prompt the user for a filename."""
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    filename = stdscr.getstr().decode("utf-8").strip()
    curses.noecho()
    return filename


def show_about(stdscr):
    """Display an About screen with information about the program."""
    stdscr.clear()
    stdscr.addstr(0, 0, "About KLWrite")
    stdscr.addstr(2, 0, "Version: 0.2")
    stdscr.addstr(3, 0, "Written by: Kevin Leblanc (Eggplant48) on 2025-01-08")
    stdscr.addstr(5, 0, "This is a basic text editor inspired by Nano.")
    stdscr.addstr(7, 0, "Press any key to return to the editor...")
    stdscr.refresh()
    stdscr.getch()  # Wait for any key press to return


def nano_clone(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Menu options
    menu_options = ["File", "Edit", "Save", "About", "Exit"]
    current_option = 0  # Highlighted menu option index

    # Ask for the initial file to open or create
    filename = get_filename(stdscr, "Enter the filename to open or create: ")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
    else:
        lines = [""]

    lines = [line.rstrip("\n") for line in lines]
    cursor_y, cursor_x = 0, 0

    while True:
        # Display the menu
        stdscr.clear()
        show_menu(stdscr, menu_options, current_option)

        # Display the content below the menu
        for i, line in enumerate(lines):
            stdscr.addstr(i + 1, 0, line)
        stdscr.move(cursor_y + 1, cursor_x)  # +1 because of the menu row
        stdscr.refresh()

        key = stdscr.getch()

        # Menu navigation
        if key == curses.KEY_F10:  # Navigate the menu using F10
            current_option = (current_option + 1) % len(menu_options)
        elif key == curses.KEY_F9:  # F9 to select menu option
            if current_option == 0:  # File
                filename = get_filename(stdscr, "Enter filename to open or create: ")
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        lines = [line.rstrip("\n") for line in f.readlines()]
                else:
                    lines = [""]
                cursor_y, cursor_x = 0, 0
            elif current_option == 2:  # Save
                if not filename:
                    filename = get_filename(stdscr, "Enter filename to save: ")
                with open(filename, 'w') as f:
                    f.writelines(line + '\n' for line in lines)
                stdscr.addstr(len(lines) + 2, 0, f"File saved as {filename}!")
                stdscr.refresh()
                curses.napms(1000)
            elif current_option == 3:  # About
                show_about(stdscr)  # Show About screen
            elif current_option == 4:  # Exit
                break
        elif key == curses.KEY_UP:  # Move cursor up
            cursor_y = max(0, cursor_y - 1)
        elif key == curses.KEY_DOWN:  # Move cursor down
            cursor_y = min(len(lines) - 1, cursor_y + 1)
        elif key == curses.KEY_LEFT:  # Move cursor left
            cursor_x = max(0, cursor_x - 1)
        elif key == curses.KEY_RIGHT:  # Move cursor right
            cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
        elif key == 10:  # Enter key for new line
            lines.insert(cursor_y + 1, lines[cursor_y][cursor_x:])
            lines[cursor_y] = lines[cursor_y][:cursor_x]
            cursor_y += 1
            cursor_x = 0
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            if cursor_x > 0:
                lines[cursor_y] = lines[cursor_y][:cursor_x - 1] + lines[cursor_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y > 0:
                cursor_x = len(lines[cursor_y - 1])
                lines[cursor_y - 1] += lines[cursor_y]
                del lines[cursor_y]
                cursor_y -= 1
        elif key == 19:  # Ctrl-S to save
            if not filename:
                filename = get_filename(stdscr, "Enter filename to save: ")
            with open(filename, 'w') as f:
                f.writelines(line + '\n' for line in lines)
            stdscr.addstr(len(lines) + 2, 0, f"File saved as {filename}!")
            stdscr.refresh()
            curses.napms(1000)
        elif key == 24:  # Ctrl-X to exit
            break
        else:  # Handle character input
            if 32 <= key <= 126:  # Printable characters
                lines[cursor_y] = lines[cursor_y][:cursor_x] + chr(key) + lines[cursor_y][cursor_x:]
                cursor_x += 1

        # Keep cursor within bounds
        cursor_x = min(cursor_x, len(lines[cursor_y]))
        cursor_y = min(cursor_y, len(lines) - 1)


if __name__ == "__main__":
    curses.wrapper(nano_clone)
