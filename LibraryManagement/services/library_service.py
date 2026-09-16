from datetime import date, timedelta

from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.models.reader import Reader
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.bts import BinarySearchTree


class LibraryService:

    LOAN_PERIOD_DAYS = 14

    # Khởi tạo các thành phần của hệ thống
    def __init__(self):
        self.repository = BookRepository()              # Quản lý dữ liệu sách
        self.borrower_repo = BorrowerRepository()       # Quản lý dữ liệu người mượn
        self.queue_repo = QueueRepository()             # Lưu hàng đợi mượn sách
        self.reader_repo = ReaderRepository()            # Quản lý hồ sơ độc giả
        self.return_history_repo = ReturnHistoryRepository()
        self.borrow_queue = Queue()                     # Hàng đợi mượn sách
        self._load_borrow_queue()
        self.book_bst = BinarySearchTree()               # Cây tìm kiếm sách
        self.return_stack = Stack()                     # Ngăn xếp trả sách
        self._load_return_history()
        self.book_linked_list = BookLinkedList()         # Danh sách liên kết sách

    def _load_borrow_queue(self):
        for borrower in self.queue_repo.load_queue():
            self.borrow_queue.enqueue(borrower)

    def _save_borrow_queue(self):
        self.queue_repo.save_queue(self.borrow_queue.items)

    def _load_return_history(self):
        for borrower in self.return_history_repo.load_history():
            self.return_stack.push(borrower)

    def _save_return_history(self):
        self.return_history_repo.save_history(self.return_stack.items)

    def get_all_readers(self):
        return self.reader_repo.load_readers()

    def add_reader(self, reader):
        if reader is None:
            return False

        reader_id = str(reader.reader_id or "").strip()
        reader_name = str(reader.name or "").strip()

        if not reader_id or not reader_name:
            return False

        reader.reader_id = reader_id
        reader.name = reader_name

        readers = self.reader_repo.load_readers()
        if any(item.reader_id == reader.reader_id for item in readers):
            return False

        readers.append(reader)
        self.reader_repo.save_readers(readers)
        return True

    def update_reader(self, updated_reader):
        if updated_reader is None:
            return False

        reader_id = str(updated_reader.reader_id or "").strip()
        reader_name = str(updated_reader.name or "").strip()

        if not reader_id or not reader_name:
            return False

        updated_reader.reader_id = reader_id
        updated_reader.name = reader_name

        readers = self.reader_repo.load_readers()
        for reader in readers:
            if reader.reader_id == updated_reader.reader_id:
                reader.name = updated_reader.name
                self.reader_repo.save_readers(readers)

                active_borrowers = self.borrower_repo.load_borrowers()
                changed = False
                for borrower in active_borrowers:
                    if borrower.borrower_id == updated_reader.reader_id:
                        borrower.name = updated_reader.name
                        changed = True
                if changed:
                    self.borrower_repo.save_borrowers(active_borrowers)

                queue_changed = False
                for borrower in self.borrow_queue.items:
                    if borrower.borrower_id == updated_reader.reader_id:
                        borrower.name = updated_reader.name
                        queue_changed = True
                if queue_changed:
                    self._save_borrow_queue()
                return True

        return False

    def remove_reader(self, reader_id):
        active_borrowers = self.borrower_repo.load_borrowers()
        if any(item.borrower_id == reader_id for item in active_borrowers):
            return False

        readers = self.reader_repo.load_readers()
        remaining = [reader for reader in readers if reader.reader_id != reader_id]
        if len(remaining) == len(readers):
            return False

        self.reader_repo.save_readers(remaining)
        return True

    def get_reader_history(self, reader_id):
        transactions = [
            borrower
            for borrower in self.borrower_repo.load_borrowers()
            if borrower.borrower_id == reader_id
        ]
        transactions.extend(
            borrower
            for borrower in self.return_history_repo.load_history()
            if borrower.borrower_id == reader_id
        )
        return transactions

    def get_overdue_borrowers(self, as_of=None):
        current_date = as_of or date.today()
        overdue = []
        for borrower in self.borrower_repo.load_borrowers():
            if self._is_overdue(borrower, current_date):
                overdue.append(borrower)
        return overdue

    @staticmethod
    def _is_overdue(borrower, as_of):
        if borrower.status not in {"pending", "borrowed"} or not borrower.due_date:
            return False
        try:
            due_date = date.fromisoformat(borrower.due_date)
        except ValueError:
            return False
        return due_date < as_of

    def _ensure_reader(self, borrower):
        readers = self.reader_repo.load_readers()
        if any(reader.reader_id == borrower.borrower_id for reader in readers):
            return
        readers.append(Reader(borrower.borrower_id, borrower.name))
        self.reader_repo.save_readers(readers)

    # Lấy tất cả sách
    def get_all_books(self):
        return self.repository.load_books()

    # Tạo danh sách liên kết từ dữ liệu sách
    def build_book_linked_list(self):
        books = self.repository.load_books()

        self.book_linked_list = BookLinkedList()

        # Thêm từng sách vào danh sách liên kết
        for book in books:
            self.book_linked_list.add_book(book)

        return self.book_linked_list

    # Tạo cây tìm kiếm từ dữ liệu sách
    def build_book_bst(self):
        books = self.repository.load_books()

        self.book_bst = BinarySearchTree()

        # Thêm từng sách vào cây
        for book in books:
            self.book_bst.insert(book)

        return self.book_bst

    def _refresh_structures(self):
        self.book_linked_list = self.build_book_linked_list()
        self.book_bst = self.build_book_bst()

    # Thêm sách
    def add_book(self, book):
        books = self.repository.load_books()
        for existing in books:
            if existing.book_id == book.book_id:
                return False
        books.append(book)

        self.repository.save_books(books)
        self._refresh_structures()
        return True

    # Xóa sách theo mã
    def remove_book(self, book_id):
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()

        if any(item.book_id == book_id for item in borrowers):
            return False

        for book in books:
            if book.book_id == book_id:
                books.remove(book)
                self.repository.save_books(books)
                self._refresh_structures()
                return True

        return False

    # Cập nhật thông tin sách
    def update_book(self, updated_book):
        if updated_book is None or updated_book.quantity < 0:
            return False

        books = self.repository.load_books()

        for i, book in enumerate(books):
            if book.book_id == updated_book.book_id:

                books[i] = updated_book
                self.repository.save_books(books)
                self._refresh_structures()
                return True

        return False

    # Tìm kiếm sách theo tên
    def search_books_by_title(self, keyWork):
        books = self.repository.load_books()
        results = []

        for book in books:
            if keyWork.lower() in book.title.lower():
                results.append(book)

        return results

    # Tìm kiếm sách theo tác giả
    def search_books_by_author(self, author):
        books = self.repository.load_books()
        results = []

        for book in books:
            if author.lower() in book.author.lower():
                results.append(book)

        return results

    # Tìm kiếm nâng cao
    def search_books_advanced(
        self,
        title=None,
        author=None,
        genre=None,
        publish_year=None,
        isbn=None,
        availability=None,
    ):
        books = self.repository.load_books()
        results = []

        normalized_title = (title or "").strip().lower()
        normalized_author = (author or "").strip().lower()
        normalized_genre = (genre or "").strip().lower()
        normalized_isbn = (isbn or "").strip().lower()

        try:
            normalized_year = int(publish_year) if publish_year not in (None, "") else None
        except (TypeError, ValueError):
            normalized_year = None

        normalized_availability = (availability or "all").strip().lower()

        for book in books:
            if normalized_title and normalized_title not in str(book.title).lower():
                continue
            if normalized_author and normalized_author not in str(book.author).lower():
                continue
            if normalized_genre and normalized_genre not in str(getattr(book, "category", "")).lower():
                continue
            if normalized_year is not None and book.publish_year != normalized_year:
                continue
            if normalized_isbn and normalized_isbn not in str(getattr(book, "isbn", "")).lower():
                continue

            if normalized_availability == "available" and book.quantity <= 0:
                continue
            if normalized_availability == "unavailable" and book.quantity > 0:
                continue

            results.append(book)

        return results

    # Mượn sách
    def book_borrow(self, borrower):
        # Kiểm tra dữ liệu đầu vào ở Service để nghiệp vụ không phụ thuộc View.
        borrower_id = str(borrower.borrower_id or "").strip()
        borrower_name = str(borrower.name or "").strip()
        book_id = str(borrower.book_id or "").strip()

        if not borrower_id:
            print("Mã độc giả không được để trống.")
            return False

        if not borrower_name:
            print("Tên độc giả không được để trống.")
            return False

        if not book_id:
            print("Mã sách không được để trống.")
            return False

        borrower.borrower_id = borrower_id
        borrower.name = borrower_name
        borrower.book_id = book_id

        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()

        active_borrower = None
        for item in borrowers:
            if item.borrower_id == borrower.borrower_id:
                active_borrower = item
                break

        if active_borrower is not None:
            if self._is_overdue(active_borrower, date.today()):
                print(f"Độc giả {borrower.borrower_id} đang có sách quá hạn.")
            else:
                print(f"Độc giả {borrower.borrower_id} đang có sách trong hệ thống.")
            return False

        for item in self.borrow_queue.items:
            if (
                item.borrower_id == borrower.borrower_id
                and item.book_id == borrower.book_id
            ):
                print(f"Độc giả {borrower.borrower_id} đã có yêu cầu mượn trong hàng đợi.")
                return False

        book = None
        for item in books:
            if item.book_id == borrower.book_id:
                book = item
                break

        if book is None:
            print(f"Sách có ID {borrower.book_id} không tồn tại trong thư viện.")
            return False

        if book.quantity <= 0:
            print(f"Sách có ID {borrower.book_id} hiện không có sẵn để mượn.")
            return False

        borrow_date = date.today()
        borrower.borrow_date = borrow_date.isoformat()
        borrower.due_date = (
            borrow_date + timedelta(days=self.LOAN_PERIOD_DAYS)
        ).isoformat()
        borrower.return_date = None
        borrower.status = "pending"

        self._ensure_reader(borrower)

        book.quantity -= 1
        self.repository.save_books(books)
        self._refresh_structures()

        self.borrow_queue.enqueue(borrower)
        self._save_borrow_queue()

        borrowers.append(borrower)
        self.borrower_repo.save_borrowers(borrowers)

        print(f"{borrower.name} đã đăng ký mượn sách '{book.title}'.")
        print(
            f"Hạn trả dự kiến: {borrower.due_date} | "
            f"Trạng thái: {borrower.status}"
        )
        return True

    # Xử lý người mượn tiếp theo trong hàng đợi
    def process_next_borrower(self):

        if self.borrow_queue.is_empty():
            print("Không có người mượn nào trong hàng đợi.")
            return None

        borrower = self.borrow_queue.dequeue()
        self._save_borrow_queue()

        borrowers = self.borrower_repo.load_borrowers()
        active_borrower = next(
            (
                item
                for item in borrowers
                if item.borrower_id == borrower.borrower_id
                and item.book_id == borrower.book_id
            ),
            None,
        )

        if active_borrower is not None:
            active_borrower.status = "borrowed"
            self.borrower_repo.save_borrowers(borrowers)
            borrower = active_borrower

        print(
            f"Đang xử lý người mượn: {borrower.name}"
            f"- sách {borrower.book_id}"
        )

        return borrower

    # Trả sách
    def return_book(self, borrower):
        # Kiểm tra đối tượng đầu vào trước khi truy cập thuộc tính.
        if borrower is None:
            print("Thông tin trả sách không hợp lệ.")
            return False

        borrower_id = str(borrower.borrower_id or "").strip()
        book_id = str(borrower.book_id or "").strip()

        if not borrower_id:
            print("Mã độc giả không được để trống.")
            return False

        if not book_id:
            print("Mã sách không được để trống.")
            return False

        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()

        # Chỉ dùng mã độc giả + mã sách để xác định giao dịch.
        # Tên nhập vào khi trả không được phép thay đổi dữ liệu đã lưu.
        active_borrower = next(
            (
                item
                for item in borrowers
                if item.borrower_id == borrower_id
                and item.book_id == book_id
            ),
            None,
        )

        if active_borrower is None:
            print(f"Độc giả {borrower_id} không có lượt mượn hợp lệ.")
            return False

        if active_borrower.status not in {"pending", "borrowed"}:
            print(f"Giao dịch của độc giả {borrower_id} đã kết thúc.")
            return False

        # Phải tìm thấy sách trước khi thay đổi bất kỳ dữ liệu giao dịch nào.
        book = next(
            (item for item in books if item.book_id == book_id),
            None,
        )

        if book is None:
            print(f"Sách có ID {book_id} không tồn tại trong thư viện.")
            return False

        # Hoàn tất giao dịch sau khi đã xác nhận đủ dữ liệu.
        book.quantity += 1
        active_borrower.return_date = date.today().isoformat()
        active_borrower.status = "returned"

        self.repository.save_books(books)
        self._refresh_structures()

        self.return_stack.push(active_borrower)
        self._save_return_history()

        print(f"{active_borrower.name} đã trả sách '{book.title}'.")

        borrowers = [
            item
            for item in borrowers
            if not (
                item.borrower_id == borrower_id
                and item.book_id == book_id
            )
        ]
        self.borrower_repo.save_borrowers(borrowers)

        self.borrow_queue.items = [
            item
            for item in self.borrow_queue.items
            if not (
                item.borrower_id == borrower_id
                and item.book_id == book_id
            )
        ]
        self._save_borrow_queue()

        return True

    # Tìm kiếm sách bằng cây BST
    def search_book_by_bst(self, book_id):
        bst = self.build_book_bst()

        return bst.search(book_id)

    # Hiển thị cây theo thứ tự Preorder
    def display_book_preorder(self):
        bst = self.build_book_bst()

        print("Preorder: ", bst.preorder())

    # Hiển thị cây theo thứ tự Inorder
    def display_book_inorder(self):
        bst = self.build_book_bst()

        print("Inorder: ", bst.inorder())

    # Hiển thị cây theo thứ tự Postorder
    def display_book_postorder(self):
        bst = self.build_book_bst()

        print("Postorder: ", bst.postorder())

    # Tìm kiếm sách bằng danh sách liên kết
    def search_book_by_linked_list(self, book_id):
        linked_list = self.build_book_linked_list()

        return linked_list.search_book(book_id)
