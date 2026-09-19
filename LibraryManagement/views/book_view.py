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
    prompt_optional_int,
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
        publish_year = prompt_int("Nhập năm xuất bản: ", "Năm xuất bản")
        quantity = prompt_int("Nhập số lượng: ", "Số lượng")
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
        book_id = prompt_field("Nhập mã sách cần xóa: ", "Mã sách")
        if book_id is None:
            self.pause()
            return
        if not self.confirm_action("Bạn có chắc chắn muốn xóa sách này không?"):
            return
        result = self.service.remove_book(book_id)
        if result == "deleted":
            self.console.print("\n[bold green]✅ Xóa sách thành công![/bold green]")
        elif result == "borrowed":
            print_info_warning("Sách đang được mượn, không thể xóa.")
        else:
            print_info_error("Không tìm thấy sách!")
        self.pause()

    def update_book(self):
        self.console.print("\n[bold cyan]===== ✏️ CẬP NHẬT SÁCH =====[/bold cyan]")
        book_id = prompt_field("Nhập mã sách cần cập nhật: ", "Mã sách")
        if book_id is None:
            self.pause()
            return
        book = self.service.get_book_by_id(book_id)
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

        title = prompt_field("Tên sách mới (Enter để giữ): ", "Tên sách", allow_empty=True) or book.title
        author = prompt_field("Tác giả mới (Enter để giữ): ", "Tác giả", allow_empty=True) or book.author
        category = prompt_field("Thể loại mới (Enter để giữ): ", "Thể loại", allow_empty=True) or book.category
        isbn = prompt_field("ISBN mới (Enter để giữ): ", "ISBN", allow_empty=True) or book.isbn
        publish_year_input = prompt_optional_int(
            "Năm xuất bản mới (Enter để giữ): ",
            "Năm xuất bản",
        )
        publish_year = (
            book.publish_year
            if publish_year_input is None
            else publish_year_input
        )

        quantity_input = prompt_optional_int(
            "Số lượng mới (Enter để giữ): ",
            "Số lượng",
        )
        quantity = book.quantity if quantity_input is None else quantity_input

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

    def _display_search_results(self, results):
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
        keyword = prompt_field("Nhập tên sách cần tìm: ", "Tên sách")
        if keyword is None:
            self.pause()
            return
        results = self.service.search_books_by_title(keyword)
        self._display_search_results(results)

    def search_by_author(self):
        self.console.print("\n[bold cyan]===== ✍️ TÌM SÁCH THEO TÁC GIẢ =====[/bold cyan]")
        author = prompt_field("Nhập tên tác giả cần tìm: ", "Tên tác giả")
        if author is None:
            self.pause()
            return
        results = self.service.search_books_by_author(author)
        self._display_search_results(results)

    def search_advanced(self):
        self.console.print("\n[bold cyan]===== 🔎 TÌM KIẾM NÂNG CAO =====[/bold cyan]")
        title = prompt_field("👉 Tên sách (để trống nếu không muốn lọc): ", "Tên sách", allow_empty=True) or None
        author = prompt_field("👉 Tác giả (để trống nếu không muốn lọc): ", "Tác giả", allow_empty=True) or None
        genre = prompt_field("👉 Thể loại (để trống nếu không muốn lọc): ", "Thể loại", allow_empty=True) or None
        publish_year = prompt_optional_int(
            "👉 Năm xuất bản (để trống nếu không muốn lọc): ",
            "Năm xuất bản",
        )
        isbn = prompt_field("👉 ISBN (để trống nếu không có): ", "ISBN", allow_empty=True) or None
        availability = prompt_field(
            "👉 Tình trạng [all/available/unavailable] (mặc định all): ",
            "Tình trạng",
            allow_empty=True,
        ) or "all"
        results = self.service.search_books_advanced(
            title=title,
            author=author,
            genre=genre,
            publish_year=publish_year,
            isbn=isbn,
            availability=availability,
        )
        self._display_search_results(results)

    def run(self):
        self.run_menu(self.show_menu, {"1": self.add_book, "2": self.delete_book, "3": self.update_book, "4": self.display_books, "5": self.search_by_title, "6": self.search_by_author, "7": self.search_advanced})
