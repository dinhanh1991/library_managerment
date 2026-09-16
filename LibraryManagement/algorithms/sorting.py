# ============================================================
# CÁC THUẬT TOÁN SẮP XẾP
# ============================================================
#
# Các thuật toán được cài đặt:
# 1. Bubble Sort
# 2. Selection Sort
# 3. Insertion Sort
# 4. Quick Sort
# 5. Merge Sort
# 6. Heap Sort
#
# Mỗi thuật toán hỗ trợ sắp xếp theo:
# - title: Tên sách
# - publish_year: Năm xuất bản
# - book_id: Mã sách (mặc định)
#
# Đồng thời đếm:
# - comparisons: Số phép so sánh
# - assignments: Số phép gán
# ============================================================


# ============================================================
# 1. BUBBLE SORT
# ============================================================

def bubble_sort(books, key):

    # Số lượng sách
    n = len(books)

    # Biến đếm số phép so sánh
    comparisons = 0

    # Biến đếm số phép gán
    assignments = 0

    # Duyệt qua từng vị trí trong danh sách
    for i in range(n):

        # So sánh các phần tử liền kề
        for j in range(0, n - i - 1):

            # Mỗi lần thực hiện điều kiện so sánh
            comparisons += 1

            # Xác định giá trị dùng để so sánh
            if key == "title":

                # Sắp xếp theo tên sách
                value1 = books[j].title
                value2 = books[j + 1].title

            elif key == "publish_year":

                # Sắp xếp theo năm xuất bản
                value1 = books[j].publish_year
                value2 = books[j + 1].publish_year

            else:

                # Mặc định sắp xếp theo mã sách
                value1 = books[j].book_id
                value2 = books[j + 1].book_id

            # Nếu phần tử trước lớn hơn phần tử sau
            # thì đổi chỗ hai phần tử
            if value1 > value2:

                temp = books[j]
                books[j] = books[j + 1]
                books[j + 1] = temp

                # Một lần đổi chỗ sử dụng 3 phép gán
                assignments += 3

    # Trả về danh sách sau khi sắp xếp
    # và số phép so sánh, số phép gán
    return books, comparisons, assignments


# ============================================================
# 2. SELECTION SORT
# ============================================================

def selection_sort(books, key):

    # Số lượng sách
    n = len(books)

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # Duyệt từng vị trí cần tìm phần tử nhỏ nhất
    for i in range(n):

        # Giả sử phần tử tại i là nhỏ nhất
        min_index = i

        # Tìm phần tử nhỏ nhất trong phần còn lại
        for j in range(i + 1, n):

            # Tăng số phép so sánh
            comparisons += 1

            # Xác định giá trị dùng để so sánh
            if key == "title":

                # So sánh theo tên sách
                value1 = books[j].title
                value2 = books[min_index].title

            elif key == "publish_year":

                # So sánh theo năm xuất bản
                value1 = books[j].publish_year
                value2 = books[min_index].publish_year

            else:

                # So sánh theo mã sách
                value1 = books[j].book_id
                value2 = books[min_index].book_id

            # Nếu tìm thấy phần tử nhỏ hơn
            if value1 < value2:

                # Cập nhật vị trí nhỏ nhất
                min_index = j

                assignments += 1

        # Nếu phần tử nhỏ nhất không nằm tại i
        if min_index != i:

            # Đổi chỗ hai phần tử
            temp = books[i]
            books[i] = books[min_index]
            books[min_index] = temp

            # 3 phép gán cho một lần đổi chỗ
            assignments += 3

    return books, comparisons, assignments


# ============================================================
# 3. INSERTION SORT
# ============================================================

