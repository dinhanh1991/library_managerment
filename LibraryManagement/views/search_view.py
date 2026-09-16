from rich import box
from rich.table import Table

from LibraryManagement.views.base_view import BaseView

class SearchView(BaseView):

    # ============================================================
    # KHỞI TẠO SEARCH VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU TÌM KIẾM
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] 🔤 Tìm theo tên sách\n"
            " [2] ✍️  Tìm theo tác giả\n"
            " [3] 🔎 Tìm kiếm nâng cao\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🔍 TÌM KIẾM SÁCH", menu_content, accent="magenta")

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # HIỂN THỊ KẾT QUẢ TÌM KIẾM
    # ============================================================

    def display_results(self, results):

        # Nếu không có kết quả
        if not results:

            self.console.print(
                "\n[bold red]"
                "❌ Không tìm thấy sách phù hợp."
                "[/bold red]"
            )

            return

        # Tạo bảng kết quả
        table = Table(
            title="🔍 KẾT QUẢ TÌM KIẾM",
            header_style="bold magenta",
            border_style="blue",
            box=box.SIMPLE_HEAVY,
            show_lines=True,
        )

        table.add_column("MÃ SÁCH", justify="center", style="cyan", no_wrap=True)
        table.add_column("TÊN SÁCH", style="green")
        table.add_column("TÁC GIẢ", style="yellow")
        table.add_column("THỂ LOẠI", style="blue")
        table.add_column("NĂM", justify="center")
        table.add_column("ISBN", style="white")
        table.add_column("TRẠNG THÁI", justify="center")
        table.add_column("SL", justify="center")

        for book in results:
            status = "Có sẵn" if book.quantity > 0 else "Đang hết"
            table.add_row(
                str(book.book_id),
                str(book.title),
                str(book.author),
                str(getattr(book, "category", "")),
                str(book.publish_year),
                str(getattr(book, "isbn", "")),
                status,
                str(book.quantity),
            )

        self.console.print()
        self.console.print(table)

        self.console.print(
            f"\n[bold green]"
            f"✅ Tìm thấy {len(results)} sách."
            f"[/bold green]"
        )

    # ============================================================
    # TÌM KIẾM THEO TÊN SÁCH
    # ============================================================

    def search_by_title(self):

        self.console.print(
            "\n[bold cyan]===== 🔤 TÌM KIẾM THEO TÊN =====[/bold cyan]"
        )

        # Nhập từ khóa
        keyword = input(
            "👉 Nhập tên sách cần tìm: "
        ).strip()

        # Kiểm tra từ khóa
        if not keyword:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Tên sách không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Gọi Service tìm sách theo tên
        results = self.service.search_books_by_title(
            keyword
        )

        # Hiển thị kết quả
        self.display_results(results)

        self.pause()

    # ============================================================
    # TÌM KIẾM THEO TÁC GIẢ
    # ============================================================

    def search_by_author(self):

        self.console.print(
            "\n[bold cyan]===== ✍️ TÌM KIẾM THEO TÁC GIẢ =====[/bold cyan]"
        )

        # Nhập tên tác giả
        author = input(
            "👉 Nhập tên tác giả cần tìm: "
        ).strip()

        # Kiểm tra dữ liệu nhập
        if not author:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Tên tác giả không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Gọi Service tìm sách theo tác giả
        results = self.service.search_books_by_author(
            author
        )

        # Hiển thị kết quả
        self.display_results(results)

        self.pause()

    # ============================================================
    # TÌM KIẾM NÂNG CAO
    # ============================================================

    def search_advanced(self):
        self.console.print("\n[bold cyan]===== 🔎 TÌM KIẾM NÂNG CAO =====[/bold cyan]")

        title = input("👉 Tên sách (để trống nếu không muốn lọc): ").strip() or None
        author = input("👉 Tác giả (để trống nếu không muốn lọc): ").strip() or None
        genre = input("👉 Thể loại (để trống nếu không muốn lọc): ").strip() or None
        publish_year = input("👉 Năm xuất bản (để trống nếu không muốn lọc): ").strip() or None
        isbn = input("👉 ISBN (để trống nếu không muốn lọc): ").strip() or None
        availability = input("👉 Tình trạng [all/available/unavailable] (mặc định all): ").strip().lower() or "all"

        if availability not in {"all", "available", "unavailable"}:
            self.console.print("\n[bold yellow]⚠️ Tình trạng không hợp lệ. Hiển thị tất cả kết quả.[/bold yellow]")
            availability = "all"

        results = self.service.search_books_advanced(
            title=title,
            author=author,
            genre=genre,
            publish_year=publish_year,
            isbn=isbn,
            availability=availability,
        )

        self.display_results(results)
        self.pause()

    # ============================================================
    # CHẠY CHƯƠNG TRÌNH
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.search_by_title,
                "2": self.search_by_author,
                "3": self.search_advanced,
            },
        )
