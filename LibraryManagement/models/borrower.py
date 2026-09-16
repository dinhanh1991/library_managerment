class Borrower:

    # Khởi tạo thông tin người mượn
    def __init__(
        self,
        borrower_id,
        name,
        book_id,
        borrow_date=None,
        due_date=None,
        return_date=None,
        status="borrowed",
    ):
        self.borrower_id = borrower_id    # Mã người mượn
        self.name = name                  # Tên người mượn
        self.book_id = book_id            # Mã sách mượn
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    # Hiển thị thông tin người mượn
    def __str__(self):
        return (
            f"{self.borrower_id} | "
            f"{self.name} | "
            f"{self.book_id} | "
            f"{self.status}"
        )

    # Chuyển đối tượng thành Dictionary
    def to_dict(self):
        return {
            "borrower_id": self.borrower_id,    # Mã người mượn
            "name": self.name,                  # Tên người mượn
            "book_id": self.book_id,             # Mã sách
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
        }

    # Tạo đối tượng từ Dictionary
    @staticmethod
    def from_dict(data, default_status="borrowed"):
        return Borrower(
            borrower_id=data.get("borrower_id"),    # Mã người mượn
            name=data.get("name"),                  # Tên người mượn
            book_id=data.get("book_id"),             # Mã sách
            borrow_date=data.get("borrow_date"),
            due_date=data.get("due_date"),
            return_date=data.get("return_date"),
            status=data.get("status", default_status),
        )