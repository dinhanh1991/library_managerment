from rich import box
from rich.table import Table

from LibraryManagement.models.reader import Reader
from LibraryManagement.utils.ui_helpers import prompt_field
from LibraryManagement.views.base_view import BaseView


class ReaderView(BaseView):
    def show_menu(self):
        menu_content = (
            " [1] ➕ Thêm độc giả\n"
            " [2] ✏️  Sửa thông tin độc giả\n"
            " [3] 🗑️  Xóa độc giả\n"
            " [4] 📋 Danh sách độc giả\n"
            " [5] 📚 Lịch sử mượn của độc giả\n"
            " [6] ⚠️ Danh sách độc giả quá hạn\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("👥 QUẢN LÝ ĐỘC GIẢ", menu_content, accent="yellow")

    def add_reader(self):
        self.show_section("===== ➕ THÊM ĐỘC GIẢ =====")
        reader_id = prompt_field("Nhập mã độc giả: ", "Mã độc giả")
        name = prompt_field("Nhập tên độc giả: ", "Tên độc giả")
        if reader_id is None or name is None:
            self.pause()
            return
        result = self.service.add_reader(Reader(reader_id, name))
        self.console.print(
            "\n[bold green]✅ Thêm độc giả thành công![/bold green]"
            if result else
            "\n[bold red]❌ Mã độc giả đã tồn tại hoặc dữ liệu không hợp lệ.[/bold red]"
        )
        self.pause()

    def update_reader(self):
        self.show_section("===== ✏️ SỬA ĐỘC GIẢ =====")
        reader_id = prompt_field("Nhập mã độc giả cần sửa: ", "Mã độc giả")
        name = prompt_field("Nhập tên mới: ", "Tên độc giả")
        if reader_id is None or name is None:
            self.pause()
            return
        result = self.service.update_reader(Reader(reader_id, name))
        self.console.print(
            "\n[bold green]✅ Cập nhật độc giả thành công![/bold green]"
            if result else
            "\n[bold red]❌ Không tìm thấy độc giả hoặc dữ liệu không hợp lệ.[/bold red]"
        )
        self.pause()

    def delete_reader(self):
        self.show_section("===== 🗑️ XÓA ĐỘC GIẢ =====")
        reader_id = prompt_field("Nhập mã độc giả cần xóa: ", "Mã độc giả")
        if reader_id is None:
            self.pause()
            return
        if not self.confirm_action("Bạn có chắc chắn muốn xóa độc giả này không?"):
            return
        result = self.service.remove_reader(reader_id)
        self.console.print(
            "\n[bold green]✅ Xóa độc giả thành công![/bold green]"
            if result else
            "\n[bold red]❌ Không thể xóa: độc giả không tồn tại hoặc đang mượn sách.[/bold red]"
        )
        self.pause()

    def display_readers(self):
        readers = self.service.get_all_readers()
        if not readers:
            self.console.print("\n[bold yellow]📭 Chưa có độc giả.[/bold yellow]")
            self.pause()
            return

        active_ids = self.service.get_active_reader_ids()
        table = Table(
            title="👥 DANH SÁCH ĐỘC GIẢ",
            header_style="bold white",
            border_style="yellow",
            box=box.SQUARE_DOUBLE_HEAD,
            show_lines=True,
        )
        table.add_column("STT", justify="center", style="bold cyan")
        table.add_column("MÃ ĐỘC GIẢ", justify="center", style="bold yellow")
        table.add_column("TÊN ĐỘC GIẢ", style="bold white")
        table.add_column("ĐANG MƯỢN", justify="center", style="bold green")

        for index, reader in enumerate(readers, start=1):
            table.add_row(
                str(index),
                reader.reader_id,
                reader.name,
                "Có" if reader.reader_id in active_ids else "Không",
            )
        self.console.print(table)
        self.pause()

    def display_history(self):
        reader_id = prompt_field("Nhập mã độc giả cần xem lịch sử: ", "Mã độc giả")
        if reader_id is None:
            self.pause()
            return
        history = self.service.get_reader_history(reader_id)
        if not history:
            self.console.print("\n[bold yellow]📭 Chưa có lịch sử giao dịch.[/bold yellow]")
            self.pause()
            return

        table = Table(title=f"📚 LỊCH SỬ - {reader_id}", header_style="bold white", border_style="cyan", box=box.SIMPLE_HEAVY)
        for column in ("MÃ SÁCH", "NGÀY MƯỢN", "HẠN TRẢ", "NGÀY TRẢ", "TRẠNG THÁI"):
            table.add_column(column, justify="center")
        for borrower in history:
            table.add_row(
                borrower.book_id,
                borrower.borrow_date or "-",
                borrower.due_date or "-",
                borrower.return_date or "-",
                borrower.status,
            )
        self.console.print(table)
        self.pause()

    def display_overdue(self):
        overdue = self.service.get_overdue_borrowers()
        if not overdue:
            self.console.print("\n[bold green]✅ Không có độc giả quá hạn.[/bold green]")
            self.pause()
            return

        table = Table(title="⚠️ ĐỘC GIẢ QUÁ HẠN", header_style="bold white", border_style="red", box=box.SQUARE_DOUBLE_HEAD, show_lines=True)
        for column in ("MÃ ĐỘC GIẢ", "TÊN ĐỘC GIẢ", "MÃ SÁCH", "HẠN TRẢ", "TRẠNG THÁI"):
            table.add_column(column, justify="center")
        for borrower in overdue:
            table.add_row(
                borrower.borrower_id,
                borrower.name,
                borrower.book_id,
                borrower.due_date or "-",
                borrower.status,
            )
        self.console.print(table)
        self.pause()

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.add_reader,
                "2": self.update_reader,
                "3": self.delete_reader,
                "4": self.display_readers,
                "5": self.display_history,
                "6": self.display_overdue,
            },
        )
