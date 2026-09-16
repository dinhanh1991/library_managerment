# 📚 Library Management

## 1. Giới thiệu

**Library Management** là ứng dụng quản lý thư viện được xây dựng bằng **Python**, áp dụng các kiến thức về **Cấu trúc dữ liệu và Giải thuật**.

Chương trình mô phỏng các nghiệp vụ cơ bản của một thư viện như quản lý sách, quản lý độc giả, mượn sách, trả sách và tìm kiếm sách. Bên cạnh đó, chương trình sử dụng các cấu trúc dữ liệu và thuật toán tự cài đặt để minh họa cách chúng được áp dụng vào một bài toán thực tế.

---

## 2. Mục tiêu

- Xây dựng chương trình quản lý thư viện bằng Python.
- Áp dụng các cấu trúc dữ liệu:
  - Queue
  - Stack
  - Linked List
  - Binary Search Tree
- Cài đặt và sử dụng các thuật toán sắp xếp.
- Thực hiện tìm kiếm và quản lý dữ liệu sách.
- Đánh giá hiệu năng của các thuật toán thông qua Benchmark.
- Tổ chức chương trình theo mô hình nhiều thành phần, dễ bảo trì và mở rộng.

---

## 3. Chức năng chính

### 3.1. Quản lý sách

Chương trình hỗ trợ:

- Thêm sách.
- Xóa sách.
- Cập nhật thông tin sách.
- Hiển thị danh sách sách.
- Tìm kiếm sách theo tên.
- Tìm kiếm sách theo tác giả.
- Tìm kiếm nâng cao.

Thông tin sách gồm:

- Mã sách.
- Tên sách.
- Tác giả.
- Năm xuất bản.
- Số lượng.
- Thể loại.
- ISBN.

### 3.2. Quản lý độc giả

Chương trình hỗ trợ:

- Thêm độc giả.
- Xóa độc giả.
- Cập nhật thông tin độc giả.
- Hiển thị danh sách độc giả.
- Tìm kiếm độc giả.

### 3.3. Mượn và trả sách

Khi độc giả mượn sách, chương trình kiểm tra:

- Sách có tồn tại hay không.
- Số lượng sách còn hay không.
- Độc giả có đang mượn sách hay không.

Sau khi mượn thành công, số lượng sách được cập nhật và thông tin mượn được lưu lại.

Khi trả sách:

- Số lượng sách được tăng lại.
- Trạng thái mượn được cập nhật.
- Thông tin trả sách được lưu vào lịch sử.
- Sách được đưa vào Stack lịch sử trả.

---

# 4. Các cấu trúc dữ liệu

## 4.1. Queue – Hàng đợi

Queue được sử dụng để quản lý **hàng đợi mượn sách**.

Queue hoạt động theo nguyên tắc:

**FIFO – First In, First Out**

Tức là người vào hàng đợi trước sẽ được xử lý trước.

Các thao tác chính:

- `enqueue()` – thêm phần tử vào cuối Queue.
- `dequeue()` – lấy phần tử ở đầu Queue.
- `is_empty()` – kiểm tra Queue rỗng.
- `remove_by_borrower_id()` – xóa người mượn khỏi hàng đợi.

## 4.2. Stack – Ngăn xếp

Stack được sử dụng để quản lý **lịch sử trả sách**.

Stack hoạt động theo nguyên tắc:

**LIFO – Last In, First Out**

Tức là phần tử được thêm vào sau sẽ được lấy ra trước.

Các thao tác chính:

- `push()` – thêm phần tử vào Stack.
- `pop()` – lấy phần tử trên cùng.
- `is_empty()` – kiểm tra Stack rỗng.

## 4.3. Linked List – Danh sách liên kết

Chương trình tự xây dựng Linked List để lưu trữ danh sách sách.

Cấu trúc gồm:

```text
Node
 ├── data
 └── next
```

Các thao tác chính:

- Thêm sách.
- Xóa sách.
- Tìm kiếm sách.
- Hiển thị danh sách.

Linked List sử dụng con trỏ `next` để liên kết các Node với nhau.

## 4.4. Binary Search Tree

Binary Search Tree được sử dụng để tổ chức và tìm kiếm sách theo `book_id`.

Mỗi Node gồm:

```text
BSTNode
 ├── book
 ├── left
 └── right
```

Các chức năng:

- Thêm Node.
- Tìm kiếm sách.
- Duyệt Inorder.
- Duyệt Preorder.
- Duyệt Postorder.

Quy tắc của Binary Search Tree:

```text
           Root
          /    \
       nhỏ hơn  lớn hơn
```

Trong chương trình, `book_id` được sử dụng làm khóa để so sánh.

---

# 5. Các thuật toán sắp xếp

Project tự cài đặt 6 thuật toán sắp xếp:

| Thuật toán | Độ phức tạp trung bình |
|---|---:|
| Bubble Sort | O(n²) |
| Selection Sort | O(n²) |
| Insertion Sort | O(n²) |
| Quick Sort | O(n log n) |
| Merge Sort | O(n log n) |
| Heap Sort | O(n log n) |

Các thuật toán có thể sắp xếp sách theo các khóa như:

- `title`
- `publish_year`
- `book_id`

Chương trình cũng thống kê:

- Thời gian thực thi.
- Số phép so sánh.
- Số phép gán.

---

# 6. Benchmark

Project có chương trình Benchmark để đánh giá hiệu năng của các thuật toán sắp xếp.

