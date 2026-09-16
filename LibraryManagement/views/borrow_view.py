
from rich.table import Table

from LibraryManagement.views.base_view import BaseView
from LibraryManagement.models.borrower import Borrower


class BorrowView(BaseView):

    # ============================================================
    # KHỞI TẠO BORROW VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU QUẢN LÝ MƯỢN SÁCH
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] 📚 Mượn sách\n"
            " [2] 👥 Xem hàng đợi mượn\n"
            " [3] ▶️  Xử lý người mượn tiếp theo\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("👤 QUẢN LÝ MƯỢN SÁCH", menu_content)

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # CHỨC NĂNG MƯỢN SÁCH
    # ============================================================

    def borrow_book(self):

        self.console.print(
            "\n[bold cyan]===== 📚 MƯỢN SÁCH =====[/bold cyan]"
        )

        # Nhập thông tin người mượn
        borrower_id = input(
            "Nhập mã độc giả: "
        ).strip()

        name = input(
            "Nhập tên độc giả: "
        ).strip()

        book_id = input(
            "Nhập mã sách muốn mượn: "
        ).strip()

        # Kiểm tra dữ liệu nhập
        if not borrower_id or not name or not book_id:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Mã độc giả, tên độc giả và mã sách "
                "không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Tạo đối tượng Borrower
        borrower = Borrower(
            borrower_id,
            name,
            book_id
        )

        # ========================================================
        # XÁC NHẬN TRƯỚC KHI MƯỢN
        # ========================================================

        if not self.confirm_action(
            "Bạn có chắc chắn muốn mượn sách này không?"
        ):
            return

        # Gọi Service xử lý mượn sách
        result = self.service.book_borrow(borrower)

        # Kiểm tra kết quả
        if result:

            self.console.print(
                "\n[bold green]✅ Mượn sách thành công![/bold green]"
            )

        else:

            self.console.print(
                "\n[bold red]❌ Không thể mượn sách![/bold red]"
            )

        self.pause()

    # ============================================================
    # HIỂN THỊ HÀNG ĐỢI MƯỢN SÁCH
    # ============================================================

    def display_queue(self):

        # Kiểm tra hàng đợi có rỗng hay không
        if self.service.borrow_queue.is_empty():

            self.console.print(
                "\n[bold yellow]📭 Hàng đợi mượn sách đang trống.[/bold yellow]"
            )

            self.pause()
            return

        # Tạo bảng Rich
        table = Table(
            title="👥 HÀNG ĐỢI MƯỢN SÁCH",
            header_style="bold magenta",
            border_style="blue"
        )

        # Các cột
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
        table.add_column("TRẠNG THÁI", justify="center")

        # Duyệt hàng đợi
        for i, borrower in enumerate(
            self.service.borrow_queue.items,
            start=1
        ):

            table.add_row(
                str(i),
                str(borrower.borrower_id),
                str(borrower.name),
                str(borrower.book_id),
                str(borrower.borrow_date or "-"),
                str(borrower.due_date or "-"),
                str(borrower.status),
            )

        # Hiển thị bảng
        self.console.print()
        self.console.print(table)

        self.pause()

    # ============================================================
    # XỬ LÝ NGƯỜI MƯỢN TIẾP THEO
    # ============================================================

    def process_next_borrower(self):

        self.console.print(
            "\n[bold cyan]===== ▶️ XỬ LÝ NGƯỜI MƯỢN =====[/bold cyan]"
        )

        # Kiểm tra hàng đợi có người hay không
        if self.service.borrow_queue.is_empty():

            self.console.print(
                "\n[bold yellow]"
                "📭 Không có người mượn trong hàng đợi."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Lấy người mượn đầu tiên để hiển thị
        borrower = self.service.borrow_queue.items[0]

        # Hiển thị thông tin người tiếp theo
        self.console.print(
            "\n[bold yellow]Người mượn tiếp theo:[/bold yellow]"
        )

        table = Table(
            border_style="blue",
            show_header=True
        )

        table.add_column(
            "MÃ ĐỘC GIẢ",
            justify="center",
            style="cyan"
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
        table.add_column("TRẠNG THÁI", justify="center")

        table.add_row(
            str(borrower.borrower_id),
            str(borrower.name),
            str(borrower.book_id),
            str(borrower.borrow_date or "-"),
            str(borrower.due_date or "-"),
            str(borrower.status),
        )

        self.console.print(table)

        # ========================================================
        # XÁC NHẬN XỬ LÝ
        # ========================================================

        if not self.confirm_action(
            "Bạn có chắc chắn muốn xử lý người mượn này không?"
        ):
            return

        # Gọi Service xử lý người mượn tiếp theo
        borrower = self.service.process_next_borrower()

        # Kiểm tra kết quả
        if borrower is not None:

            self.console.print(
                "\n[bold green]"
                f"✅ Đã xử lý: "
                f"{borrower.borrower_id} | "
                f"{borrower.name} | "
                f"Sách: {borrower.book_id}"
                "[/bold green]"
            )

        else:

            self.console.print(
                "\n[bold red]"
                "❌ Không thể xử lý người mượn."
                "[/bold red]"
            )

        self.pause()

    # ============================================================
    # CHẠY CHƯƠNG TRÌNH
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.borrow_book,
                "2": self.display_queue,
                "3": self.process_next_borrower,
            },
        )