def insertion_sort(books, key):

    # Số lượng sách
    n = len(books)

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # Bắt đầu từ phần tử thứ hai
    for i in range(1, n):

        # Lưu phần tử đang cần chèn
        key_book = books[i]

        assignments += 1

        # Vị trí ngay trước phần tử hiện tại
        j = i - 1

        # Dịch chuyển các phần tử lớn hơn sang phải
        while j >= 0:

            comparisons += 1

            # Xác định giá trị dùng để so sánh
            if key == "title":

                value1 = key_book.title
                value2 = books[j].title

            elif key == "publish_year":

                value1 = key_book.publish_year
                value2 = books[j].publish_year

            else:

                value1 = key_book.book_id
                value2 = books[j].book_id

            # Nếu phần tử hiện tại nhỏ hơn
            # phần tử phía trước
            if value1 < value2:

                # Dịch phần tử phía trước sang phải
                books[j + 1] = books[j]

                assignments += 1

                j -= 1

            else:

                # Đã tìm được vị trí cần chèn
                break

        # Đưa phần tử vào vị trí thích hợp
        books[j + 1] = key_book

        assignments += 1

    return books, comparisons, assignments


# ============================================================
# 4. QUICK SORT
# ============================================================

def quick_sort(books, key):

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # --------------------------------------------------------
    # Hàm lấy giá trị dùng để so sánh
    # --------------------------------------------------------

    def get_value(book):

        if key == "title":

            # Sắp xếp theo tên
            return book.title

        elif key == "publish_year":

            # Sắp xếp theo năm
            return book.publish_year

        else:

            # Mặc định theo mã sách
            return book.book_id

    # --------------------------------------------------------
    # Hàm partition
    #
    # Chọn phần tử cuối làm pivot.
    # Các phần tử nhỏ hơn pivot được đưa sang bên trái.
    # Các phần tử lớn hơn pivot được đưa sang bên phải.
    # --------------------------------------------------------

    def partition(arr, low, high):

        # Cho phép thay đổi biến đếm của hàm quick_sort
        nonlocal comparisons, assignments

        # Chọn phần tử cuối làm pivot
        pivot = arr[high]

        assignments += 1

        # Vị trí cuối của nhóm phần tử nhỏ hơn pivot
        i = low - 1

        # Duyệt qua các phần tử từ low đến high - 1
        for j in range(low, high):

            comparisons += 1

            # Nếu phần tử hiện tại nhỏ hơn pivot
            if get_value(arr[j]) < get_value(pivot):

                i += 1

                # Đổi chỗ arr[i] và arr[j]
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp

                assignments += 3

        # Đưa pivot về đúng vị trí
        temp = arr[i + 1]
        arr[i + 1] = arr[high]
        arr[high] = temp

        assignments += 3

        # Trả về vị trí của pivot
        return i + 1

    # --------------------------------------------------------
    # Hàm Quick Sort đệ quy
    # --------------------------------------------------------

    def quick_sort_recursive(arr, low, high):

        # Chỉ thực hiện khi đoạn danh sách còn ít nhất 2 phần tử
        if low < high:

            # Chia danh sách thành hai phần
            pivot_index = partition(
                arr,
                low,
                high
            )

            # Sắp xếp phần bên trái
            quick_sort_recursive(
                arr,
                low,
                pivot_index - 1
            )

            # Sắp xếp phần bên phải
            quick_sort_recursive(
                arr,
                pivot_index + 1,
                high
            )

    # Bắt đầu Quick Sort trên toàn bộ danh sách
    quick_sort_recursive(
        books,
        0,
        len(books) - 1
    )

    return books, comparisons, assignments


# ============================================================
# 5. MERGE SORT
# ============================================================

def merge(left, right, key):

    # Danh sách dùng để lưu kết quả sau khi trộn
    result = []

    # Vị trí hiện tại của danh sách left
    i = 0

    # Vị trí hiện tại của danh sách right
    j = 0

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # --------------------------------------------------------
    # Hàm lấy giá trị dùng để so sánh
    # --------------------------------------------------------

    def get_value(book):

        if key == "title":

            return book.title

        elif key == "publish_year":

            return book.publish_year

        else:

            return book.book_id

    # --------------------------------------------------------
    # Trộn hai danh sách đã được sắp xếp
    # --------------------------------------------------------

    while i < len(left) and j < len(right):

        comparisons += 1

        # So sánh phần tử hiện tại của hai danh sách
        if get_value(left[i]) < get_value(right[j]):

            # Đưa phần tử nhỏ hơn vào result
            result.append(left[i])

            assignments += 1

            i += 1

        else:

            result.append(right[j])

            assignments += 1

            j += 1

    # --------------------------------------------------------
    # Đưa các phần tử còn lại của left vào result
    # --------------------------------------------------------

    while i < len(left):

        result.append(left[i])

        assignments += 1

        i += 1

    # --------------------------------------------------------
    # Đưa các phần tử còn lại của right vào result
    # --------------------------------------------------------

    while j < len(right):

        result.append(right[j])

        assignments += 1

        j += 1

    return result, comparisons, assignments


