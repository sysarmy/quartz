import argparse
import multitasking
import sys

from rich.align import Align
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from quartz.layout import get_layout
from quartz.helpers import HostPinguer
from quartz.utils import get_default_gateway
from time import sleep
from rich.live import Live

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quartz by Sysarmy")
    parser.add_argument(
        "-t",
        "--time",
        metavar="sec",
        type=int,
        default=10,
        help="segundos que querés que corra Quartz (default=10)",
    )
    args = parser.parse_args()

    layout = get_layout()

    job_progress = Progress()
    job_progress.add_task("Ping")

    total = sum(task.total for task in job_progress.tasks)
    overall_progress = Progress(
        SpinnerColumn(),
        BarColumn(complete_style="green"),
        TextColumn("{task.percentage:>3.0f}%"),
    )
    overall_task = overall_progress.add_task("Ping", total=int(total))
    progress_table = Align.center(Panel(overall_progress))

    one = HostPinguer(get_default_gateway(), int(args.time))
    two = HostPinguer("auth.afip.gob.ar", int(args.time))
    three = HostPinguer("cdn.netflix.com", int(args.time))
    four = HostPinguer("ec2.us-east-1.amazonaws.com", int(args.time))

    layout["progress"].update(progress_table)
    layout["analysis"].update(Align.center(
        "En progreso...", vertical="middle"))

    with Live(layout, refresh_per_second=4) as live:
        one.ping()
        two.ping()
        three.ping()
        four.ping()

        while not overall_progress.finished:
            refresh_interval = 0.25

            for job in job_progress.tasks:
                if not job.finished:
                    job_progress.advance(
                        job.id, advance=refresh_interval * 100 / int(args.time)
                    )

            completed = sum(task.completed for task in job_progress.tasks)
            overall_progress.update(overall_task, completed=completed)
            layout["upper_left"].update(
                Panel(
                    Align.center(str(one.get_status()), vertical="middle"),
                    title="[bold]Tu router[/bold]",
                    border_style=one.get_status_color(),
                )
            )
            layout["upper_right"].update(
                Panel(
                    Align.center(str(two.get_status()), vertical="middle"),
                    title=two.get_host(),
                    border_style=one.get_status_color(),
                )
            )
            layout["lower_left"].update(
                Panel(
                    Align.center(str(three.get_status()), vertical="middle"),
                    title=three.get_host(),
                    border_style=one.get_status_color(),
                )
            )
            layout["lower_right"].update(
                Panel(
                    Align.center(str(four.get_status()), vertical="middle"),
                    title=four.get_host(),
                    border_style=one.get_status_color(),
                )
            )
            live.update(layout)
            sleep(refresh_interval)

        if overall_progress.finished:
            live.stop()
