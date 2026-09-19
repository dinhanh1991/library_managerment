class Book:

    # Khởi tạo thông tin sách
    def __init__(self, book_id, title, author, publish_year, quantity, category="Chưa phân loại", isbn=""):
        self.book_id = book_id              # Mã sách
        self.title = title                  # Tên sách
        self.author = author                # Tác giả
        self.publish_year = publish_year    # Năm xuất bản
        self.quantity = quantity            # Số lượng
        self.category = (category or "Chưa phân loại").strip() or "Chưa phân loại"   # Thể loại
        self.isbn = (isbn or "").strip()  # Mã ISBN

    def is_available(self):
        """Return whether the book has at least one copy available."""
        return self.quantity > 0

    # Hiển thị thông tin sách
    def __str__(self):
        return (
            f"{self.book_id} | "
            f"{self.title} | "
            f"{self.author} | "
            f"{self.publish_year} | "
            f"{self.quantity} | "
            f"{self.category} | "
            f"{self.isbn}"
        )

    # Chuyển đối tượng thành Dictionary
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "publish_year": self.publish_year,
            "quantity": self.quantity,
            "category": self.category,
            "isbn": self.isbn
        }

    # Tạo đối tượng từ Dictionary
    @staticmethod
    def from_dict(data):
        required_fields = ["book_id", "title", "author", "publish_year", "quantity"]
        if not isinstance(data, dict):
            raise ValueError("Dữ liệu sách phải có dạng object JSON")
        if any(field not in data for field in required_fields):
            raise ValueError("Dữ liệu sách thiếu trường bắt buộc")
        if not isinstance(data["book_id"], str) or not data["book_id"].strip():
            raise ValueError("book_id của sách không hợp lệ")
        if not isinstance(data["title"], str) or not data["title"].strip():
            raise ValueError("title của sách không hợp lệ")
        if not isinstance(data["author"], str) or not data["author"].strip():
            raise ValueError("author của sách không hợp lệ")
        if not isinstance(data["publish_year"], int) or isinstance(data["publish_year"], bool):
            raise ValueError("publish_year của sách không hợp lệ")
        if not isinstance(data["quantity"], int) or isinstance(data["quantity"], bool) or data["quantity"] < 0:
            raise ValueError("quantity của sách không hợp lệ")

        category = data.get("category")
        if category is not None and not isinstance(category, str):
            raise ValueError("category của sách không hợp lệ")

        isbn = data.get("isbn")
        if isbn is not None and not isinstance(isbn, str):
            raise ValueError("isbn của sách không hợp lệ")

        return Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            publish_year=data["publish_year"],
            quantity=data["quantity"],
            category=category or "Chưa phân loại",
            isbn=isbn or ""
        )