def merge_sort(books, key):

    # Nếu danh sách có 0 hoặc 1 phần tử
    # thì danh sách đã được sắp xếp
    if len(books) <= 1:

        return books, 0, 0

    # Tìm vị trí giữa danh sách
    mid = len(books) // 2

    # Chia danh sách thành hai nửa
    left = books[:mid]
    right = books[mid:]

    # Sắp xếp đệ quy nửa bên trái
    left, comparisons_left, assignments_left = merge_sort(
        left,
        key
    )

    # Sắp xếp đệ quy nửa bên phải
    right, comparisons_right, assignments_right = merge_sort(
        right,
        key
    )

    # Trộn hai nửa đã được sắp xếp
    result, comparisons_merge, assignments_merge = merge(
        left,
        right,
        key
    )

    # Tổng số phép so sánh
    comparisons = (
        comparisons_left
        + comparisons_right
        + comparisons_merge
    )

    # Tổng số phép gán
    assignments = (
        assignments_left
        + assignments_right
        + assignments_merge
    )

    return result, comparisons, assignments


# ============================================================
# 6. HEAP SORT
# ============================================================

def heapify(books, n, i, key):

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # --------------------------------------------------------
    # Hàm lấy giá trị dùng để so sánh
    # --------------------------------------------------------

    def get_value(book):

        if key == "title":

            return book.title

        elif key == "publish_year":

            return book.publish_year

        else:

            return book.book_id

    # Ban đầu giả sử node hiện tại là lớn nhất
    largest = i

    # Vị trí của node con bên trái
    left = 2 * i + 1

    # Vị trí của node con bên phải
    right = 2 * i + 2

    # --------------------------------------------------------
    # Kiểm tra node con bên trái
    # --------------------------------------------------------

    if left < n:

        comparisons += 1

        if get_value(books[left]) > get_value(books[largest]):

            largest = left

            assignments += 1

    # --------------------------------------------------------
    # Kiểm tra node con bên phải
    # --------------------------------------------------------

    if right < n:

        comparisons += 1

        if get_value(books[right]) > get_value(books[largest]):

            largest = right

            assignments += 1

    # --------------------------------------------------------
    # Nếu node lớn nhất không phải node hiện tại
    # thì đổi chỗ
    # --------------------------------------------------------

    if largest != i:

        temp = books[i]
        books[i] = books[largest]
        books[largest] = temp

        assignments += 3

        # Tiếp tục heapify ở node con
        child_comparisons, child_assignments = heapify(
            books,
            n,
            largest,
            key
        )

        # Cộng dồn số phép so sánh và phép gán
        comparisons += child_comparisons
        assignments += child_assignments

    return comparisons, assignments


def heap_sort(books, key):

    # Số lượng sách
    n = len(books)

    # Biến đếm phép so sánh
    comparisons = 0

    # Biến đếm phép gán
    assignments = 0

    # --------------------------------------------------------
    # BƯỚC 1: Xây dựng Max Heap
    # --------------------------------------------------------

    for i in range(n // 2 - 1, -1, -1):

        heap_comparisons, heap_assignments = heapify(
            books,
            n,
            i,
            key
        )

        comparisons += heap_comparisons
        assignments += heap_assignments

    # --------------------------------------------------------
    # BƯỚC 2:
    # Đưa phần tử lớn nhất về cuối danh sách
    # --------------------------------------------------------

    for i in range(n - 1, 0, -1):

        # Đổi phần tử đầu tiên với phần tử cuối
        temp = books[0]
        books[0] = books[i]
        books[i] = temp

        assignments += 3

        # Xây dựng lại Max Heap
        heap_comparisons, heap_assignments = heapify(
            books,
            i,
            0,
            key
        )

        comparisons += heap_comparisons
        assignments += heap_assignments

    return books, comparisons, assignments
