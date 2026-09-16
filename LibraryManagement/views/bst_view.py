from rich.table import Table

from LibraryManagement.views.base_view import BaseView

class BSTView(BaseView):

    # ============================================================
    # KHỞI TẠO BST VIEW
    # ============================================================

    def __init__(self, service):
        super().__init__(service)

    # ============================================================
    # HIỂN THỊ MENU QUẢN LÝ BST
    # ============================================================

    def show_menu(self):
        menu_content = (
            " [1] 🔍 Tìm sách theo mã bằng BST\n"
            " [2] 📋 Duyệt Inorder\n"
            " [3] 📋 Duyệt Preorder\n"
            " [4] 📋 Duyệt Postorder\n"
            " [0] 🔙 Quay lại"
        )
        self.render_menu("🌳 QUẢN LÝ BST", menu_content)

    # ============================================================
    # TẠM DỪNG MÀN HÌNH
    # ============================================================

    # ============================================================
    # HIỂN THỊ THÔNG TIN SÁCH
    # ============================================================

    def display_book(self, book):

        # Tạo bảng thông tin sách
        table = Table(
            title="📚 KẾT QUẢ TÌM KIẾM",
            header_style="bold magenta",
            border_style="blue"
        )

        # Thêm các cột
        table.add_column(
            "MÃ SÁCH",
            justify="center",
            style="cyan",
            no_wrap=True
        )

        table.add_column(
            "TÊN SÁCH",
            style="green"
        )

        table.add_column(
            "TÁC GIẢ",
            style="yellow"
        )

        table.add_column(
            "NĂM",
            justify="center"
        )

        table.add_column(
            "SL",
            justify="center"
        )

        # Thêm thông tin sách vào bảng
        table.add_row(
            str(book.book_id),
            str(book.title),
            str(book.author),
            str(book.publish_year),
            str(book.quantity)
        )

        # Hiển thị bảng
        self.console.print()
        self.console.print(table)

    # ============================================================
    # TÌM SÁCH BẰNG BST
    # ============================================================

    def search_book(self):

        self.console.print(
            "\n[bold cyan]===== 🔍 TÌM SÁCH BẰNG BST =====[/bold cyan]"
        )

        # Nhập mã sách
        book_id = input(
            "👉 Nhập mã sách cần tìm: "
        ).strip()

        # Kiểm tra dữ liệu nhập
        if not book_id:

            self.console.print(
                "\n[bold yellow]"
                "⚠️ Mã sách không được để trống."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Gọi Service tìm kiếm bằng BST
        book = self.service.search_book_by_bst(
            book_id
        )

        # Nếu tìm thấy
        if book:

            self.display_book(book)

        # Nếu không tìm thấy
        else:

            self.console.print(
                "\n[bold red]"
                "❌ Không tìm thấy sách."
                "[/bold red]"
            )

        self.pause()

    # ============================================================
    # DUYỆT BST - INORDER
    # ============================================================

    def display_inorder(self):

        self.console.print(
            "\n[bold cyan]===== 📋 BST INORDER =====[/bold cyan]"
        )

        # Xây dựng BST từ dữ liệu sách
        bst = self.service.build_book_bst()

        # Kiểm tra BST có rỗng không
        if bst.root is None:

            self.console.print(
                "\n[bold yellow]"
                "📭 Thư viện chưa có sách."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Hiển thị tiêu đề
        self.console.print(
            "\n[bold green]"
            "📋 KẾT QUẢ DUYỆT INORDER:"
            "[/bold green]"
        )

        # Thực hiện duyệt Inorder
        bst.inorder(bst.root)

        self.pause()

    # ============================================================
    # DUYỆT BST - PREORDER
    # ============================================================

    def display_preorder(self):

        self.console.print(
            "\n[bold cyan]===== 📋 BST PREORDER =====[/bold cyan]"
        )

        # Xây dựng BST
        bst = self.service.build_book_bst()

        # Kiểm tra BST rỗng
        if bst.root is None:

            self.console.print(
                "\n[bold yellow]"
                "📭 Thư viện chưa có sách."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Hiển thị tiêu đề
        self.console.print(
            "\n[bold green]"
            "📋 KẾT QUẢ DUYỆT PREORDER:"
            "[/bold green]"
        )

        # Thực hiện duyệt Preorder
        bst.preorder(bst.root)

        self.pause()

    # ============================================================
    # DUYỆT BST - POSTORDER
    # ============================================================

    def display_postorder(self):

        self.console.print(
            "\n[bold cyan]===== 📋 BST POSTORDER =====[/bold cyan]"
        )

        # Xây dựng BST
        bst = self.service.build_book_bst()

        # Kiểm tra BST rỗng
        if bst.root is None:

            self.console.print(
                "\n[bold yellow]"
                "📭 Thư viện chưa có sách."
                "[/bold yellow]"
            )

            self.pause()
            return

        # Hiển thị tiêu đề
        self.console.print(
            "\n[bold green]"
            "📋 KẾT QUẢ DUYỆT POSTORDER:"
            "[/bold green]"
        )

        # Thực hiện duyệt Postorder
        bst.postorder(bst.root)

        self.pause()

    # ============================================================
    # CHẠY CHƯƠNG TRÌNH
    # ============================================================

    def run(self):
        self.run_menu(
            self.show_menu,
            {
                "1": self.search_book,
                "2": self.display_inorder,
                "3": self.display_preorder,
                "4": self.display_postorder,
            },
        )
