from rich.table import Table

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.utils.ui_helpers import prompt_field
from LibraryManagement.views.base_view import BaseView


class BorrowView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] 📚 Mượn sách\n"
            " [2] 👥 Xem hàng đợi mượn\n"
            " [3] ▶️  Xử lý người mượn tiếp theo\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("👤 QUẢN LÝ MƯỢN SÁCH", menu_content)

    def borrow_book(self):
        self.console.print("\n[bold cyan]===== 📚 MƯỢN SÁCH =====[/bold cyan]")
        borrower_id = prompt_field("Nhập mã độc giả: ", "Mã độc giả")
        name = prompt_field("Nhập tên độc giả: ", "Tên độc giả")
        book_id = prompt_field("Nhập mã sách muốn mượn: ", "Mã sách")
        if borrower_id is None or name is None or book_id is None:
            self.pause()
            return

        if not self.confirm_action("Bạn có chắc chắn muốn mượn sách này không?"):
            return

        result = self.service.book_borrow(Borrower(borrower_id, name, book_id))
        if result:
            self.console.print("\n[bold green]✅ Mượn sách thành công![/bold green]")
        else:
            self.console.print("\n[bold red]❌ Không thể mượn sách![/bold red]")
        self.pause()

    def display_queue(self):
        queue_items = self.service.get_borrow_queue_items()
        if not queue_items:
            self.console.print("\n[bold yellow]📭 Hàng đợi mượn sách đang trống.[/bold yellow]")
            self.pause()
            return

        table = Table(
            title="👥 HÀNG ĐỢI MƯỢN SÁCH",
            header_style="bold magenta",
            border_style="blue",
        )
        for column in ("STT", "MÃ ĐỘC GIẢ", "TÊN ĐỘC GIẢ", "MÃ SÁCH", "NGÀY MƯỢN", "HẠN TRẢ", "TRẠNG THÁI"):
            table.add_column(column, justify="center" if column != "TÊN ĐỘC GIẢ" else "left")

        for index, borrower in enumerate(queue_items, start=1):
            table.add_row(
                str(index),
                str(borrower.borrower_id),
                str(borrower.name),
                str(borrower.book_id),
                str(borrower.borrow_date or "-"),
                str(borrower.due_date or "-"),
                str(borrower.status),
            )
        self.console.print(table)
        self.pause()

    def process_next_borrower(self):
        self.console.print("\n[bold cyan]===== ▶️ XỬ LÝ NGƯỜI MƯỢN =====[/bold cyan]")
        borrower = self.service.get_next_borrower()
        if borrower is None:
            self.console.print("\n[bold yellow]📭 Không có người mượn trong hàng đợi.[/bold yellow]")
            self.pause()
            return

        self.console.print(
            f"\n[bold yellow]Người mượn tiếp theo:[/bold yellow] "
            f"{borrower.borrower_id} | {borrower.name} | Sách: {borrower.book_id}"
        )

        if not self.confirm_action("Bạn có chắc chắn muốn xử lý người mượn này không?"):
            return

        processed = self.service.process_next_borrower()
        if processed is not None:
            self.console.print(
                f"\n[bold green]✅ Đã xử lý: {processed.borrower_id} | "
                f"{processed.name} | Sách: {processed.book_id}[/bold green]"
            )
        else:
            self.console.print("\n[bold red]❌ Không thể xử lý người mượn.[/bold red]")
        self.pause()

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.borrow_book,
                "2": self.display_queue,
                "3": self.process_next_borrower,
            },
        )
