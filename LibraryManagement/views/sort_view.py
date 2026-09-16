from rich.table import Table

from LibraryManagement.views.base_view import BaseView
from LibraryManagement.algorithms.sort_strategy import (
    BubbleSortStrategy,
    SelectionSortStrategy,
    InsertionSortStrategy,
    QuickSortStrategy,
    MergeSortStrategy,
    HeapSortStrategy,
)
from LibraryManagement.algorithms.benchmark import run_benchmark


class SortView(BaseView):

    def __init__(self, service):
        super().__init__(service)

    def show_menu(self):
        menu_content = (
            " [1] 🔵 Bubble Sort\n"
            " [2] 🟢 Selection Sort\n"
            " [3] 🟡 Insertion Sort\n"
            " [4] 🔴 Quick Sort\n"
            " [5] 🟣 Merge Sort\n"
            " [6] 🟠 Heap Sort\n"
            " [7] 📊 So sánh hiệu năng các thuật toán\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("📊 SẮP XẾP SÁCH", menu_content)

    def choose_key(self):
        self.console.print(
            "\n[bold cyan]===== 🔑 TIÊU CHÍ SẮP XẾP =====[/bold cyan]"
        )

        table = Table(header_style="bold magenta", border_style="blue")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("TIÊU CHÍ", style="green")
        table.add_row("1", "Sắp xếp theo tên sách")
        table.add_row("2", "Sắp xếp theo năm xuất bản")
        self.console.print(table)

        choice = self.prompt_choice()
        if choice == "1":
            return "title"
        if choice == "2":
            return "publish_year"

        self.console.print("\n[bold red]⚠️ Lựa chọn không hợp lệ![/bold red]")
        self.pause()
        return None

    def create_book_table(self, title):
        table = Table(
            title=title,
            header_style="bold magenta",
            border_style="blue",
        )
        table.add_column("MÃ SÁCH", justify="center", style="cyan", no_wrap=True)
        table.add_column("TÊN SÁCH", style="green")
        table.add_column("TÁC GIẢ", style="yellow")
        table.add_column("NĂM", justify="center")
        table.add_column("SL", justify="center")
        return table

    def add_book_to_table(self, table, book):
        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity),
        )

    def sort_books(self, strategy):
        books = self.service.get_all_books()
        if not books:
            self.console.print("\n[bold yellow]📭 Thư viện chưa có sách.[/bold yellow]")
            self.pause()
            return

        key = self.choose_key()
        if key is None:
            return

        result, comparisons, assignments = strategy.sort(books, key)

        self.console.print(
            f"\n[bold cyan]===== 📊 KẾT QUẢ {strategy.name.upper()} =====[/bold cyan]"
        )
        table = self.create_book_table(f"📊 KẾT QUẢ {strategy.name.upper()}")
        for book in result:
            self.add_book_to_table(table, book)

        self.console.print()
        self.console.print(table)

        stats_table = Table(
            title="📈 THỐNG KÊ THUẬT TOÁN",
            header_style="bold magenta",
            border_style="blue",
        )
        stats_table.add_column("CHỈ SỐ", style="cyan")
        stats_table.add_column("GIÁ TRỊ", justify="center", style="green")
        stats_table.add_row("Số phép so sánh", str(comparisons))
        stats_table.add_row("Số phép gán", str(assignments))
        self.console.print()
        self.console.print(stats_table)
        self.pause()

    def run(self):
        strategies = {
            "1": BubbleSortStrategy(),
            "2": SelectionSortStrategy(),
            "3": InsertionSortStrategy(),
            "4": QuickSortStrategy(),
            "5": MergeSortStrategy(),
            "6": HeapSortStrategy(),
        }
        self.run_menu(
            self.show_menu,
            {
                choice: (lambda strategy=strategy: self.sort_books(strategy))
                for choice, strategy in strategies.items()
            }
            | {"7": self.run_benchmark},
        )

    def run_benchmark(self):
        self.show_section("===== 📊 SO SÁNH HIỆU NĂNG =====")
        run_benchmark()
        self.pause()
