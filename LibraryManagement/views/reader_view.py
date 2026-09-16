from rich import box
from rich.table import Table

from LibraryManagement.models.reader import Reader
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
        reader_id = input("Nhập mã độc giả: ").strip()
        name = input("Nhập tên độc giả: ").strip()

        if not reader_id or not name:
            self.console.print("\n[bold yellow]⚠️ Mã và tên độc giả không được để trống.[/bold yellow]")
            self.pause()
            return

        if self.service.add_reader(Reader(reader_id, name)):
            self.console.print("\n[bold green]✅ Thêm độc giả thành công![/bold green]")
        else:
            self.console.print("\n[bold red]❌ Mã độc giả đã tồn tại.[/bold red]")
        self.pause()

    def update_reader(self):
        self.show_section("===== ✏️ SỬA ĐỘC GIẢ =====")
        reader_id = input("Nhập mã độc giả cần sửa: ").strip()
        name = input("Nhập tên mới: ").strip()

        if not reader_id or not name:
            self.console.print("\n[bold yellow]⚠️ Mã và tên độc giả không được để trống.[/bold yellow]")
            self.pause()
            return

        if self.service.update_reader(Reader(reader_id, name)):
            self.console.print("\n[bold green]✅ Cập nhật độc giả thành công![/bold green]")
        else:
            self.console.print("\n[bold red]❌ Không tìm thấy độc giả.[/bold red]")
        self.pause()

    def delete_reader(self):
        self.show_section("===== 🗑️ XÓA ĐỘC GIẢ =====")
        reader_id = input("Nhập mã độc giả cần xóa: ").strip()

        if not reader_id:
            self.console.print("\n[bold yellow]⚠️ Mã độc giả không được để trống.[/bold yellow]")
            self.pause()
            return

        if not self.confirm_action("Bạn có chắc chắn muốn xóa độc giả này không?"):
            return

        if self.service.remove_reader(reader_id):
            self.console.print("\n[bold green]✅ Xóa độc giả thành công![/bold green]")
        else:
            self.console.print(
                "\n[bold red]❌ Không thể xóa: độc giả không tồn tại hoặc đang mượn sách.[/bold red]"
            )
        self.pause()

    def display_readers(self):
        readers = self.service.get_all_readers()
        if not readers:
            self.console.print("\n[bold yellow]📭 Chưa có độc giả.[/bold yellow]")
            self.pause()
            return

        table = Table(
            title="👥 DANH SÁCH ĐỘC GIẢ",
            header_style="bold white",
            border_style="yellow",
            box=box.SQUARE_DOUBLE_HEAD,
            show_lines=True,
            title_justify="left",
        )
        table.add_column("STT", justify="center", style="bold cyan")
        table.add_column("MÃ ĐỘC GIẢ", justify="center", style="bold yellow")
        table.add_column("TÊN ĐỘC GIẢ", style="bold white")
        table.add_column("ĐANG MƯỢN", justify="center", style="bold green")

        active_ids = {
            borrower.borrower_id
            for borrower in self.service.borrower_repo.load_borrowers()
        }
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
        reader_id = input("Nhập mã độc giả cần xem lịch sử: ").strip()
        if not reader_id:
            self.console.print("\n[bold yellow]⚠️ Mã độc giả không được để trống.[/bold yellow]")
            self.pause()
            return

        history = self.service.get_reader_history(reader_id)
        if not history:
            self.console.print("\n[bold yellow]📭 Chưa có lịch sử giao dịch.[/bold yellow]")
            self.pause()
            return

        table = Table(
            title=f"📚 LỊCH SỬ - {reader_id}",
            header_style="bold white",
            border_style="cyan",
            box=box.SIMPLE_HEAVY,
            show_lines=True,
            title_justify="left",
        )
        table.add_column("MÃ SÁCH", justify="center", style="bold green")
        table.add_column("NGÀY MƯỢN", justify="center", style="bold blue")
        table.add_column("HẠN TRẢ", justify="center", style="bold magenta")
        table.add_column("NGÀY TRẢ", justify="center", style="bold yellow")
        table.add_column("TRẠNG THÁI", justify="center", style="bold cyan")

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

        table = Table(
            title="⚠️ ĐỘC GIẢ QUÁ HẠN",
            header_style="bold white",
            border_style="red",
            box=box.SQUARE_DOUBLE_HEAD,
            show_lines=True,
            title_justify="left",
        )
        table.add_column("MÃ ĐỘC GIẢ", justify="center", style="bold cyan")
        table.add_column("TÊN ĐỘC GIẢ", style="bold white")
        table.add_column("MÃ SÁCH", justify="center", style="bold yellow")
        table.add_column("HẠN TRẢ", justify="center", style="bold red")
        table.add_column("TRẠNG THÁI", justify="center", style="bold magenta")

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