Kích thước dữ liệu được kiểm tra:

```text
25
100
500
1000
10000
```

Mỗi kích thước dữ liệu được chạy nhiều lần để lấy kết quả trung bình.

Các thông số được ghi nhận:

- Execution time (ms).
- Comparisons.
- Assignments.

Kết quả được lưu vào:

```text
data/benchmark_results.csv
```

Chương trình cũng tạo biểu đồ để trực quan hóa kết quả Benchmark.

Các file biểu đồ:

```text
data/benchmark_all_algorithms.png
data/benchmark_nlogn.png
```

---

# 7. Cấu trúc project

```text
LibraryManagement/
│
├── algorithms/
│   ├── benchmark.py
│   ├── plot_benchmark.py
│   ├── sorting.py
│   └── test_sorting.py
│
├── controllers/
│
├── data/
│   ├── books.json
│   ├── borrowers_list.json
│   ├── benchmark_results.csv
│   ├── benchmark_all_algorithms.png
│   └── benchmark_nlogn.png
│
├── data_structures/
│   ├── queue.py
│   ├── stack.py
│   ├── linked_list.py
│   └── bts.py
│
├── models/
│   └── book.py
│
├── repositories/
│   ├── book_repo.py
│   ├── borrower_repo.py
│   └── ...
│
├── services/
│   └── library_service.py
│
├── views/
│   ├── book_view.py
│   ├── borrow_view.py
│   ├── return_view.py
│   ├── sort_view.py
│   ├── search_view.py
│   ├── bst_view.py
│   └── linked_list_view.py
│
└── main.py
```

---

# 8. Công nghệ sử dụng

- **Python 3**
- **Rich** – xây dựng giao diện Console.
- **JSON** – lưu trữ dữ liệu.
- **CSV** – lưu kết quả Benchmark.
- **Matplotlib** – tạo biểu đồ Benchmark.
- **Git / GitHub** – quản lý mã nguồn.

---

# 9. Lưu trữ dữ liệu

Dữ liệu được lưu dưới dạng JSON.

Ví dụ thông tin sách:

```json
{
    "book_id": "S001",
    "title": "Lập trình Python",
    "author": "Nguyễn Văn A",
    "publish_year": 2024,
    "quantity": 6,
    "category": "",
    "isbn": ""
}
```

Việc tách phần lưu trữ thành Repository giúp chương trình dễ dàng thay đổi cách lưu dữ liệu trong tương lai.

---

# 10. Kiến trúc chương trình

Chương trình được chia thành nhiều thành phần:

```text
View
  ↓
Service
  ↓
Repository
  ↓
JSON Data
```

Trong đó:

- **View**: giao diện tương tác với người dùng.
- **Service**: xử lý nghiệp vụ.
- **Repository**: đọc và ghi dữ liệu.
- **Model**: mô tả đối tượng dữ liệu.
- **Data Structures**: cài đặt Queue, Stack, Linked List, BST.
- **Algorithms**: cài đặt các thuật toán sắp xếp và Benchmark.

---

# 11. Cách chạy chương trình

### Bước 1: Clone project

```bash
git clone https://github.com/dinhanh1991/library_managerment.git
```

### Bước 2: Di chuyển vào thư mục project

```bash
cd library_managerment/LibraryManagement
```

### Bước 3: Cài đặt thư viện cần thiết

```bash
pip install rich matplotlib
```

### Bước 4: Chạy chương trình

```bash
python main.py
```

---

# 12. Chạy Benchmark

Để kiểm tra hiệu năng các thuật toán sắp xếp:

```bash
python algorithms/benchmark.py
```

Kết quả Benchmark được lưu vào:

```text
data/benchmark_results.csv
```

Sau đó có thể chạy chương trình tạo biểu đồ:

```bash
python algorithms/plot_benchmark.py
```

---

# 13. Độ phức tạp thuật toán

### Bubble Sort

```text
Best:    O(n)
Average: O(n²)
Worst:   O(n²)
Space:   O(1)
```

### Selection Sort

```text
Best:    O(n²)
Average: O(n²)
Worst:   O(n²)
Space:   O(1)
```

### Insertion Sort

```text
Best:    O(n)
Average: O(n²)
Worst:   O(n²)
Space:   O(1)
```

### Quick Sort

```text
Best:    O(n log n)
Average: O(n log n)
Worst:   O(n²)
```

### Merge Sort

```text
Best:    O(n log n)
Average: O(n log n)
Worst:   O(n log n)
Space:   O(n)
```

### Heap Sort

```text
Best:    O(n log n)
Average: O(n log n)
Worst:   O(n log n)
Space:   O(1)
```

---

# 14. Mục tiêu học tập

Project được thực hiện nhằm áp dụng kiến thức môn **Cấu trúc dữ liệu và Giải thuật** vào một bài toán thực tế.

Thông qua project, người thực hiện thực hành:

- Quản lý dữ liệu bằng Python.
- Xây dựng các cấu trúc dữ liệu cơ bản.
- Cài đặt thuật toán sắp xếp.
- Phân tích độ phức tạp thuật toán.
- Đo và so sánh hiệu năng thực tế.
- Tổ chức mã nguồn thành các module.
- Sử dụng Git và GitHub để quản lý source code.

---

# 15. Tác giả

**Lê Đình Anh**

Project học tập môn **Cấu trúc dữ liệu và Giải thuật**.
