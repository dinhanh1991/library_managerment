class Stack:

    # Khởi tạo Stack
    def __init__(self):
        self.items = []    # Danh sách phần tử

    # Thêm phần tử vào Stack
    def push(self, item):
        self.items.append(item)

    # Lấy phần tử trên cùng ra khỏi Stack
    def pop(self):
        if not self.items:
            return None

        return self.items.pop()

    # Kiểm tra Stack có rỗng không
    def is_empty(self):
        return len(self.items) == 0