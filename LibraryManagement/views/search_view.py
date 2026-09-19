from rich import box
from rich.table import Table

from LibraryManagement.utils.ui_helpers import prompt_field, prompt_optional_int
from LibraryManagement.views.base_view import BaseView


class SearchView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] 🔤 Tìm theo tên sách\n"
            " [2] ✍️  Tìm theo tác giả\n"
            " [3] 🔎 Tìm kiếm nâng cao\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🔍 TÌM KIẾM SÁCH", menu_content, accent="magenta")

    def display_results(self, results):
        if not results:
            self.console.print("\n[bold red]❌ Không tìm thấy sách phù hợp.[/bold red]")
            return

        table = Table(
            title="🔍 KẾT QUẢ TÌM KIẾM",
            header_style="bold magenta",
            border_style="blue",
            box=box.SIMPLE_HEAVY,
            show_lines=True,
        )
        for column in ("MÃ SÁCH", "TÊN SÁCH", "TÁC GIẢ", "THỂ LOẠI", "NĂM", "ISBN", "TRẠNG THÁI", "SL"):
            table.add_column(column, justify="center" if column in {"MÃ SÁCH", "NĂM", "TRẠNG THÁI", "SL"} else "left")

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

        self.console.print(table)
        self.console.print(f"\n[bold green]✅ Tìm thấy {len(results)} sách.[/bold green]")

    def search_by_title(self):
        self.console.print("\n[bold cyan]===== 🔤 TÌM KIẾM THEO TÊN =====[/bold cyan]")
        keyword = prompt_field("👉 Nhập tên sách cần tìm: ", "Tên sách")
        if keyword is None:
            self.pause()
            return
        self.display_results(self.service.search_books_by_title(keyword))
        self.pause()

    def search_by_author(self):
        self.console.print("\n[bold cyan]===== ✍️ TÌM KIẾM THEO TÁC GIẢ =====[/bold cyan]")
        author = prompt_field("👉 Nhập tên tác giả cần tìm: ", "Tên tác giả")
        if author is None:
            self.pause()
            return
        self.display_results(self.service.search_books_by_author(author))
        self.pause()

    def search_advanced(self):
        self.console.print("\n[bold cyan]===== 🔎 TÌM KIẾM NÂNG CAO =====[/bold cyan]")
        title = prompt_field("👉 Tên sách (Enter để bỏ qua): ", "Tên sách", allow_empty=True) or None
        author = prompt_field("👉 Tác giả (Enter để bỏ qua): ", "Tác giả", allow_empty=True) or None
        genre = prompt_field("👉 Thể loại (Enter để bỏ qua): ", "Thể loại", allow_empty=True) or None
        publish_year = prompt_optional_int(
            "👉 Năm xuất bản (Enter để bỏ qua): ",
            "Năm xuất bản",
        )
        isbn = prompt_field("👉 ISBN (Enter để bỏ qua): ", "ISBN", allow_empty=True) or None
        availability = prompt_field(
            "👉 Tình trạng [all/available/unavailable] (mặc định all): ",
            "Tình trạng",
            allow_empty=True,
        ) or "all"

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

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.search_by_title,
                "2": self.search_by_author,
                "3": self.search_advanced,
            },
        )
