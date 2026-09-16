class Node:

    # Khởi tạo Node
    def __init__(self, data):
        self.data = data        # Dữ liệu
        self.next = None        # Node tiếp theo


class BookLinkedList:

    # Khởi tạo Linked List
    def __init__(self):
        self.head = None        # Node đầu tiên

    # Thêm sách vào danh sách
    def add_book(self, book):
        new_node = Node(book)

        # Nếu danh sách rỗng
        if not self.head:
            self.head = new_node
            return

        # Duyệt đến Node cuối
        current = self.head
        while current.next:
            current = current.next

        # Thêm Node mới vào cuối
        current.next = new_node

    # Hiển thị danh sách sách
    def display(self):
        current = self.head

        while current:
            print(current.data)
            current = current.next

    # Xóa sách theo mã
    def delete_book(self, book_id):

        # Kiểm tra danh sách rỗng
        if not self.head:
            return False

        # Xóa Node đầu tiên
        if self.head.data.book_id == book_id:
            self.head = self.head.next
            return True

        # Tìm Node cần xóa
        current = self.head
        while current.next:
            if current.next.data.book_id == book_id:
                current.next = current.next.next
                return True

            current = current.next

        return False

    # Tìm kiếm sách theo mã
    def search_book(self, book_id):
        current = self.head

        # Duyệt danh sách để tìm sách
        while current:
            if current.data.book_id == book_id:
                return current.data

            current = current.next

        return None