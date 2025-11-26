import curses
from curses import wrapper
from curses.textpad import Textbox

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_BLACK, -1)
    curses.init_pair(6, curses.COLOR_WHITE, -1)
    curses.init_pair(7, -1, curses.COLOR_BLACK)
    RED = curses.color_pair(1)
    YELLOW  = curses.color_pair(2)
    GREEN  = curses.color_pair(3)
    BLUE = curses.color_pair(4)
    BLACK = curses.color_pair(5)
    WHITE = curses.color_pair(6)
    BACK_BLACK = curses.color_pair(7)

    h, w = stdscr.getmaxyx()

    try:
        curses.curs_set(0)
    except curses.error:
        pass

    stdscr.clear() 
    stdscr.refresh()

    help_h, help_w = 1, w
    help_win = curses.newwin(help_h, help_w, h-1, 0)
    help_win.addstr(0, 0, " NORMAL ", curses.A_BOLD | BLUE | curses.A_REVERSE )
    help_win.addstr(0, help_w-4, "   ", curses.A_BOLD)
    help_win.addstr(0, help_w//2-(8//2), "h - HELP", WHITE)
    help_win.refresh()

    todo_h, todo_w = h-2, w//3
    todo_win = curses.newwin(todo_h, todo_w, 0, 0)
    todo_win.attron(RED)
    todo_win.box()
    todo_win.addstr(0, 1, " Todo ", curses.A_BOLD | curses.A_REVERSE | RED)

    edit_win = curses.newwin(todo_h-2, todo_w-2, 1, 1)
    textbox = Textbox(edit_win)

    todo_win.refresh()
    edit_win.refresh()

    pro_h, pro_w = h-2, w//3
    pro_win = curses.newwin(pro_h, pro_w, 0, w//2-(pro_w//2))
    pro_win.attron(YELLOW)
    pro_win.box()
    pro_win.addstr(0, 1, " In Progress ", curses.A_BOLD | curses.A_REVERSE | YELLOW)
    pro_win.refresh()

    done_h, done_w = h-2, w//3
    done_win = curses.newwin(done_h, done_w, 0, w-done_w)
    done_win.attron(GREEN)
    done_win.box()
    done_win.addstr(0, 1, " Done ", curses.A_BOLD | curses.A_REVERSE | GREEN)
    done_win.refresh()

    todo_tasks = []
    pro_tasks = []
    done_tasks = []
    current_column = 0
    current_index = 0

    def render_tasks():
        selected_attr = curses.A_REVERSE
        normal_attr_todo = RED
        normal_attr_pro = YELLOW
        normal_attr_done = GREEN

        todo_win.erase()
        todo_win.box()
        attr = selected_attr if current_column == 0 else normal_attr_todo
        todo_win.addstr(0, 1, " Todo ", curses.A_BOLD | attr | normal_attr_todo)
        for i, task in enumerate(todo_tasks):
            attr = curses.A_REVERSE if current_column == 0 and i == current_index else curses.A_NORMAL
            todo_win.addstr(1 + i, 1, task, attr)
        todo_win.refresh()

        pro_win.erase()
        pro_win.box()
        attr = selected_attr if current_column == 1 else normal_attr_todo
        pro_win.addstr(0, 1, " In Progress ", curses.A_BOLD | attr | normal_attr_pro)
        for i, task in enumerate(pro_tasks):
            attr = curses.A_REVERSE if current_column == 1 and i == current_index else curses.A_NORMAL
            pro_win.addstr(1 + i, 1, task, attr)
        pro_win.refresh()

        done_win.erase()
        done_win.box()
        attr = selected_attr if current_column == 2 else normal_attr_todo
        done_win.addstr(0, 1, " Done ", curses.A_BOLD | attr | normal_attr_done)
        for i, task in enumerate(done_tasks):
            attr = curses.A_REVERSE if current_column == 2 and i == current_index else curses.A_NORMAL
            done_win.addstr(1 + i, 1, task, attr)
        done_win.refresh()


    def validate_key(ch):
        if ch == 10 or ch == 13:
            y, x = edit_win.getyx()
            edit_win.insstr(y, x, '\n- ')
            edit_win.move(y + 1, 2)
            edit_win.refresh()
            return 0
        elif ch == 27:
            return 7
        else:
            return ch

    def help_screen():
        help_screen_h, help_screen_w = h-2, w
        help_screen_win = curses.newwin(help_screen_h, help_screen_w, 0, 0)
        help_screen_win.attron(BLUE)
        help_screen_win.box()
        help_screen_win.addstr(0, 1, " Help ", curses.A_BOLD | curses.A_REVERSE | BLUE)
        help_screen_win.addstr(help_screen_h-1, help_screen_w//2-(21//2), "Press Any Key to Hide", curses.A_ITALIC | curses.A_DIM)

        help_screen_win.addstr(2, 1, "- q   : QUIT", WHITE)
        help_screen_win.addstr(3, 1, "- ESC : NORMAL MODE", WHITE)
        help_screen_win.addstr(4, 1, "- a/i : ADD TASK", WHITE)
        help_screen_win.addstr(5, 1, "- d/r : DELETE SELECTED TASK", WHITE)
        help_screen_win.addstr(6, 1, "- h/← : MOVE SELECTED TASK LEFT", WHITE)
        help_screen_win.addstr(7, 1, "- l/→ : MOVE SELECTED TASK RIGHT", WHITE)
        help_screen_win.addstr(8, 1, "- k/↑ : MOVE SELECTION UP", WHITE)
        help_screen_win.addstr(9, 1, "- j/↓ : MOVE SELECTION DOWN", WHITE)

        help_screen_win.refresh()
        key = stdscr.getch()
        if key == 27:
            help_screen_win.clear()

    select = False

    while True:
        render_tasks()
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('h'):
            help_screen()
        elif key == 27:
            help_win.addstr(0, 0, " NORMAL ", curses.A_BOLD | BLUE | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "   ", curses.A_BOLD)
            help_win.refresh()
            if select:
                current_column = 0
                current_index = 0
                render_tasks()
                select = False
        elif key == ord('d') or key == ord('r'):
            if current_column == 0:
                if len(todo_tasks) > 0:
                    todo_tasks.pop(current_index)
            elif current_column == 1:
                if len(pro_tasks) > 0:
                    pro_tasks.pop(current_index)
            else:
                if len(done_tasks) > 0:
                    done_tasks.pop(current_index)
            render_tasks()
        elif key == ord('a') or key == ord('i'):
            current_column = 0
            current_index = 0
            render_tasks()
            help_win.addstr(0, 0, " ADD    ", curses.A_BOLD | GREEN | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            try:
                curses.curs_set(1)
            except curses.error:
                pass

            help_win.refresh()

            edit_win.clear()
            edit_win.addstr(0, 0, "- ")
            edit_win.move(0, 2)
            edit_win.refresh()

            textbox.edit(validate_key)

            task_text = textbox.gather().strip()
            if task_text.startswith("- "):
                task_text = task_text[2:].strip()
            if task_text:
                todo_tasks.append("- " + task_text)

            help_win.addstr(0, 0, " SELECT ", curses.A_BOLD | YELLOW | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            help_win.refresh()
            render_tasks()
            select = True
        elif key in [curses.KEY_RIGHT, ord('l')]:
            select = True
            help_win.addstr(0, 0, " SELECT ", curses.A_BOLD | YELLOW | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            help_win.refresh()
            active_tasks = [todo_tasks, pro_tasks, done_tasks]
            if current_column < 2:
                if current_index != -1 and current_index < len(active_tasks[current_column]):
                    task = active_tasks[current_column].pop(current_index)
                    next_column = current_column + 1
                    active_tasks[next_column].append(task)

                    if current_index >= len(active_tasks[current_column]):
                        current_index = len(active_tasks[current_column]) - 1

                    current_column = next_column
                    current_index = len(active_tasks[next_column]) - 1
                else:
                    current_column += 1
                    current_index = -1
        elif key in [curses.KEY_LEFT, ord('h')]:
            select = True
            help_win.addstr(0, 0, " SELECT ", curses.A_BOLD | YELLOW | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            help_win.refresh()

            active_tasks = [todo_tasks, pro_tasks, done_tasks]
            if current_column > 0:
                if current_index != -1 and current_index < len([todo_tasks, pro_tasks, done_tasks][current_column]):
                    task = active_tasks[current_column].pop(current_index)
                    new_column = current_column - 1
                    active_tasks[new_column].append(task)

                    if current_index >= len(active_tasks[current_column]):
                        current_index = len(active_tasks[current_column]) - 1
                    current_column = new_column
                    current_index = len(active_tasks[new_column]) - 1
                else:
                    current_column -= 1
                    current_index = -1
        elif key in [curses.KEY_UP, ord('k')]:
            select = True
            help_win.addstr(0, 0, " SELECT ", curses.A_BOLD | YELLOW | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            help_win.refresh()

            if current_index == -1 and len([todo_tasks, pro_tasks, done_tasks][current_column]) > 0:
                current_index = 0
            elif current_index > 0:
                current_index -= 1
        elif key in [curses.KEY_DOWN, ord('j')]:
            select = True
            help_win.addstr(0, 0, " SELECT ", curses.A_BOLD | YELLOW | curses.A_REVERSE)
            help_win.addstr(0, help_w-4, "ESC", curses.A_BOLD | WHITE)
            help_win.refresh()

            if current_index + 1 < len([todo_tasks, pro_tasks, done_tasks][current_column]):
                current_index += 1


wrapper(main)
