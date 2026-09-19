import logging
from rich import box
from rich.console import Console
from rich.table import Table

from LibraryManagement.utils.logging_config import LOGGER

console = Console()


def prompt_field(prompt, field_name, allow_empty=False, *, validator=None, error_message=None):
    while True:
        value = input(prompt).strip()

        if not allow_empty and not value:
            console.print(f"\n[bold yellow]⚠️ {field_name} không được để trống.[/bold yellow]")
            LOGGER.warning("%s is empty", field_name)
            return None

        if validator is not None:
            try:
                validator(value)
            except ValueError as exc:
                message = error_message or str(exc)
                console.print(f"\n[bold red]❌ {message}[/bold red]")
                LOGGER.warning("Invalid input for %s: %s", field_name, value)
                continue

        return value


def prompt_int(prompt, field_name, *, min_value=None, max_value=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            console.print(f"\n[bold red]❌ {field_name} phải là số nguyên.[/bold red]")
            LOGGER.warning("Invalid integer input for %s: %s", field_name, raw)
            continue

        if min_value is not None and value < min_value:
            console.print(f"\n[bold red]❌ {field_name} phải >= {min_value}.[/bold red]")
            LOGGER.warning("Input for %s below minimum: %s", field_name, value)
            continue

        if max_value is not None and value > max_value:
            console.print(f"\n[bold red]❌ {field_name} phải <= {max_value}.[/bold red]")
            LOGGER.warning("Input for %s above maximum: %s", field_name, value)
            continue

        return value


def prompt_optional_int(prompt, field_name):
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None

        try:
            return int(raw)
        except ValueError:
            console.print(f"\n[bold red]❌ {field_name} phải là số nguyên.[/bold red]")
            LOGGER.warning("Invalid optional integer input for %s: %s", field_name, raw)


def create_book_table(title, *, show_index=False):
    table = Table(
        title=title,
        header_style="bold white",
        border_style="green",
        box=box.SQUARE_DOUBLE_HEAD,
        show_lines=True,
        title_justify="left",
        pad_edge=False,
    )
    if show_index:
        table.add_column("STT", justify="center", style="bold cyan", no_wrap=True)
    table.add_column("MÃ SÁCH", justify="center", style="bold green", no_wrap=True)
    table.add_column("TÊN SÁCH", style="bold white")
    table.add_column("TÁC GIẢ", style="bold yellow")
    table.add_column("NĂM", justify="center", style="bold blue")
    table.add_column("SL", justify="center", style="bold magenta")
    table.add_column("TÌNH TRẠNG", justify="center", no_wrap=True)
    return table


def add_book_to_table(table, book, *, index=None, status=None):
    status_styles = {
        "Có sẵn": "[bold green]Có sẵn[/bold green]",
        "Hết": "[bold yellow]Hết[/bold yellow]",
    }
    display_status = status_styles.get(status, str(status or "-"))

    row = [
        str(book.book_id),
        str(book.title),
        str(book.author),
        str(book.publish_year),
        str(book.quantity),
        display_status,
    ]
    if index is not None:
        row.insert(0, str(index))
    table.add_row(*row)


def print_info_success(message):
    console.print(f"\n[bold green]✅ {message}[/bold green]")
    LOGGER.info(message)


def print_info_warning(message):
    console.print(f"\n[bold yellow]⚠️ {message}[/bold yellow]")
    LOGGER.warning(message)


def print_info_error(message):
    console.print(f"\n[bold red]❌ {message}[/bold red]")
    LOGGER.error(message)
