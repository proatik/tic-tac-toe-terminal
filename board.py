# ----- typing ----- #
from typing import TYPE_CHECKING

# ----- rich ----- #
from rich.panel import Panel
from rich.align import Align


if TYPE_CHECKING:
    from game import TicTacToe


class Board:
    def __init__(self, game: "TicTacToe"):
        self.game = game

    def __rich__(self) -> Panel:
        return Panel(
            Align.center(self.game.generate_board_table(), vertical="middle"),
            title="Board",
            border_style="#565656"
        )
