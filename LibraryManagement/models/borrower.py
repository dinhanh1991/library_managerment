from datetime import date


class Borrower:

    def is_active(self):
        return self.status in {"pending", "borrowed"}

    def is_borrowing_book(self, book_id):
        return self.is_active() and self.book_id == book_id

    def is_overdue(self, as_of=None):
        """Return whether this borrower is currently overdue."""
        if self.status not in {"pending", "borrowed"} or not self.due_date:
            return False
        as_of = as_of or date.today()
        try:
            due_date = date.fromisoformat(self.due_date)
        except ValueError:
            return False
        return due_date < as_of

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
            "borrower_id": self.borrower_id,
            "name": self.name,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
        }

    # Tạo đối tượng từ Dictionary
    @staticmethod
    def from_dict(data, default_status="borrowed"):
        required_fields = ["borrower_id", "name", "book_id"]
        if any(field not in data for field in required_fields):
            raise ValueError("Dữ liệu người mượn thiếu trường bắt buộc")
        if not isinstance(data["borrower_id"], str) or not data["borrower_id"].strip():
            raise ValueError("borrower_id không hợp lệ")
        if not isinstance(data["name"], str) or not data["name"].strip():
            raise ValueError("name của người mượn không hợp lệ")
        if not isinstance(data["book_id"], str) or not data["book_id"].strip():
            raise ValueError("book_id của người mượn không hợp lệ")

        status = data.get("status", default_status)
        if status not in {"pending", "borrowed", "returned"}:
            raise ValueError("status của người mượn không hợp lệ")

        for field in ["borrow_date", "due_date", "return_date"]:
            value = data.get(field)
            if value is not None:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"{field} của người mượn không hợp lệ")
                try:
                    date.fromisoformat(value)
                except ValueError as exc:
                    raise ValueError(f"{field} của người mượn không hợp lệ") from exc

        return Borrower(
            borrower_id=data["borrower_id"],
            name=data["name"],
            book_id=data["book_id"],
            borrow_date=data.get("borrow_date"),
            due_date=data.get("due_date"),
            return_date=data.get("return_date"),
            status=status,
        )
