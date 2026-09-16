class BSTNode:

    # Khởi tạo Node của cây BST
    def __init__(self, book):
        self.book = book          # Thông tin sách
        self.left = None          # Node bên trái
        self.right = None         # Node bên phải


class BinarySearchTree:

    # Khởi tạo cây BST
    def __init__(self):
        self.root = None          # Node gốc

    # Thêm sách vào cây
    def insert(self, book):

        new_node = BSTNode(book)

        # Nếu cây rỗng
        if self.root is None:
            self.root = new_node
            return

        current = self.root

        while True:

            # Nếu mã sách nhỏ hơn Node hiện tại
            if book.book_id < current.book.book_id:

                if current.left is None:
                    current.left = new_node
                    return

                current = current.left

            # Nếu mã sách lớn hơn Node hiện tại
            elif book.book_id > current.book.book_id:

                if current.right is None:
                    current.right = new_node
                    return

                current = current.right

            # Nếu mã sách đã tồn tại
            else:
                return

    # Tìm kiếm sách theo mã
    def search(self, book_id):
        current = self.root

        while current is not None:

            # Tìm thấy sách
            if book_id == current.book.book_id:
                return current.book

            # Tìm sang cây bên trái
            elif book_id < current.book.book_id:
                current = current.left

            # Tìm sang cây bên phải
            else:
                current = current.right

        return None

    # Duyệt cây theo Inorder
    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.book)
            self.inorder(node.right)

    # Duyệt cây theo Preorder
    def preorder(self, node):
        if node is not None:
            print(node.book)
            self.preorder(node.left)
            self.preorder(node.right)

    # Duyệt cây theo Postorder
    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.book)