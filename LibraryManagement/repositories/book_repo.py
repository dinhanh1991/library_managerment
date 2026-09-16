import json
from pathlib import Path

from LibraryManagement.models.book import Book


class BookRepository:

    # Đường dẫn file lưu dữ liệu sách
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "books.json"

    # Đọc danh sách sách từ file
    def load_books(self):
        try:
            # Mở file JSON để đọc
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

                books = []

                # Chuyển dữ liệu thành đối tượng Book
                for item in data:
                    book = Book.from_dict(item)
                    books.append(book)

                return books

        # Nếu file chưa tồn tại thì trả về danh sách rỗng
        except FileNotFoundError:
            return []

    # Lưu danh sách sách vào file
    def save_books(self, books):
        try:
            data = []

            # Chuyển từng đối tượng Book thành Dictionary
            for book in books:
                data.append(book.to_dict())

            # Mở file để ghi dữ liệu
            with open(self.FILE_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        # Xử lý lỗi khi lưu dữ liệu
        except OSError as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")