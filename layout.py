# ---- rich ---- #
from rich.layout import Layout


def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )

    layout["main"].split_row(
        Layout(name="instructions", ratio=2),
        Layout(name="board", ratio=1),
    )

    return layout
