# ----- system ----- #
from sys import exit
from pynput import keyboard

# ----- rich ----- #
from rich.live import Live
from rich.table import Table
from threading import Thread

# ----- custom ----- #
from board import Board
from header import Header
from layout import make_layout
from instructions import Instructions
from ai import get_random_move, get_optimal_move


class TicTacToe:
    def __init__(self):
        self.running = True
        self.in_game = False
        self.row, self.col = 1, 1
        self.data = [[" ", " ", " "] for _ in range(3)]

        self.board = Board(self)
        self.instructions = Instructions()

        self.layout = make_layout()
        self.layout["header"].update(Header())
        self.layout["board"].update(self.board)
        self.layout["instructions"].update(self.instructions)

    def count_blank_cells(self) -> int:
        return sum(row.count(" ") for row in self.data)

    def is_game_over(self) -> tuple[bool, str]:
        board = self.data

        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return True, board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != " ":
                return True, board[0][i]

        if board[0][0] == board[1][1] == board[2][2] != " ":
            return True, board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != " ":
            return True, board[0][2]

        if self.count_blank_cells() == 0:
            return True, "="

        return False, ""

    def make_ai_move(self) -> None:
        if self.count_blank_cells() == 0:
            return

        mode = self.instructions.get_selected_mode()

        if mode == "Normal":
            r, c = get_random_move(self.data)
        elif mode == "Impossible":
            r, c = get_optimal_move(self.data)

        self.data[r][c] = "X"

    def get_styled_cell(self, val: str, r: int, c: int) -> str:
        is_current = (r == self.row and c == self.col)

        if is_current and self.in_game and self.count_blank_cells() > 0:
            if val == ' ':
                return "[yellow]■[/yellow]"
            else:
                return f"[yellow]{val}[/yellow]"

        if val == "X":
            return f"[red]{val}[/red]"
        if val == "O":
            return f"[green]{val}[/green]"

        return val

    def generate_board_table(self) -> Table:
        table = Table(safe_box=True, padding=(1, 3),
                      show_lines=True, show_header=False)

        for i, row in enumerate(self.data):
            table.add_row(
                self.get_styled_cell(row[0], i, 0),
                self.get_styled_cell(row[1], i, 1),
                self.get_styled_cell(row[2], i, 2)
            )

        return table

    def process_key_press(self, key) -> None:
        if key == keyboard.Key.esc or (hasattr(key, 'char') and key.char in ['q', 'Q']):
            self.running = False
            exit()

        try:
            k = key.char
        except:
            k = key.name

        # ----- mode selection phase ----- #
        if not self.instructions.selection_done:
            if k == "up":
                self.instructions.move_up()
            elif k == "down":
                self.instructions.move_down()
            elif k == "enter":
                self.in_game = True
                self.instructions.select()

            self.layout["instructions"].update(self.instructions)
            return

        # ----- restart after game over ----- #
        if not self.in_game and isinstance(k, str) and k.upper() == "P":
            self.restart()
            self.in_game = True
            return

        # ----- game phase ----- #
        if k in ['up', 'down', 'left', 'right']:
            match k:
                case "up": self.row = max(0, self.row - 1)
                case "down": self.row = min(2, self.row + 1)
                case "left": self.col = max(0, self.col - 1)
                case "right": self.col = min(2, self.col + 1)

        elif isinstance(k, str) and (k.lower() in ["o", 'space']) and self.data[self.row][self.col] == " ":
            self.data[self.row][self.col] = "O"

            if self.check_and_update_game_status():
                self.layout["board"].update(self.board)
                return

            self.make_ai_move()
            self.check_and_update_game_status()
            self.layout["board"].update(self.board)

    def check_and_update_game_status(self) -> bool:
        over, result = self.is_game_over()
        if over:
            self.in_game = False
            self.instructions.update_result(result)
            self.layout["instructions"].update(self.instructions)
        return over

    def restart(self) -> None:
        self.in_game = False
        self.row, self.col = 1, 1
        self.data = [[" ", " ", " "] for _ in range(3)]

        self.instructions.result = None
        self.layout["board"].update(self.board)
        self.layout["instructions"].update(self.instructions)

    def start_keyboard_listener(self) -> None:
        with keyboard.Listener(on_press=self.process_key_press) as listener:
            listener.join()

    def run_ui_loop(self) -> None:
        with Live(self.layout, refresh_per_second=2, screen=True) as live:
            while self.running:
                live.update(self.layout, refresh=True)

    def start(self) -> None:
        thread_ui = Thread(target=self.run_ui_loop)
        thread_keys = Thread(target=self.start_keyboard_listener)

        thread_ui.start()
        thread_keys.start()

        thread_ui.join()
        thread_keys.join()
