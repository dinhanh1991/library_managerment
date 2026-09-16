class Book:

    # Khởi tạo thông tin sách
    def __init__(self, book_id, title, author, publish_year, quantity, category="", isbn=""):
        self.book_id = book_id              # Mã sách
        self.title = title                  # Tên sách
        self.author = author                # Tác giả
        self.publish_year = publish_year    # Năm xuất bản
        self.quantity = quantity            # Số lượng
        self.category = category            # Thể loại
        self.isbn = isbn                    # Mã ISBN

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
            "book_id": self.book_id,              # Mã sách
            "title": self.title,                  # Tên sách
            "author": self.author,                # Tác giả
            "publish_year": self.publish_year,    # Năm xuất bản
            "quantity": self.quantity,            # Số lượng
            "category": self.category,            # Thể loại
            "isbn": self.isbn                     # Mã ISBN
        }

    # Tạo đối tượng từ Dictionary
    @staticmethod
    def from_dict(data):
        return Book(
            book_id=data.get("book_id"),              # Mã sách
            title=data.get("title"),                  # Tên sách
            author=data.get("author"),                # Tác giả
            publish_year=data.get("publish_year"),    # Năm xuất bản
            quantity=data.get("quantity"),            # Số lượng
            category=data.get("category", ""),      # Thể loại
            isbn=data.get("isbn", "")               # Mã ISBN
        )