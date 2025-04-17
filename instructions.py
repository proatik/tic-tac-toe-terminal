# ----- rich ----- #
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.console import Group


class Instructions:
    def __init__(self):
        self.result = None
        self.selected_index = 0
        self.selection_done = False
        self.modes = ["Normal", "Impossible"]

    def move_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.modes)

    def move_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.modes)

    def select(self) -> None:
        self.selection_done = True

    def get_selected_mode(self) -> str:
        return self.modes[self.selected_index]

    def update_result(self, winner: str) -> None:
        if winner == "X":
            self.result = "Game Over: [red]AI wins![/]"
        elif winner == "O":
            self.result = "Game Over: [green]You win![/]"
        elif winner == "=":
            self.result = "Game Over: [yellow]It's a draw![/]"
        else:
            self.result = None

    def __rich__(self) -> Panel:
        if not self.selection_done:
            return self.render_mode_selection()
        else:
            return self.render_in_game_instructions()

    def render_mode_selection(self) -> Panel:
        hint = Text("Select Mode (↑ ↓, Enter)", justify="center", style="dim")

        table = Table.grid(padding=(0, 1))
        for i, mode in enumerate(self.modes):
            prefix = "▶" if i == self.selected_index else " "

            if i == self.selected_index:
                table.add_row(f"[bold #00C9A7]{prefix} {mode}[/]")
            else:
                table.add_row(f"[bold]{prefix} {mode}[/]")

        content = Align.center(
            Group(hint, Text("\n"), table),
            vertical="middle"
        )

        return Panel(content, title="Instructions", border_style="#565656")

    def render_in_game_instructions(self) -> Panel:
        if self.result:
            instructions = Text(
                "Press P to play again\n"
                "Press Q or ESC to exit",
                style="dim"
            )

            result_text = Text.from_markup(self.result)
        else:
            instructions = Text(
                "Press ← to move left\n"
                "Press → to move right\n"
                "Press ↑ to move up\n"
                "Press ↓ to move down\n"
                "Press O or SPACE to mark\n"
                "Press Q or ESC to exit",
                style="dim"
            )

            result_text = Text("\n", justify="center")

        return Panel(
            Align.center(
                Group(
                    instructions,
                    "\n",
                    result_text
                ),
                vertical="middle"
            ),
            title="Instructions",
            border_style="#565656"
        )
