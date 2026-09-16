class Queue:

    # Khởi tạo Queue
    def __init__(self):
        self.items = []    # Danh sách phần tử

    # Thêm phần tử vào Queue
    def enqueue(self, borrower):
        self.items.append(borrower)

    # Kiểm tra Queue có rỗng không
    def is_empty(self):
        return len(self.items) == 0

    # Lấy phần tử đầu tiên ra khỏi Queue
    def dequeue(self):
        if not self.items:
            return None

        return self.items.pop(0)

    def remove_by_borrower_id(self, borrower_id):
        self.items = [
            borrower
            for borrower in self.items
            if borrower.borrower_id != borrower_id
        ]