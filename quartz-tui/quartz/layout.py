from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich import box


def get_layout():
    """
    Return a Layout object that represents the layout structure of the console application.
    """
    layout = Layout()

    layout.split_column(
        Layout(name="title"),
        Layout(name="upper", ratio=4),
        Layout(name="lower", ratio=4),
        Layout(name="bar"),
    )

    layout["upper"].split_row(
        Layout(name="upper_left"),
        Layout(name="upper_right"),
    )
    layout["lower"].split_row(
        Layout(name="lower_left"),
        Layout(name="lower_right"),
    )
    layout["bar"].split_row(
        Layout(name="progress"),
        Layout(name="analysis"),
    )

    layout["title"].update(
        Panel(
            Align.center(
                ":magnifying_glass_tilted_left: [bold]Quartz[/bold] by [bold][link=https://sysarmy.com/]Sysarmy[/link][/bold] :globe_with_meridians:",
                vertical="middle",
            ),
            subtitle="v0.0.1-alpha",
            box=box.DOUBLE,
        )
    )

    return layout
