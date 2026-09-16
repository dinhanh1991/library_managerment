from rich.table import Table

from LibraryManagement.views.base_view import BaseView

class LinkedListView(BaseView):

    # ============================================================
    # KHỞI TẠO LINKED LIST VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU QUẢN LÝ LINKED LIST
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] 📋 Hiển thị danh sách sách\n"
            " [2] 🔍 Tìm sách theo mã bằng Linked List\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🔗 QUẢN LÝ LINKED LIST", menu_content)

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # TẠO BẢNG HIỂN THỊ THÔNG TIN SÁCH
    # ============================================================

    def create_book_table(self, title="📚 DANH SÁCH SÁCH"):
        """
        Tạo bảng Rich dùng chung cho:
        - Hiển thị toàn bộ sách
        - Hiển thị kết quả tìm kiếm

        Việc dùng chung một hàm giúp giao diện
        ở hai chức năng giống nhau.
        """

        table = Table(
            title=title,
            header_style="bold magenta",
            border_style="blue"
        )

        # Cột mã sách
        table.add_column(
            "MÃ SÁCH",
            justify="center",
            style="cyan",
            no_wrap=True
        )

        # Cột tên sách
        table.add_column(
            "TÊN SÁCH",
            style="green"
        )

        # Cột tác giả
        table.add_column(
            "TÁC GIẢ",
            style="yellow"
        )

        # Cột năm xuất bản
        table.add_column(
            "NĂM",
            justify="center"
        )

        # Cột số lượng
        table.add_column(
            "SL",
            justify="center"
        )

        return table

    # ============================================================
    # THÊM MỘT CUỐN SÁCH VÀO BẢNG
    # ============================================================

    def add_book_to_table(self, table, book):
        """
        Thêm thông tin một Book vào bảng Rich.
        """

        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity)
        )

    # ============================================================
    # HIỂN THỊ DANH SÁCH SÁCH BẰNG LINKED LIST
    # ============================================================

    def display_books(self):
        self.console.print(
            "\n[bold cyan]===== 📋 DANH SÁCH SÁCH - LINKED LIST =====[/bold cyan]"
        )

        # Xây dựng Linked List từ dữ liệu sách
        linked_list = self.service.build_book_linked_list()

        # Kiểm tra Linked List có rỗng hay không
        if linked_list.head is None:
            self.console.print(
                "\n[bold yellow]📭 Thư viện chưa có sách.[/bold yellow]"
            )
            self.pause()
            return

        # Tạo bảng
        table = self.create_book_table(
            "📋 DANH SÁCH SÁCH - LINKED LIST"
        )

        # Bắt đầu từ node đầu tiên
        current = linked_list.head

        # Duyệt từng node trong Linked List
        while current is not None:

            # Lấy Book được lưu trong node
            book = current.data

            # Thêm sách vào bảng
            self.add_book_to_table(table, book)

            # Chuyển sang node tiếp theo
            current = current.next

        # Hiển thị bảng
        self.console.print()
        self.console.print(table)

        self.pause()

    # ============================================================
    # TÌM SÁCH THEO MÃ BẰNG LINKED LIST
    # ============================================================

    def search_book(self):
        self.console.print(
            "\n[bold cyan]===== 🔍 TÌM SÁCH BẰNG LINKED LIST =====[/bold cyan]"
        )

        # Nhập mã sách cần tìm
        book_id = input("👉 Nhập mã sách cần tìm: ").strip()

        # Kiểm tra dữ liệu nhập vào
        if not book_id:
            self.console.print(
                "\n[bold yellow]⚠️ Mã sách không được để trống.[/bold yellow]"
            )
            self.pause()
            return

        # Gọi Service để tìm sách bằng Linked List
        book = self.service.search_book_by_linked_list(book_id)

        # Nếu tìm thấy sách
        if book:

            # Tạo bảng giống hệt bảng hiển thị danh sách
            table = self.create_book_table(
                "🔍 KẾT QUẢ TÌM KIẾM - LINKED LIST"
            )

            # Thêm sách tìm được vào bảng
            self.add_book_to_table(table, book)

            # Hiển thị bảng
            self.console.print()
            self.console.print(table)

        # Nếu không tìm thấy
        else:
            self.console.print(
                "\n[bold red]❌ Không tìm thấy sách.[/bold red]"
            )

        self.pause()

    # ============================================================
    # CHẠY MENU LINKED LIST
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.display_books,
                "2": self.search_book,
            },
        )