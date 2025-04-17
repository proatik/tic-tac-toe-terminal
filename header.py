# ----- system ----- #
from datetime import datetime

# ----- rich ----- #
from rich.panel import Panel
from rich.style import Style
from rich.table import Table


class Header:
    def __rich__(self) -> Panel:
        date_time = datetime.now().strftime("%A, %d %B, %Y | %I:%M:%S %p")
        date_time = date_time.replace(":", "[bold #565656]:[/]")

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", style=Style(color="#565656"))
        grid.add_column(justify="right", style=Style(color="#00C9A7"))
        grid.add_row(
            "🧩 [#00C9A7 bold]Tic Tac Toe[/] by [u #0097E6 link=https://www.linkedin.com/in/proatik]ProAtik[/]",
            date_time
        )

        return Panel(grid, border_style="#565656")
