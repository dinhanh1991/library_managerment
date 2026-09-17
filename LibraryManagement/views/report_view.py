from rich import box
from rich.table import Table

from LibraryManagement.services.report_service import ReportService
from LibraryManagement.views.base_view import BaseView


class ReportView(BaseView):
    """Render library reports returned by ReportService."""

    def __init__(self, service):
        super().__init__(service)
        self.report_service = ReportService(service)

    def show_menu(self):
        menu_content = (
            " [1] 📊 Thống kê tổng quan\n"
            " [2] 📚 Thống kê sách\n"
            " [3] 🔄 Thống kê mượn / trả\n"
            " [4] 🏷️  Thống kê theo thể loại\n"
            " [5] ⚠️  Danh sách quá hạn\n"
            " [6] 🏆 Top sách được mượn\n"
            " [7] 👥 Top độc giả mượn sách\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("📊 BÁO CÁO & THỐNG KÊ", menu_content, accent="bright_magenta")

    def show_overview(self):
        data = self.report_service.get_overview()
        table = Table(title="📊 THỐNG KÊ TỔNG QUAN", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("CHỈ TIÊU", style="bold white")
        table.add_column("GIÁ TRỊ", justify="center", style="bold cyan")

        rows = [
            ("Tổng số đầu sách", data["total_books"]),
            ("Số đầu sách còn hàng", data["available_books"]),
            ("Đang mượn", data["borrowed"]),
            ("Đang chờ", data["pending"]),
            ("Quá hạn", data["overdue"]),
            ("Tổng độc giả", data["total_readers"]),
        ]
        for label, value in rows:
            table.add_row(label, str(value))

        self.console.print(table)
        self.pause()

    def show_book_statistics(self):
        data = self.report_service.get_book_statistics()
        table = Table(title="📚 THỐNG KÊ SÁCH", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("CHỈ TIÊU", style="bold white")
        table.add_column("GIÁ TRỊ", justify="center", style="bold green")

        rows = [
            ("Tổng số đầu sách", data["total_titles"]),
            ("Tổng số lượng bản", data["total_quantity"]),
            ("Số bản đang có sẵn", data["available_quantity"]),
            ("Đầu sách hết hàng", data["out_of_stock"]),
        ]
        for label, value in rows:
            table.add_row(label, str(value))

        self.console.print(table)
        self.pause()

    def show_borrow_statistics(self):
        data = self.report_service.get_borrow_statistics()
        table = Table(title="🔄 THỐNG KÊ MƯỢN / TRẢ", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("TRẠNG THÁI", style="bold white")
        table.add_column("SỐ LƯỢNG", justify="center", style="bold cyan")

        for label, key in [
            ("Đang mượn", "borrowed"),
            ("Đang chờ", "pending"),
            ("Quá hạn", "overdue"),
            ("Đã trả", "returned"),
        ]:
            table.add_row(label, str(data[key]))

        self.console.print(table)
        self.pause()

    def show_category_statistics(self):
        data = self.report_service.get_category_statistics()
        table = Table(title="🏷️ THỐNG KÊ THEO THỂ LOẠI", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("THỂ LOẠI", style="bold white")
        table.add_column("ĐANG MƯỢN / CHỜ", justify="center", style="bold green")

        if data:
            for category, count in data.items():
                table.add_row(category, str(count))
        else:
            table.add_row("Chưa có dữ liệu", "0")

        self.console.print(table)
        self.pause()

    def show_overdue_borrowers(self):
        data = self.report_service.get_overdue_borrowers()
        table = Table(title="⚠️ DANH SÁCH QUÁ HẠN", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("MÃ ĐỘC GIẢ", style="bold cyan")
        table.add_column("TÊN", style="bold white")
        table.add_column("MÃ SÁCH", style="bold yellow")
        table.add_column("HẠN TRẢ", style="bold red")
        table.add_column("QUÁ HẠN", justify="center", style="bold magenta")

        if data:
            for item in data:
                table.add_row(
                    str(item["borrower_id"]),
                    str(item["name"]),
                    str(item["book_id"]),
                    str(item["due_date"]),
                    f'{item["overdue_days"]} ngày',
                )
        else:
            table.add_row("-", "Không có", "-", "-", "0 ngày")

        self.console.print(table)
        self.pause()

    def show_most_borrowed_books(self):
        data = self.report_service.get_most_borrowed_books()
        table = Table(title="🏆 TOP SÁCH ĐƯỢC MƯỢN", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("MÃ SÁCH", style="bold cyan")
        table.add_column("TÊN SÁCH", style="bold white")
        table.add_column("SỐ LẦN", justify="center", style="bold green")

        if data:
            for item in data[:10]:
                table.add_row(
                    str(item["book_id"]),
                    str(item["title"]),
                    str(item["borrow_count"]),
                )
        else:
            table.add_row("-", "Chưa có dữ liệu", "0")

        self.console.print(table)
        self.pause()

    def show_most_active_readers(self):
        data = self.report_service.get_most_active_readers()
        table = Table(title="👥 TOP ĐỘC GIẢ MƯỢN SÁCH", box=box.SIMPLE_HEAVY, show_lines=True)
        table.add_column("MÃ ĐỘC GIẢ", style="bold cyan")
        table.add_column("TÊN", style="bold white")
        table.add_column("SỐ LẦN", justify="center", style="bold yellow")

        if data:
            for item in data[:10]:
                table.add_row(
                    str(item["borrower_id"]),
                    str(item["name"]),
                    str(item["borrow_count"]),
                )
        else:
            table.add_row("-", "Chưa có dữ liệu", "0")

        self.console.print(table)
        self.pause()

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.show_overview,
                "2": self.show_book_statistics,
                "3": self.show_borrow_statistics,
                "4": self.show_category_statistics,
                "5": self.show_overdue_borrowers,
                "6": self.show_most_borrowed_books,
                "7": self.show_most_active_readers,
            },
        )
