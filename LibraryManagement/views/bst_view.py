from rich.table import Table

from LibraryManagement.utils.ui_helpers import prompt_field
from LibraryManagement.views.base_view import BaseView


class BSTView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] 🔍 Tìm sách theo mã bằng BST\n"
            " [2] 📋 Duyệt Inorder\n"
            " [3] 📋 Duyệt Preorder\n"
            " [4] 📋 Duyệt Postorder\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🌳 QUẢN LÝ BST", menu_content)

    def display_book(self, book):
        table = Table(
            title="📚 KẾT QUẢ TÌM KIẾM",
            header_style="bold magenta",
            border_style="blue",
        )
        for column in ("MÃ SÁCH", "TÊN SÁCH", "TÁC GIẢ", "NĂM", "SL"):
            table.add_column(column, justify="center" if column in {"MÃ SÁCH", "NĂM", "SL"} else "left")
        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity),
        )
        self.console.print(table)

    def search_book(self):
        self.console.print("\n[bold cyan]===== 🔍 TÌM SÁCH BẰNG BST =====[/bold cyan]")
        book_id = prompt_field("👉 Nhập mã sách cần tìm: ", "Mã sách")
        if book_id is None:
            self.pause()
            return

        book = self.service.search_book_by_bst(book_id)
        if book:
            self.display_book(book)
        else:
            self.console.print("\n[bold red]❌ Không tìm thấy sách.[/bold red]")
        self.pause()

    def _display_traversal(self, title, books):
        self.console.print(f"\n[bold cyan]===== 📋 BST {title} =====[/bold cyan]")
        if not books:
            self.console.print("\n[bold yellow]📭 Thư viện chưa có sách.[/bold yellow]")
            self.pause()
            return

        table = Table(title=f"📋 BST {title}", header_style="bold magenta", border_style="blue")
        table.add_column("MÃ SÁCH", justify="center", style="cyan")
        table.add_column("TÊN SÁCH", style="green")
        table.add_column("TÁC GIẢ", style="yellow")
        table.add_column("NĂM", justify="center")
        table.add_column("SL", justify="center")
        for book in books:
            table.add_row(
                str(book.book_id),
                str(book.title),
                str(book.author),
                str(book.publish_year),
                str(book.quantity),
            )
        self.console.print(table)
        self.pause()

    def display_inorder(self):
        self._display_traversal("INORDER", self.service.get_bst_inorder())

    def display_preorder(self):
        self._display_traversal("PREORDER", self.service.get_bst_preorder())

    def display_postorder(self):
        self._display_traversal("POSTORDER", self.service.get_bst_postorder())

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.search_book,
                "2": self.display_inorder,
                "3": self.display_preorder,
                "4": self.display_postorder,
            },
        )
