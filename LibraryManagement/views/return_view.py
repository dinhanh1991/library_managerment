from rich.table import Table

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.utils.ui_helpers import prompt_field
from LibraryManagement.views.base_view import BaseView


class ReturnView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] ↩️ Trả sách\n"
            " [2] 📚 Xem lịch sử trả sách\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("↩️ QUẢN LÝ TRẢ SÁCH", menu_content)

    def return_book(self):
        self.console.print("\n[bold cyan]===== ↩️ TRẢ SÁCH =====[/bold cyan]")
        borrower_id = prompt_field("Nhập mã độc giả: ", "Mã độc giả")
        book_id = prompt_field("Nhập mã sách trả: ", "Mã sách")
        if borrower_id is None or book_id is None:
            self.pause()
            return

        if not self.confirm_action("Bạn có chắc chắn muốn trả sách này không?"):
            return

        result = self.service.return_book(Borrower(borrower_id, "", book_id))
        if result:
            self.console.print("\n[bold green]✅ Trả sách thành công![/bold green]")
        else:
            self.console.print("\n[bold red]❌ Không thể trả sách![/bold red]")
        self.pause()

    def display_return_stack(self):
        stack = self.service.get_return_stack_items()
        if not stack:
            self.console.print("\n[bold yellow]📭 Chưa có lịch sử trả sách.[/bold yellow]")
            self.pause()
            return

        table = Table(
            title="📚 LỊCH SỬ TRẢ SÁCH",
            header_style="bold magenta",
            border_style="blue",
        )
        for column in ("STT", "MÃ ĐỘC GIẢ", "TÊN ĐỘC GIẢ", "MÃ SÁCH", "NGÀY MƯỢN", "HẠN TRẢ", "NGÀY TRẢ", "TRẠNG THÁI"):
            table.add_column(column, justify="center" if column != "TÊN ĐỘC GIẢ" else "left")

        for index, borrower in enumerate(reversed(stack), start=1):
            table.add_row(
                str(index),
                str(borrower.borrower_id),
                str(borrower.name),
                str(borrower.book_id),
                str(borrower.borrow_date or "-"),
                str(borrower.due_date or "-"),
                str(borrower.return_date or "-"),
                str(borrower.status),
            )
        self.console.print(table)
        self.pause()

    def run(self):
        self.run_menu(
            self.show_menu,
            {"1": self.return_book, "2": self.display_return_stack},
        )
