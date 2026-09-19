from rich.console import Console
from rich.panel import Panel


class BaseView:
    def __init__(self, service):
        self.service = service
        self.console = Console()

    @staticmethod
    def get_accent_color(label):
        colors = {
            "book": "green",
            "borrow": "cyan",
            "return": "blue",
            "search": "magenta",
            "reader": "yellow",
            "tree": "bright_magenta",
            "list": "bright_cyan",
            "sort": "bright_green",
            "default": "cyan",
        }
        lowered = label.lower()
        for key, value in colors.items():
            if key in lowered:
                return value
        return colors["default"]

    def pause(self):
        try:
            input("\n👉 Nhấn Enter để tiếp tục...")
        except (EOFError, KeyboardInterrupt):
            return

    def show_section(self, title):
        accent = self.get_accent_color(title)
        self.console.print(
            Panel.fit(
                f"[bold white]{title}[/bold white]",
                border_style=accent,
                title="[bold white]MỤC[/bold white]",
                title_align="left",
                padding=(0, 2),
            )
        )

    def confirm_action(self, message):
        while True:
            choice = input(f"\n{message} (Y/N): ").strip().upper()
            if choice == "Y":
                return True
            if choice == "N":
                self.console.print("\n[bold yellow]↩️ Bạn đã hủy thao tác.[/bold yellow]")
                self.pause()
                return False
            self.console.print("\n[bold red]⚠️ Vui lòng chỉ nhập Y hoặc N![/bold red]")

    def render_menu(self, title, options, accent=None):
        accent = accent or self.get_accent_color(title)
        self.console.print()
        self.console.print(
            Panel(
                options,
                width=78,
                border_style=accent,
                expand=False,
                padding=(1, 2),
                title=f"[bold {accent}]{title}[/bold {accent}]",
                subtitle="[bold white]Library Management[/bold white]",
                title_align="left",
            )
        )

    def invalid_choice(self):
        self.console.print("\n[bold red]⚠️ Lựa chọn không hợp lệ![/bold red]")
        self.pause()

    def handle_action_error(self, error):
        self.console.print(
            f"\n[bold red]❌ Không thể hoàn thành thao tác: {error}[/bold red]"
        )
        self.pause()

    def prompt_choice(self, prompt_text="\n👉 Nhập lựa chọn: "):
        return input(prompt_text).strip()

    def _resolve_menu_action(self, actions, choice):
        """Return the action bound to the current menu choice, or a sentinel for invalid input."""
        if choice == "0":
            return None

        action = actions.get(choice)
        if action is None:
            self.invalid_choice()
            return "__invalid__"
        return action

    def run_menu(self, show_menu, actions):
        while True:
            show_menu()
            choice = self.prompt_choice()
            action = self._resolve_menu_action(actions, choice)

            if action is None:
                return
            if action == "__invalid__":
                continue

            try:
                action()
            except (OSError, ValueError) as error:
                self.handle_action_error(error)
