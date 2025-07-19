import random
import time
from pathlib import Path

import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
from main import scrape_instagram_accounts

console = Console()

# ------------------------------------------------------------------ #
# 1.  Glitchy intro splash                                           #
# ------------------------------------------------------------------ #
GLITCH_FRAMES = [
    r"""
██╗███╗   ██╗███████╗████████╗ █████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║██╔██╗ ██║███████╗   ██║   ███████║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║██║╚██╗██║╚════██║   ██║   ██╔══██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║██║ ╚████║███████║   ██║   ██║  ██║███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                          
"""
]


console.clear()
for _ in range(20):
    frame = random.choice(GLITCH_FRAMES)
    console.print(Align.center(Text(frame, style="bold bright_cyan")), height=15)
    time.sleep(0.08)
    console.clear()
console.print(
    Align.center(
        Panel(
            "Instagram Account Finder \n[dim]v1.0  |  powered by TronOnly[/dim]",
            border_style="bright_magenta",
        )
    )
)
time.sleep(1.2)

console.print("\n[bold yellow]🔮  Initiating sequence…[/bold yellow]\n")

niche = Prompt.ask(
    "[bold green]Niche / keyword[/bold green] (e.g. [cyan]Basketball[/cyan])",
    default="Basketball",
)

pages = click.IntRange(1, 99)(
    Prompt.ask(
        "[bold green]Pages to scrape[/bold green]  [dim](≈ 10 accs/page)[/dim]",
        default="3",
    )
)

fmt = Prompt.ask(
    "[bold green]Export format[/bold green]",
    choices=["json", "csv", "txt"],
    default="json",
)

out_stem = Prompt.ask(
    "[bold green]File name[/bold green]",
    default=niche.replace(" ", "_"),
)

headless = Confirm.ask(
    "[bold green]Headless mode?[/bold green]  [dim](no browser window)[/dim]",
    default=True,
)


console.print("\n[bold red]🚀  IGNITION…[/bold red]\n")

with Live(
    Spinner("bouncingBall", text="[red]Doing your dirty work...[/red]"),
    refresh_per_second=12,
    console=console,
):
    scrape_instagram_accounts(
        niche=niche,
        max_pages=pages,
        headless=headless,
        output_path=str(Path(out_stem)),
        format=fmt.lower(),
    )

console.print(
    f"\n[bold green]🎉  Mission complete![/bold green]  "
    f"Artifact dropped → [cyan underline]{Path.cwd() / (out_stem + '.' + fmt.lower())}[/cyan underline]"
)
