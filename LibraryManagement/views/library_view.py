from datetime import date

from rich import box
from rich.panel import Panel
from rich.table import Table

from LibraryManagement.views.base_view import BaseView
from LibraryManagement.views.book_view import BookView
from LibraryManagement.views.borrow_view import BorrowView
from LibraryManagement.views.reader_view import ReaderView
from LibraryManagement.views.return_view import ReturnView
from LibraryManagement.views.sort_view import SortView
from LibraryManagement.views.search_view import SearchView
from LibraryManagement.views.bst_view import BSTView
from LibraryManagement.views.linked_list_view import LinkedListView
from LibraryManagement.views.report_view import ReportView
from LibraryManagement.services.report_service import ReportService


class LibraryView(BaseView):

    def __init__(self, service):
        super().__init__(service)
        self.borrow_view = BorrowView(service)
        self.reader_view = ReaderView(service)
        self.book_view = BookView(service)
        self.return_view = ReturnView(service)
        self.sort_view = SortView(service)
        self.search_view = SearchView(service)
        self.bst_view = BSTView(service)
        self.linked_list_view = LinkedListView(service)
        self.report_service = ReportService(service)
        self.report_view = ReportView(service)

    def get_dashboard_stats(self):
        stats = self.report_service.get_dashboard_stats()
        return (
            stats["total_books"],
            stats["total_available"],
            stats["current_borrowed"],
            stats["overdue_count"],
            stats["category_counts"],
        )

    def get_time_window_stats(self, days=30, as_of=None):
        return self.report_service.get_time_window_stats(days, as_of)

    def _render_dark_panel(self, body, title, border_color="bright_cyan", accent="white", subtitle=None):
        return Panel(
            body,
            title=f"[bold {accent}]{title}[/bold {accent}]",
            subtitle=subtitle,
            border_style=border_color,
            style="bold black on #070d1b",
            padding=(1, 2),
        )

    def _build_bar_segment(self, value, maximum, width=32):
        if maximum <= 0:
            return "░" * width
        filled = max(1, int((value / maximum) * width)) if value > 0 else 0
        return "█" * filled + "░" * (width - filled)

    def _status_style(self, status):
        mapping = {
            "borrowed": ("[bold cyan]Đang mượn[/bold cyan]", "cyan"),
            "pending": ("[bold yellow]Chờ xử lý[/bold yellow]", "yellow"),
            "returned": ("[bold green]Đã trả[/bold green]", "green"),
            "overdue": ("[bold red]Quá hạn[/bold red]", "red"),
        }
        return mapping.get(status, (f"[bold white]{status}[/bold white]", "white"))

    def get_book_status(self, book):
        overdue_books = {borrower.book_id for borrower in self.service.get_overdue_borrowers()}
        if book.book_id in overdue_books:
            return ("Quá hạn", "bold red", "red")
        if book.quantity > 0:
            return ("Có sẵn", "bold green", "green")
        return ("Hết", "bold yellow", "yellow")

    def get_overdue_queue(self):
        overdue = []
        for borrower in self.service.get_overdue_borrowers():
            try:
                days = (date.today() - date.fromisoformat(borrower.due_date)).days
            except ValueError:
                days = 0
            overdue.append((borrower.borrower_id, borrower.name, borrower.book_id, borrower.due_date, days))
        return sorted(overdue, key=lambda item: item[4], reverse=True)

    def show_welcome_banner(self):
        banner = Panel(
            "[bold white]📚 HỆ THỐNG QUẢN LÝ THƯ VIỆN[/bold white]\n"
            "[bold bright_cyan]Quản lý sách, độc giả, mượn trả và thống kê nhanh[/bold bright_cyan]",
            box=box.DOUBLE,
            border_style="bright_cyan",
            title="[bold white]WELCOME[/bold white]",
            title_align="left",
            padding=(1, 2),
        )
        self.console.print(banner)

    def show_dashboard(self):
        total_books, total_available, current_borrowed, overdue_count, category_counts = self.get_dashboard_stats()
        window_stats = self.get_time_window_stats(days=30)

        filter_panel = self._render_dark_panel(
            "[bold white]BỘ LỌC THỜI GIAN[/bold white]\n"
            "[bold cyan]Hiển thị trong 30 ngày gần nhất[/bold cyan]\n"
            "[bold white]Tổng hoạt động:[/bold white] [bold bright_green]{total_active}[/bold bright_green]"
            .format(total_active=window_stats["total_active"]),
            title="FILTER",
            border_color="bright_magenta",
            accent="bright_magenta",
        )

        self.console.print()
        self.console.print(
            Panel(
                "[bold #7ef9ff]DARK MODE / NEON ADMIN DASHBOARD[/bold #7ef9ff]\n"
                "[bold white]Tổng quan hệ thống thư viện[/bold white]",
                border_style="#22d3ee",
                style="bold black on #040b16",
                padding=(1, 2),
                title="[bold #7ef9ff]ADMIN[/bold #7ef9ff]",
            )
        )

        self.console.print(filter_panel)

        cards = Table.grid(expand=True)
        cards.add_column(justify="center")
        cards.add_column(justify="center")
        cards.add_column(justify="center")

        cards.add_row(
            Panel.fit(f"[bold white]📚 Tổng số sách\n[bold green]{total_books}[/bold green]", border_style="green", style="bold black on #06131b", padding=(1, 3)),
            Panel.fit(f"[bold white]📖 Đang mượn\n[bold cyan]{current_borrowed}[/bold cyan]", border_style="cyan", style="bold black on #06131b", padding=(1, 3)),
            Panel.fit(f"[bold white]⚠️ Quá hạn\n[bold red]{overdue_count}[/bold red]", border_style="red", style="bold black on #06131b", padding=(1, 3)),
        )
        self.console.print()
        self.console.print(cards)

        categories = category_counts or {"Chưa phân loại": 0}
        max_count = max(categories.values()) if categories else 1

        chart_table = Table(
            title="📈 BIỂU ĐỒ CỘT - SÁCH ĐANG MƯỢN THEO THỂ LOẠI",
            header_style="bold white",
            border_style="bright_magenta",
            box=box.HEAVY,
            show_lines=True,
            title_justify="left",
            style="bold black on #0a1020",
        )
        chart_table.add_column("THỂ LOẠI", style="bold white")
        chart_table.add_column("SL", justify="center", style="bold cyan")
        chart_table.add_column("BIỂU ĐỒ", style="bold magenta")

        for name, count in list(categories.items())[:6]:
            chart_table.add_row(name, str(count), self._build_bar_segment(count, max_count, width=30))

        reader_summary = window_stats["reader_summary"]
        reader_table = Table(
            title="👥 THỐNG KÊ THEO ĐỘC GIẢ",
            header_style="bold white",
            border_style="bright_yellow",
            box=box.HEAVY,
            show_lines=True,
            title_justify="left",
            style="bold black on #0b1222",
        )
        reader_table.add_column("ĐỘC GIẢ", style="bold white")
        reader_table.add_column("LẦN MƯỢN", justify="center", style="bold yellow")

        for name, count in list(reader_summary.items())[:5]:
            reader_table.add_row(name, str(count))

        category_summary = window_stats["category_summary"]
        category_table = Table(
            title="📚 THỐNG KÊ THEO THỂ LOẠI",
            header_style="bold white",
            border_style="bright_green",
            box=box.HEAVY,
            show_lines=True,
            title_justify="left",
            style="bold black on #0b1222",
        )
        category_table.add_column("THỂ LOẠI", style="bold white")
        category_table.add_column("SỐ LƯỢNG", justify="center", style="bold green")

        for name, count in list(category_summary.items())[:5]:
            category_table.add_row(name, str(count))

        status_summary = window_stats["status_summary"]
        status_summary_table = Table(
            title="🔄 TÌNH TRẠNG MƯỢN TRẢ",
            header_style="bold white",
            border_style="bright_cyan",
            box=box.HEAVY,
            show_lines=True,
            title_justify="left",
            style="bold black on #0b1222",
        )
        status_summary_table.add_column("TRẠNG THÁI", style="bold white")
        status_summary_table.add_column("SL", justify="center")

        for status, count in status_summary.items():
            label, color = self._status_style(status)
            status_summary_table.add_row(f"[{color}]{label}[/]", str(count))

        overview_table = Table(
            title="📊 TỔNG QUAN THƯ VIỆN",
            header_style="bold white",
            border_style="bright_cyan",
            box=box.SQUARE_DOUBLE_HEAD,
            show_lines=True,
            title_justify="left",
            style="bold black on #0a1020",
        )
        overview_table.add_column("MÃ SÁCH", justify="center", style="bold green")
        overview_table.add_column("TÊN SÁCH", style="bold white")
        overview_table.add_column("TRẠNG THÁI", justify="center")
        overview_table.add_column("SL", justify="center", style="bold magenta")

        books = self.service.get_all_books()[:8]
        for book in books:
            status, style, color_name = self.get_book_status(book)
            overview_table.add_row(book.book_id, book.title, f"[{style}]{status}[/]", str(book.quantity))

        overdue_table = Table(
            title="🧾 QUEUE QUÁ HẠN",
            header_style="bold white",
            border_style="red",
            box=box.HORIZONTALS,
            show_lines=True,
            title_justify="left",
        )
        overdue_table.add_column("MÃ ĐỘC GIẢ", style="bold cyan")
        overdue_table.add_column("TÊN", style="bold white")
        overdue_table.add_column("MÃ SÁCH", style="bold yellow")
        overdue_table.add_column("HẠN TRẢ", style="bold red")
        overdue_table.add_column("SỐ NGÀY", style="bold magenta")

        overdue_rows = self.get_overdue_queue()
        if overdue_rows:
            for borrower_id, name, book_id, due_date, days in overdue_rows[:5]:
                overdue_table.add_row(borrower_id, name, book_id, due_date, str(days))
        else:
            overdue_table.add_row("-", "Không có", "-", "-", "0")

        status_table = Table(
            title="🟢 TRẠNG THÁI HỆ THỐNG",
            header_style="bold white",
            border_style="bright_green",
            box=box.SIMPLE,
            show_lines=True,
            title_justify="left",
        )
        status_table.add_column("KHU VỰC", style="bold white")
        status_table.add_column("TRẠNG THÁI", justify="center")

        if overdue_count == 0:
            status_table.add_row("Hệ thống", "[bold green]Ổn định[/bold green]")
        elif overdue_count <= 3:
            status_table.add_row("Hệ thống", "[bold yellow]Cần chú ý[/bold yellow]")
        else:
            status_table.add_row("Hệ thống", "[bold red]Nguy hiểm[/bold red]")

        status_table.add_row("Sách mới", "[bold green]Sẵn sàng[/bold green]")
        status_table.add_row("Mượn trả", "[bold cyan]Đang hoạt động[/bold cyan]")
        status_table.add_row("Quá hạn", "[bold red]Cần xử lý[/bold red]")

        self.console.print()
        self.console.print(chart_table)
        self.console.print()
        self.console.print(reader_table)
        self.console.print()
        self.console.print(category_table)
        self.console.print()
        self.console.print(status_summary_table)
        self.console.print()
        self.console.print(overview_table)
        self.console.print()
        self.console.print(overdue_table)
        self.console.print()
        self.console.print(status_table)
        self.console.print(f"\n[bold bright_green]✅ Sẵn có: {total_available} cuốn[/bold bright_green]")

    def show_menu(self):
        menu_content = (
            "[bold white]HỆ THỐNG QUẢN LÝ THƯ VIỆN[/bold white]\n\n"
            " [1] 📖 Quản lý sách\n"
            " [2] 👤 Quản lý mượn sách\n"
            " [3] ↩️  Quản lý trả sách\n"
            " [4] 🔍 Tìm kiếm sách\n"
            " [5] 🌳 Tìm sách bằng BST\n"
            " [6] 🔗 Hiển thị Linked List\n"
            " [7] 📊 Sắp xếp sách\n"
            " [8] 👥 Quản lý độc giả\n"
            " [9] 📊 Báo cáo & thống kê\n"
            " [0] 🚪 Thoát chương trình"
        )
        self.render_menu("📚 LIBRARY MANAGEMENT SYSTEM", menu_content, accent="bright_cyan")

    def run(self):
        self.show_welcome_banner()
        self.show_dashboard()
        self.run_menu(
            self.show_menu,
            {
                "1": self.book_view.run,
                "2": self.borrow_view.run,
                "3": self.return_view.run,
                "4": self.search_view.run,
                "5": self.bst_view.run,
                "6": self.linked_list_view.run,
                "7": self.sort_view.run,
                "8": self.reader_view.run,
                "9": self.report_view.run,
            },
        )
        self.console.print("\n[bold green]👋 Cảm ơn bạn đã sử dụng hệ thống![/bold green]")
