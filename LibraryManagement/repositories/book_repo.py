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

            if not isinstance(data, list):
                raise ValueError("Dữ liệu sách phải có dạng danh sách JSON.")

            books = []

            # Chuyển dữ liệu thành đối tượng Book
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Mỗi dữ liệu sách phải có dạng object JSON.")
                book = Book.from_dict(item)
                books.append(book)

            return books

        # Nếu file chưa tồn tại thì trả về danh sách rỗng
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise ValueError(f"File dữ liệu sách không hợp lệ: {e}") from e

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