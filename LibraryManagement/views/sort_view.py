from rich.table import Table

from LibraryManagement.views.base_view import BaseView

from LibraryManagement.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort
)

from LibraryManagement.algorithms.benchmark import run_benchmark


class SortView(BaseView):

    # ============================================================
    # KHỞI TẠO SORT VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU SẮP XẾP
    # ============================================================

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

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # CHỌN TIÊU CHÍ SẮP XẾP
    # ============================================================

    def choose_key(self):

        self.console.print(
            "\n[bold cyan]===== 🔑 TIÊU CHÍ SẮP XẾP =====[/bold cyan]"
        )

        # Tạo bảng lựa chọn tiêu chí
        table = Table(
            header_style="bold magenta",
            border_style="blue"
        )

        table.add_column(
            "STT",
            justify="center",
            style="cyan"
        )

        table.add_column(
            "TIÊU CHÍ",
            style="green"
        )

        table.add_row(
            "1",
            "Sắp xếp theo tên sách"
        )

        table.add_row(
            "2",
            "Sắp xếp theo năm xuất bản"
        )

        self.console.print(table)

        # Nhập lựa chọn
        choice = self.prompt_choice()

        if choice == "1":
            return "title"

        elif choice == "2":
            return "publish_year"

        else:
            self.console.print(
                "\n[bold red]⚠️ Lựa chọn không hợp lệ![/bold red]"
            )

            self.pause()

            return None

    # ============================================================
    # TẠO BẢNG HIỂN THỊ SÁCH
    # ============================================================

    def create_book_table(self, title):

        # Tạo bảng Rich
        table = Table(
            title=title,
            header_style="bold magenta",
            border_style="blue"
        )

        # Cột mã sách
        table.add_column(
            "MÃ SÁCH",
            justify="center",
            style="cyan",
            no_wrap=True
        )

        # Cột tên sách
        table.add_column(
            "TÊN SÁCH",
            style="green"
        )

        # Cột tác giả
        table.add_column(
            "TÁC GIẢ",
            style="yellow"
        )

        # Cột năm xuất bản
        table.add_column(
            "NĂM",
            justify="center"
        )

        # Cột số lượng
        table.add_column(
            "SL",
            justify="center"
        )

        return table

    # ============================================================
    # THÊM SÁCH VÀO BẢNG
    # ============================================================

    def add_book_to_table(self, table, book):

        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity)
        )

    # ============================================================
    # SẮP XẾP SÁCH
    # ============================================================

    def sort_books(self, algorithm, algorithm_name):

        # Lấy toàn bộ sách từ Service
        books = self.service.get_all_books()

        # Kiểm tra thư viện có sách hay không
        if not books:
            self.console.print(
                "\n[bold yellow]📭 Thư viện chưa có sách.[/bold yellow]"
            )

            self.pause()
            return

        # Cho người dùng chọn tiêu chí sắp xếp
        key = self.choose_key()

        # Nếu lựa chọn không hợp lệ thì kết thúc
        if key is None:
            return

        # Gọi thuật toán sắp xếp
        result, comparisons, assignments = algorithm(
            books,
            key
        )

        # --------------------------------------------------------
        # HIỂN THỊ KẾT QUẢ
        # --------------------------------------------------------

        self.console.print(
            f"\n[bold cyan]===== 📊 KẾT QUẢ {algorithm_name.upper()} =====[/bold cyan]"
        )

        # Tạo bảng kết quả
        table = self.create_book_table(
            f"📊 KẾT QUẢ {algorithm_name.upper()}"
        )

        # Thêm từng sách sau khi sắp xếp vào bảng
        for book in result:
            self.add_book_to_table(table, book)

        # Hiển thị bảng
        self.console.print()
        self.console.print(table)

        # --------------------------------------------------------
        # HIỂN THỊ THỐNG KÊ
        # --------------------------------------------------------

        stats_table = Table(
            title="📈 THỐNG KÊ THUẬT TOÁN",
            header_style="bold magenta",
            border_style="blue"
        )

        stats_table.add_column(
            "CHỈ SỐ",
            style="cyan"
        )

        stats_table.add_column(
            "GIÁ TRỊ",
            justify="center",
            style="green"
        )

        # Số phép so sánh
        stats_table.add_row(
            "Số phép so sánh",
            str(comparisons)
        )

        # Số phép gán
        stats_table.add_row(
            "Số phép gán",
            str(assignments)
        )

        self.console.print()
        self.console.print(stats_table)

        self.pause()

    # ============================================================
    # CHẠY MENU SẮP XẾP
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": lambda: self.sort_books(bubble_sort, "Bubble Sort"),
                "2": lambda: self.sort_books(selection_sort, "Selection Sort"),
                "3": lambda: self.sort_books(insertion_sort, "Insertion Sort"),
                "4": lambda: self.sort_books(quick_sort, "Quick Sort"),
                "5": lambda: self.sort_books(merge_sort, "Merge Sort"),
                "6": lambda: self.sort_books(heap_sort, "Heap Sort"),
                "7": self.run_benchmark,
            },
        )

    def run_benchmark(self):
        self.show_section("===== 📊 SO SÁNH HIỆU NĂNG =====")
        run_benchmark()
        self.pause()