
from rich.table import Table

from LibraryManagement.views.base_view import BaseView
from LibraryManagement.models.book import Book
from LibraryManagement.utils.logging_config import LOGGER
from LibraryManagement.utils.ui_helpers import (
    add_book_to_table,
    create_book_table,
    print_info_error,
    print_info_success,
    print_info_warning,
    prompt_field,
    prompt_int,
)


class BookView(BaseView):

    # ============================================================
    # KHỞI TẠO BOOK VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU QUẢN LÝ SÁCH
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] ➕ Thêm sách\n"
            " [2] 🗑️  Xóa sách\n"
            " [3] ✏️  Cập nhật sách\n"
            " [4] 📋 Hiển thị tất cả\n"
            " [5] 🔍 Tìm theo tên\n"
            " [6] ✍️  Tìm theo tác giả\n"
            " [7] 🔎 Tìm kiếm nâng cao\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("📖 QUẢN LÝ SÁCH", menu_content, accent="green")

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # CHỨC NĂNG THÊM SÁCH
    # ============================================================

    def add_book(self):
        self.console.print("\n[bold cyan]===== ➕ THÊM SÁCH =====[/bold cyan]")

        book_id = prompt_field("Nhập mã sách: ", "Mã sách")
        title = prompt_field("Nhập tên sách: ", "Tên sách")
        author = prompt_field("Nhập tác giả: ", "Tác giả")

        if book_id is None or title is None or author is None:
            self.pause()
            return

        publish_year = prompt_int("Nhập năm xuất bản: ", "Năm xuất bản", min_value=0)
        quantity = prompt_int("Nhập số lượng: ", "Số lượng", min_value=0)
        category = prompt_field("Nhập thể loại (nhấn Enter để đặt mặc định): ", "Thể loại", allow_empty=True) or "Chưa phân loại"
        isbn = prompt_field("Nhập ISBN (nhấn Enter nếu không có): ", "ISBN", allow_empty=True) or ""

        if publish_year is None or quantity is None:
            self.pause()
            return

        book = Book(book_id, title, author, publish_year, quantity, category=category, isbn=isbn)

        # ========================================================
        # XÁC NHẬN TRƯỚC KHI THÊM
        # ========================================================

        # Gọi hàm confirm_action()
        # Nếu người dùng chọn N thì return False
        # và kết thúc chức năng thêm sách
        if not self.confirm_action(
            "Bạn có chắc chắn muốn thêm sách này không?"
        ):
            return

        added = self.service.add_book(book)
        if added:
            print_info_success("Thêm sách thành công!")
            LOGGER.info("Book added: %s", book.book_id)
        else:
            print_info_error("Mã sách đã tồn tại trong hệ thống.")
        self.pause()

    # ============================================================
    # CHỨC NĂNG XÓA SÁCH
    # ============================================================

    def delete_book(self):

        self.console.print(
            "\n[bold cyan]===== 🗑️ XÓA SÁCH =====[/bold cyan]"
        )

        # Nhập mã sách cần xóa
        book_id = input(
            "Nhập mã sách cần xóa: "
        ).strip()

        # Kiểm tra mã sách có bị bỏ trống không
        if not book_id:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Mã sách không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # ========================================================
        # XÁC NHẬN TRƯỚC KHI XÓA
        # ========================================================

        # Hỏi người dùng có chắc chắn muốn xóa hay không
        if not self.confirm_action(
            "Bạn có chắc chắn muốn xóa sách này không?"
        ):
            return

        # Gọi Service thực hiện xóa sách
        result = self.service.remove_book(book_id)

        # Kiểm tra kết quả xóa
        if result:

            self.console.print(
                "\n[bold green]✅ Xóa sách thành công![/bold green]"
            )

        else:

            self.console.print(
                "\n[bold red]❌ Không tìm thấy sách![/bold red]"
            )

        self.pause()

    # ============================================================
    # CHỨC NĂNG CẬP NHẬT SÁCH
    # ============================================================

    def update_book(self):

        self.console.print(
            "\n[bold cyan]===== ✏️ CẬP NHẬT SÁCH =====[/bold cyan]"
        )

        # Nhập mã sách cần cập nhật
        book_id = input(
            "Nhập mã sách cần cập nhật: "
        ).strip()

        # Kiểm tra mã sách có bị bỏ trống không
        if not book_id:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Mã sách không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Lấy toàn bộ danh sách sách từ Service
        books = self.service.get_all_books()

        # Ban đầu chưa tìm thấy sách
        book = None

        # Duyệt qua danh sách để tìm sách theo mã
        for item in books:

            if item.book_id == book_id:
                book = item
                break

        if book is None:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return

        # ========================================================
        # HIỂN THỊ THÔNG TIN HIỆN TẠI
        # ========================================================

        self.console.print(
            "\n[bold yellow]Thông tin hiện tại:[/bold yellow]"
        )

        print(f"Mã sách: {book.book_id}")
        print(f"Tên sách: {book.title}")
        print(f"Tác giả: {book.author}")
        print(f"Năm xuất bản: {book.publish_year}")
        print(f"Số lượng: {book.quantity}")

        # ========================================================
        # NHẬP THÔNG TIN MỚI
        # ========================================================

        self.console.print(
            "\n[bold yellow]--- Nhập thông tin mới ---[/bold yellow]"
        )

        title = input("Tên sách mới (Enter để giữ): ").strip() or book.title
        author = input("Tác giả mới (Enter để giữ): ").strip() or book.author
        category = input("Thể loại mới (Enter để giữ): ").strip() or book.category
        isbn = input("ISBN mới (Enter để giữ): ").strip() or book.isbn

        raw_publish_year = input("Năm xuất bản mới (Enter để giữ): ").strip()
        if raw_publish_year:
            try:
                publish_year = int(raw_publish_year)
            except ValueError:
                print_info_error("Năm xuất bản không hợp lệ.")
                self.pause()
                return
        else:
            publish_year = book.publish_year

        raw_quantity = input("Số lượng mới (Enter để giữ): ").strip()
        if raw_quantity:
            try:
                quantity = int(raw_quantity)
            except ValueError:
                print_info_error("Số lượng không hợp lệ.")
                self.pause()
                return
        else:
            quantity = book.quantity

        # Tạo đối tượng Book chứa thông tin mới
        updated_book = Book(
            book_id,
            title,
            author,
            publish_year,
            quantity,
            category=category,
            isbn=isbn,
        )

        # ========================================================
        # XÁC NHẬN TRƯỚC KHI CẬP NHẬT
        # ========================================================

        # Nếu người dùng chọn N thì không cập nhật
        if not self.confirm_action(
            "Bạn có chắc chắn muốn cập nhật sách này không?"
        ):
            return

        # Nếu người dùng chọn Y
        # thì thực hiện cập nhật
        result = self.service.update_book(updated_book)

        if result:
            print_info_success("Cập nhật sách thành công!")
            LOGGER.info("Book updated: %s", book_id)
        else:
            print_info_error("Cập nhật sách thất bại!")
        self.pause()

    # ============================================================
    # HIỂN THỊ TẤT CẢ SÁCH
    # ============================================================

    def display_books(self):

        # Lấy toàn bộ sách từ Service
        books = self.service.get_all_books()

        self.console.print()

        table = create_book_table("📚 DANH SÁCH SÁCH")

        if not books:
            table.add_row("-", "Không có sách trong thư viện", "-", "-", "-")
        else:
            for book in books:
                add_book_to_table(table, book)

        # Hiển thị bảng
        self.console.print(table)

        self.pause()

    # ============================================================
    # TÌM SÁCH THEO TÊN
    # ============================================================

    def search_by_title(self):

        self.console.print(
            "\n[bold cyan]===== 🔍 TÌM SÁCH THEO TÊN =====[/bold cyan]"
        )

        # Nhập từ khóa tìm kiếm
        keyword = input(
            "Nhập tên sách cần tìm: "
        ).strip()

        if not keyword:
            print_info_warning("Tên sách không được để trống.")
            self.pause()
            return

        # Gọi Service tìm sách theo tên
        results = self.service.search_books_by_title(keyword)

        if not results:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return

        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book)
        self.console.print(table)

        self.pause()

    # ============================================================
    # TÌM SÁCH THEO TÁC GIẢ
    # ============================================================

    def search_by_author(self):

        self.console.print(
            "\n[bold cyan]===== ✍️ TÌM SÁCH THEO TÁC GIẢ =====[/bold cyan]"
        )

        # Nhập tên tác giả cần tìm
        author = input(
            "Nhập tên tác giả cần tìm: "
        ).strip()

        if not author:
            print_info_warning("Tên tác giả không được để trống.")
            self.pause()
            return

        # Gọi Service tìm sách theo tác giả
        results = self.service.search_books_by_author(author)

        if not results:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return

        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book)
        self.console.print(table)

        self.pause()

    # ============================================================
    # TÌM KIẾM NÂNG CAO
    # ============================================================

    def search_advanced(self):
        self.console.print("\n[bold cyan]===== 🔎 TÌM KIẾM NÂNG CAO =====[/bold cyan]")

        title = input("👉 Tên sách (để trống nếu không muốn lọc): ").strip() or None
        author = input("👉 Tác giả (để trống nếu không muốn lọc): ").strip() or None
        genre = input("👉 Thể loại (để trống nếu không muốn lọc): ").strip() or None
        publish_year = input("👉 Năm xuất bản (để trống nếu không muốn lọc): ").strip() or None
        isbn = input("👉 ISBN (để trống nếu không muốn lọc): ").strip() or None
        availability = input("👉 Tình trạng [all/available/unavailable] (mặc định all): ").strip().lower() or "all"

        if availability not in {"all", "available", "unavailable"}:
            print_info_warning("Tình trạng không hợp lệ. Hiển thị tất cả kết quả.")
            availability = "all"

        results = self.service.search_books_advanced(
            title=title,
            author=author,
            genre=genre,
            publish_year=publish_year,
            isbn=isbn,
            availability=availability,
        )

        if not results:
            print_info_error("Không tìm thấy sách phù hợp!")
            self.pause()
            return

        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book)
        self.console.print(table)
        self.pause()

    # ============================================================
    # CHẠY CHƯƠNG TRÌNH
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.add_book,
                "2": self.delete_book,
                "3": self.update_book,
                "4": self.display_books,
                "5": self.search_by_title,
                "6": self.search_by_author,
                "7": self.search_advanced,
            },
        )
