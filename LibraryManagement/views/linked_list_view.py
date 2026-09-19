from rich.table import Table

from LibraryManagement.utils.ui_helpers import prompt_field
from LibraryManagement.views.base_view import BaseView


class LinkedListView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] 📋 Hiển thị danh sách sách\n"
            " [2] 🔍 Tìm sách theo mã bằng Linked List\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🔗 QUẢN LÝ LINKED LIST", menu_content)

    def create_book_table(self, title="📚 DANH SÁCH SÁCH"):
        table = Table(title=title, header_style="bold magenta", border_style="blue")
        for column in ("MÃ SÁCH", "TÊN SÁCH", "TÁC GIẢ", "NĂM", "SL"):
            table.add_column(column, justify="center" if column in {"MÃ SÁCH", "NĂM", "SL"} else "left")
        return table

    def add_book_to_table(self, table, book):
        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity),
        )

    def display_books(self):
        self.console.print("\n[bold cyan]===== 📋 DANH SÁCH SÁCH - LINKED LIST =====[/bold cyan]")
        books = self.service.get_linked_list_books()
        if not books:
            self.console.print("\n[bold yellow]📭 Thư viện chưa có sách.[/bold yellow]")
            self.pause()
            return

        table = self.create_book_table("📋 DANH SÁCH SÁCH - LINKED LIST")
        for book in books:
            self.add_book_to_table(table, book)
        self.console.print(table)
        self.pause()

    def search_book(self):
        self.console.print("\n[bold cyan]===== 🔍 TÌM SÁCH BẰNG LINKED LIST =====[/bold cyan]")
        book_id = prompt_field("👉 Nhập mã sách cần tìm: ", "Mã sách")
        if book_id is None:
            self.pause()
            return

        book = self.service.search_book_by_linked_list(book_id)
        if book:
            table = self.create_book_table("🔍 KẾT QUẢ TÌM KIẾM - LINKED LIST")
            self.add_book_to_table(table, book)
            self.console.print(table)
        else:
            self.console.print("\n[bold red]❌ Không tìm thấy sách.[/bold red]")
        self.pause()

    def run(self):
        self.run_menu(
            self.show_menu,
            {"1": self.display_books, "2": self.search_book},
        )
