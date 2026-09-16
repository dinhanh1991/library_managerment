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
    def __init__(self, service):
        super().__init__(service)

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
        if not self.confirm_action("Bạn có chắc chắn muốn thêm sách này không?"):
            return
        added = self.service.add_book(book)
        if added:
            print_info_success("Thêm sách thành công!")
            LOGGER.info("Book added: %s", book.book_id)
        else:
            print_info_error("Mã sách đã tồn tại hoặc dữ liệu sách không hợp lệ.")
        self.pause()

    def delete_book(self):
        self.console.print("\n[bold cyan]===== 🗑️ XÓA SÁCH =====[/bold cyan]")
        book_id = input("Nhập mã sách cần xóa: ").strip()
        if not book_id:
            print_info_warning("Mã sách không được để trống.")
            self.pause()
            return
        if not self.confirm_action("Bạn có chắc chắn muốn xóa sách này không?"):
            return
        result = self.service.remove_book(book_id)
        if result:
            self.console.print("\n[bold green]✅ Xóa sách thành công![/bold green]")
        else:
            books = self.service.get_all_books()
            is_existing = any(item.book_id == book_id for item in books)
            if is_existing and self.service.is_book_borrowed(book_id):
                print_info_warning("Sách đang được mượn, không thể xóa.")
            else:
                print_info_error("Không tìm thấy sách!")
        self.pause()

    def update_book(self):
        self.console.print("\n[bold cyan]===== ✏️ CẬP NHẬT SÁCH =====[/bold cyan]")
        book_id = input("Nhập mã sách cần cập nhật: ").strip()
        if not book_id:
            print_info_warning("Mã sách không được để trống.")
            self.pause()
            return
        books = self.service.get_all_books()
        book = None
        for item in books:
            if item.book_id == book_id:
                book = item
                break
        if book is None:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return

        self.console.print("\n[bold yellow]Thông tin hiện tại:[/bold yellow]")
        print(f"Mã sách: {book.book_id}")
        print(f"Tên sách: {book.title}")
        print(f"Tác giả: {book.author}")
        print(f"Năm xuất bản: {book.publish_year}")
        print(f"Số lượng: {book.quantity}")
        self.console.print("\n[bold yellow]--- Nhập thông tin mới ---[/bold yellow]")

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
            if publish_year < 0:
                print_info_error("Năm xuất bản không được âm.")
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
            if quantity < 0:
                print_info_error("Số lượng không được âm.")
                self.pause()
                return
        else:
            quantity = book.quantity

        updated_book = Book(book_id, title, author, publish_year, quantity, category=category, isbn=isbn)
        if not self.confirm_action("Bạn có chắc chắn muốn cập nhật sách này không?"):
            return
        result = self.service.update_book(updated_book)
        if result:
            print_info_success("Cập nhật sách thành công!")
            LOGGER.info("Book updated: %s", book_id)
        else:
            print_info_error("Cập nhật sách thất bại!")
        self.pause()

    @staticmethod
    def get_book_status(book):
        if book.quantity > 0:
            return "Có sẵn"
        return "Hết"

    def display_books(self):
        books = self.service.get_all_books()
        self.console.print()
        table = create_book_table("📚 DANH SÁCH SÁCH")
        if not books:
            table.add_row("-", "Không có sách trong thư viện", "-", "-", "-", "-")
        else:
            for book in books:
                status = self.get_book_status(book)
                add_book_to_table(table, book, status=status)
        self.console.print(table)
        self.pause()

    def search_by_title(self):
        self.console.print("\n[bold cyan]===== 🔍 TÌM SÁCH THEO TÊN =====[/bold cyan]")
        keyword = input("Nhập tên sách cần tìm: ").strip()
        if not keyword:
            print_info_warning("Tên sách không được để trống.")
            self.pause()
            return
        results = self.service.search_books_by_title(keyword)
        if not results:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return
        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book, status=self.get_book_status(book))
        self.console.print(table)
        self.pause()

    def search_by_author(self):
        self.console.print("\n[bold cyan]===== ✍️ TÌM SÁCH THEO TÁC GIẢ =====[/bold cyan]")
        author = input("Nhập tên tác giả cần tìm: ").strip()
        if not author:
            print_info_warning("Tên tác giả không được để trống.")
            self.pause()
            return
        results = self.service.search_books_by_author(author)
        if not results:
            print_info_error("Không tìm thấy sách!")
            self.pause()
            return
        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book, status=self.get_book_status(book))
        self.console.print(table)
        self.pause()

    def search_advanced(self):
        self.console.print("\n[bold cyan]===== 🔎 TÌM KIẾM NÂNG CAO =====[/bold cyan]")
        title = input("👉 Tên sách (để trống nếu không muốn lọc): ").strip() or None
        author = input("👉 Tác giả (để trống nếu không muốn lọc): ").strip() or None
        genre = input("👉 Thể loại (để trống nếu không muốn lọc): ").strip() or None
        publish_year = input("👉 Năm xuất bản (để trống nếu không muốn lọc): ").strip() or None
        isbn = input("👉 ISBN (để trống nếu không có): ").strip() or None
        availability = input("👉 Tình trạng [all/available/unavailable] (mặc định all): ").strip().lower() or "all"
        if availability not in {"all", "available", "unavailable"}:
            print_info_warning("Tình trạng không hợp lệ. Hiển thị tất cả kết quả.")
            availability = "all"
        results = self.service.search_books_advanced(title=title, author=author, genre=genre, publish_year=publish_year, isbn=isbn, availability=availability)
        if not results:
            print_info_error("Không tìm thấy sách phù hợp!")
            self.pause()
            return
        self.console.print(f"\n[bold green]🔎 Tìm thấy {len(results)} sách:[/bold green]")
        table = create_book_table("🔎 KẾT QUẢ TÌM KIẾM")
        for book in results:
            add_book_to_table(table, book, status=self.get_book_status(book))
        self.console.print(table)
        self.pause()

    def run(self):
        self.run_menu(self.show_menu, {"1": self.add_book, "2": self.delete_book, "3": self.update_book, "4": self.display_books, "5": self.search_by_title, "6": self.search_by_author, "7": self.search_advanced})
