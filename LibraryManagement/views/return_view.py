from rich.table import Table

from LibraryManagement.views.base_view import BaseView
from LibraryManagement.models.borrower import Borrower


class ReturnView(BaseView):

    def __init__(self, service):
        super().__init__(service)

    @staticmethod
    def _prompt_return_fields():
        borrower_id = input("Nhập mã độc giả: ").strip()
        name = input("Nhập tên độc giả: ").strip()
        book_id = input("Nhập mã sách trả: ").strip()
        return borrower_id, name, book_id

    def _validate_return_input(self, borrower_id, name, book_id):
        if not borrower_id or not name or not book_id:
            self.console.print(
                "\n[bold yellow]⚠️ Mã độc giả, tên độc giả và mã sách không được để trống.[/bold yellow]"
            )
            self.pause()
            return False
        return True

    # ============================================================
    # HIỂN THỊ MENU QUẢN LÝ TRẢ SÁCH
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] ↩️ Trả sách\n"
            " [2] 📚 Xem lịch sử trả sách\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("↩️ QUẢN LÝ TRẢ SÁCH", menu_content)

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # CHỨC NĂNG TRẢ SÁCH
    # ============================================================

    def return_book(self):
        self.console.print("\n[bold cyan]===== ↩️ TRẢ SÁCH =====[/bold cyan]")
        borrower_id, name, book_id = self._prompt_return_fields()

        if not self._validate_return_input(borrower_id, name, book_id):
            return

        borrower = Borrower(borrower_id, name, book_id)

        # ========================================================
        # XÁC NHẬN TRƯỚC KHI TRẢ
        # ========================================================

        if not self.confirm_action(
            "Bạn có chắc chắn muốn trả sách này không?"
        ):
            return

        # Gọi Service xử lý trả sách
        result = self.service.return_book(borrower)

        # Kiểm tra kết quả
        if result:

            self.console.print(
                "\n[bold green]✅ Trả sách thành công![/bold green]"
            )

        else:

            self.console.print(
                "\n[bold red]❌ Không thể trả sách![/bold red]"
            )

        self.pause()

    # ============================================================
    # HIỂN THỊ LỊCH SỬ TRẢ SÁCH
    # ============================================================

    def display_return_stack(self):

        # Kiểm tra Stack có rỗng hay không
        if self.service.return_stack.is_empty():

            self.console.print(
                "\n[bold yellow]"
                "📭 Chưa có lịch sử trả sách."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Lấy dữ liệu từ Stack
        stack = self.service.return_stack.items

        # Tạo bảng Rich
        table = Table(
            title="📚 LỊCH SỬ TRẢ SÁCH",
            header_style="bold magenta",
            border_style="blue"
        )

        # Tạo các cột
        table.add_column(
            "STT",
            justify="center",
            style="cyan",
            no_wrap=True
        )

        table.add_column(
            "MÃ ĐỘC GIẢ",
            justify="center"
        )

        table.add_column(
            "TÊN ĐỘC GIẢ",
            style="green"
        )

        table.add_column(
            "MÃ SÁCH",
            justify="center",
            style="yellow"
        )

        table.add_column("NGÀY MƯỢN", justify="center")
        table.add_column("HẠN TRẢ", justify="center")
        table.add_column("NGÀY TRẢ", justify="center")
        table.add_column("TRẠNG THÁI", justify="center")

        # Stack hoạt động theo nguyên tắc LIFO
        # nên hiển thị phần tử cuối cùng trước
        for i, borrower in enumerate(
            reversed(stack),
            start=1
        ):

            table.add_row(
                str(i),
                str(borrower.borrower_id),
                str(borrower.name),
                str(borrower.book_id),
                str(borrower.borrow_date or "-"),
                str(borrower.due_date or "-"),
                str(borrower.return_date or "-"),
                str(borrower.status),
            )

        # Hiển thị bảng
        self.console.print()
        self.console.print(table)

        self.pause()

    # ============================================================
    # CHẠY CHƯƠNG TRÌNH
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.return_book,
                "2": self.display_return_stack,
            },
        )

