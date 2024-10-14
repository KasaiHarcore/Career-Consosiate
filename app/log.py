import time
from collections.abc import Callable
from os import get_terminal_size

from loguru import logger
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

welcome_message_chat = """
Welcome to the C&C, this is a demo for AI in HR.
"""

def terminal_width():
    return get_terminal_size().columns

WIDTH = min(120, terminal_width() - 10)

console = Console()

print_stdout = True


def log_exception(exception):
    logger.exception(exception)


def print_banner(msg: str) -> None:
    if not print_stdout:
        return

    banner = f" {msg} ".center(WIDTH, "=")
    console.print()
    console.print(banner, style="bold")
    console.print()
        
def print_user(
    msg: str, desc = "", print_callback: Callable[[dict], None] | None = None
) -> None:
    if not print_stdout:
        return

    name = "Request"
    if desc:
        title = f"{name} ({desc})"
    else:
        title = name

    panel = Panel(
        msg,
        title=title,
        title_align="left",
        border_style="green",
        width=WIDTH,
    )
    console.print(panel)

    if print_callback:
        print_callback(
            {"title": f"{name} ({desc})", "message": msg, "category": "user"}
        
)
        
def print_output(
    msg: str, desc = "", print_callback: Callable[[dict], None] | None = None
) -> None:
    if not print_stdout:
        return

    markdown = Markdown(msg)

    name = "Output"
    if desc:
        title = f"{name} ({desc})"
    else:
        title = name

    panel = Panel(
        markdown,
        title = title,
        title_align = "left",
        border_style = "cyan",
        width=WIDTH,
    )
    console.print(panel)

    if print_callback:
        print_callback(
            {"title": f"{name} ({desc})", "message": msg, "category": "output"}
        )


def print_llm(
    msg: str, desc="", print_callback: Callable[[dict], None] | None = None
) -> None:
    if not print_stdout:
        return

    markdown = Markdown(msg)

    name = "Agent"
    if desc:
        title = f"{name} ({desc})"
    else:
        title = name

    panel = Panel(
        markdown,
        title=title,
        title_align = "left",
        border_style = "blue",
        width=WIDTH,
    )
    console.print(panel)
    if print_callback:
        print_callback(
            {
                "title": f"{name} ({desc})",
                "message": msg,
                "category": "LLM",
            }
        )


def log_and_print(msg):
    logger.info(msg)
    if print_stdout:
        console.print(msg)


def log_and_cprint(msg, **kwargs):
    logger.info(msg)
    if print_stdout:
        console.print(msg, **kwargs)


def log_and_always_print(msg):
    """
    A mode which always print to stdout, no matter what.
    Useful when running multiple tasks and we just want to see the important information.
    """
    logger.info(msg)
    # always include time for important messages
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    console.print(f"\n[{t}] {msg}")


def print_with_time(msg):
    """
    Print a msg to console with timestamp.
    """
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    console.print(f"\n[{t}] {msg}")
