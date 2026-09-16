# 📚 Library Management

## 1. Giới thiệu

**Library Management** là chương trình quản lý thư viện chạy trên **Console**, được phát triển bằng **Python** để áp dụng kiến thức môn **Cấu trúc dữ liệu và Giải thuật** vào một chương trình thực tế.

Chương trình hiện có các nhóm chức năng chính: quản lý sách, quản lý độc giả, mượn/trả sách, tìm kiếm, sử dụng Queue/Stack/Linked List/Binary Search Tree, sắp xếp sách bằng nhiều thuật toán và đo hiệu năng các thuật toán sắp xếp.

Dữ liệu nghiệp vụ được lưu bằng các file **JSON**; kết quả benchmark được lưu bằng **CSV** và biểu đồ được tạo bằng **Matplotlib**.

---

## 2. Chức năng thực tế của chương trình

### 2.1. Quản lý sách

Chương trình hỗ trợ:

- Thêm sách.
- Xóa sách theo mã sách.
- Cập nhật thông tin sách.
- Hiển thị danh sách sách.
- Tìm kiếm theo tên sách.
- Tìm kiếm theo tác giả.
- Tìm kiếm nâng cao theo nhiều điều kiện.

Thông tin `Book` hiện gồm:

- `book_id`: mã sách.
- `title`: tên sách.
- `author`: tác giả.
- `publish_year`: năm xuất bản.
- `quantity`: số lượng.
- `category`: thể loại.
- `isbn`: mã ISBN.

Model `Book` có `to_dict()` để chuyển đối tượng thành dữ liệu JSON và `from_dict()` để tạo lại đối tượng từ dữ liệu đọc được. fileciteturn42file0L2-L6

### 2.2. Tìm kiếm nâng cao

Tìm kiếm nâng cao có thể kết hợp các điều kiện:

- Tên sách.
- Tác giả.
- Thể loại.
- Năm xuất bản.
- ISBN.
- Tình trạng còn sách / hết sách.

### 2.3. Quản lý độc giả

Chương trình có các chức năng:

- Thêm độc giả.
- Cập nhật độc giả.
- Xóa độc giả.
- Hiển thị danh sách độc giả.
- Xem lịch sử giao dịch của độc giả.
- Xem danh sách độc giả quá hạn.

Khi cập nhật độc giả, tên độc giả trong các lượt mượn đang hoạt động và trong hàng đợi cũng được cập nhật theo.

### 2.4. Mượn sách

Quy trình mượn sách gồm kiểm tra lượt mượn đang hoạt động, kiểm tra số lượng sách và cập nhật thông tin mượn.

Mỗi lượt mượn có thời hạn **14 ngày**. Lượt mượn mới được đưa vào **Queue** với trạng thái `pending`; khi xử lý người tiếp theo trong hàng đợi, trạng thái được chuyển sang `borrowed`. Số lượng sách được giảm sau khi tạo lượt mượn. fileciteturn33file0L2-L3

Chương trình cũng kiểm tra trường hợp độc giả đang có sách quá hạn và không cho tạo lượt mượn mới trong trường hợp đó.

### 2.5. Trả sách

Khi trả sách:

- Số lượng sách được tăng lại.
- Lượt mượn được chuyển sang trạng thái `returned`.
- Ngày trả được ghi nhận.
- Giao dịch được đưa vào **Stack** và lưu vào lịch sử trả.
- Lượt mượn đang hoạt động được loại khỏi danh sách mượn.
- Người mượn được loại khỏi Queue nếu còn trong hàng đợi.

### 2.6. Cấu trúc dữ liệu được sử dụng

Chương trình không chỉ dùng cấu trúc dữ liệu có sẵn của Python mà có các module riêng để cài đặt:

- Queue.
- Stack.
- Linked List.
- Binary Search Tree.

`LibraryService` khởi tạo và sử dụng cả bốn cấu trúc này trong quá trình quản lý thư viện. fileciteturn33file0L2-L3

---

## 3. Các cấu trúc dữ liệu

### Queue

`data_structures/queue.py` cài đặt hàng đợi cho các lượt mượn sách.

Các thao tác chính:

- `enqueue()` – thêm vào cuối hàng đợi.
- `dequeue()` – lấy phần tử đầu hàng đợi.
- `is_empty()` – kiểm tra rỗng.
- `remove_by_borrower_id()` – loại lượt mượn của độc giả khỏi hàng đợi.

Queue được sử dụng theo nguyên tắc **FIFO (First In, First Out)**.

### Stack

`data_structures/stack.py` cài đặt Stack cho lịch sử trả sách.

Các thao tác chính:

- `push()` – thêm phần tử lên đỉnh Stack.
- `pop()` – lấy phần tử trên cùng.
- `is_empty()` – kiểm tra rỗng.

Stack hoạt động theo nguyên tắc **LIFO (Last In, First Out)**.

### Linked List

`data_structures/linked_list.py` cài đặt danh sách liên kết đơn với `Node` gồm dữ liệu và liên kết tới node tiếp theo.

Linked List được xây dựng từ dữ liệu sách và hỗ trợ thêm, xóa, hiển thị và tìm kiếm sách.

### Binary Search Tree

`data_structures/bts.py` cài đặt Binary Search Tree để tổ chức sách theo `book_id`.

Chương trình có các thao tác:

- Insert.
- Search.
- Inorder.
- Preorder.
- Postorder.

`LibraryService` có các chức năng xây dựng lại BST từ dữ liệu sách, tìm kiếm sách bằng BST và hiển thị Preorder/Postorder. fileciteturn33file0L2-L3

---

## 4. Các thuật toán sắp xếp

File `algorithms/sorting.py` hiện cài đặt **6 thuật toán**:

1. Bubble Sort.
2. Selection Sort.
3. Insertion Sort.
4. Quick Sort.
5. Merge Sort.
6. Heap Sort.

Các thuật toán hỗ trợ khóa sắp xếp:

- `title` – tên sách.
- `publish_year` – năm xuất bản.
- `book_id` – mã sách, được dùng mặc định.

Mỗi hàm sắp xếp trả về:

```text
(danh sách sau sắp xếp, comparisons, assignments)
```

Trong đó `comparisons` là số phép so sánh và `assignments` là số phép gán được chương trình đếm trong quá trình chạy. fileciteturn34file0L2-L2

### Độ phức tạp lý thuyết

| Thuật toán | Best | Average | Worst |
|---|---:|---:|---:|
| Bubble Sort | O(n²) | O(n²) | O(n²) |
| Selection Sort | O(n²) | O(n²) | O(n²) |
| Insertion Sort | O(n) | O(n²) | O(n²) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) |

Lưu ý: Bubble Sort trong mã hiện tại không có bước dừng sớm khi danh sách đã được sắp xếp, vì vậy trường hợp tốt nhất của implementation hiện tại vẫn là **O(n²)**.

---

## 5. Benchmark

Project có `algorithms/benchmark.py` để đo hiệu năng thực tế của 6 thuật toán sắp xếp.

Benchmark hiện chạy với các kích thước:

```text
25
100
500
1000
10000
```

Mỗi kích thước được chạy **5 lần** trên cùng bộ dữ liệu đầu vào đã được xáo trộn, sau đó lấy giá trị trung bình. Tiêu chí sắp xếp của benchmark hiện tại là **tên sách (`title`)**. fileciteturn37file0L2-L6

Các thông số được ghi nhận:

- Thời gian thực thi trung bình (ms).
- Số phép so sánh trung bình.
- Số phép gán trung bình.

Kết quả được lưu tại:

```text
data/benchmark_results.csv
```

`algorithms/plot_benchmark.py` đọc CSV và tạo hai biểu đồ:

```text
data/benchmark_all_algorithms.png
data/benchmark_nlogn.png
```

Biểu đồ thứ hai dùng để so sánh nhóm Heap Sort, Quick Sort và Merge Sort. fileciteturn38file0L2-L6

Ngoài benchmark, `algorithms/test_sorting.py` chứa các lần chạy thử trực tiếp 6 thuật toán trên một tập sách mẫu, trong đó có kiểm tra sắp xếp theo tên và năm xuất bản. fileciteturn49file0L2-L6

---

## 6. Kiểm thử chương trình

Thư mục `tests/` hiện có:

```text
tests/
└── test_library_service.py
```

File test kiểm tra nhiều nghiệp vụ của `LibraryService`, gồm quản lý sách, tìm kiếm nâng cao, mượn/trả sách, cập nhật số lượng, Queue FIFO và lưu Queue, ngăn mượn trùng, CRUD độc giả, không cho xóa độc giả đang mượn, lịch sử độc giả, danh sách quá hạn và thống kê Dashboard.

Ngoài ra, các file `__pycache__` xuất hiện trong repository là dữ liệu cache được Python tạo ra khi chạy chương trình, không phải thành phần nghiệp vụ của hệ thống.

---

## 7. Cấu trúc project thực tế

```text
LibraryManagement/
│
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py
│   ├── benchmark.py
│   ├── plot_benchmark.py
│   └── test_sorting.py
│
├── controllers/
│   ├── __init__.py
│   ├── library_controller.py
│   ├── book_controller.py
│   ├── borrow_controller.py
│   └── reader_controller.py
│
├── data/
│   ├── books.json
│   ├── borrowers_list.json
│   ├── borrow_queue.json
│   ├── readers.json
│   ├── return_history.json
│   ├── benchmark_results.csv
│   ├── benchmark_all_algorithms.png
│   └── benchmark_nlogn.png
│
├── data_structures/
│   ├── __init__.py
│   ├── queue.py
│   ├── stack.py
│   ├── linked_list.py
│   └── bts.py
│
├── models/
│   ├── book.py
│   ├── borrower.py
│   └── reader.py
│
├── repositories/
│   ├── __init__.py
│   ├── book_repo.py
│   ├── borrower_repo.py
│   ├── queue_repo.py
│   ├── reader_repo.py
│   └── return_history_repo.py
│
├── services/
│   └── library_service.py
│
├── utils/
│   ├── ui_helpers.py
│   └── logging_config.py
│
├── views/
│   ├── base_view.py
│   ├── library_view.py
│   ├── book_view.py
│   ├── borrow_view.py
│   ├── return_view.py
│   ├── search_view.py
│   ├── sort_view.py
│   ├── bst_view.py
│   ├── linked_list_view.py
│   └── reader_view.py
│
├── tests/
│   └── test_library_service.py
│
├── .vscode/
├── __init__.py
└── main.py
```

Các thư mục `controllers`, `utils` và `tests` là những thành phần có thật trong project hiện tại, không phải thư mục dự kiến. Cấu trúc trên được lập lại theo source hiện có trong repository. fileciteturn35file0L2-L10 fileciteturn41file0L2-L10 fileciteturn46file0L2-L10

---

## 8. Mô tả từng tầng và file chính

### `main.py`

Điểm khởi động của chương trình. File này tạo `LibraryController` và gọi `controller.run()`. Phần điều phối menu không đặt trực tiếp trong `main.py`. fileciteturn43file0L2-L6

### `controllers/`

Tầng Controller điều phối luồng thao tác của người dùng.

- `library_controller.py`: Controller cấp cao; tạo Service/View và kết nối các controller chức năng. Menu chính ánh xạ tới quản lý sách, mượn, trả, tìm kiếm, BST, Linked List, sắp xếp và quản lý độc giả. fileciteturn47file0L2-L6
- `book_controller.py`: điều phối các thao tác quản lý sách.
- `borrow_controller.py`: điều phối quy trình mượn và xử lý người tiếp theo trong Queue.
- `reader_controller.py`: điều phối các thao tác quản lý độc giả, lịch sử và quá hạn. fileciteturn48file0L2-L6

### `services/`

- `library_service.py`: lớp nghiệp vụ trung tâm. File này xử lý sách, độc giả, mượn/trả, quá hạn, tìm kiếm, Queue, Stack, Linked List và BST; đồng thời kết nối các Repository để đọc/ghi dữ liệu. fileciteturn33file0L2-L3

### `models/`

Chứa các lớp biểu diễn dữ liệu:

- `book.py`: đối tượng sách.
- `borrower.py`: đối tượng lượt mượn.
- `reader.py`: đối tượng độc giả.

### `repositories/`

Tầng Repository chịu trách nhiệm đọc/ghi dữ liệu của từng nhóm nghiệp vụ:

- `book_repo.py`: dữ liệu sách.
- `borrower_repo.py`: các lượt mượn đang được lưu.
- `queue_repo.py`: dữ liệu hàng đợi mượn.
- `reader_repo.py`: dữ liệu độc giả.
- `return_history_repo.py`: lịch sử trả sách.

Các Repository hiện lưu dữ liệu vào các file JSON trong `data/`. Danh sách file Repository hiện có được xác nhận trực tiếp từ source repository. fileciteturn39file0L2-L10

### `views/`

Tầng View xử lý giao diện Console và tương tác nhập/xuất với người dùng. Các View hiện có gồm View cơ sở, View thư viện, sách, mượn, trả, tìm kiếm, sắp xếp, BST, Linked List và độc giả.

### `utils/`

- `ui_helpers.py`: các hàm hỗ trợ giao diện và nhập liệu dùng chung, bao gồm xử lý input, kiểm tra số nguyên, hiển thị bảng sách và thông báo.
- `logging_config.py`: cấu hình logger dùng chung cho chương trình.

### `data_structures/`

Chứa phần cài đặt trực tiếp các cấu trúc dữ liệu Queue, Stack, Linked List và Binary Search Tree. Danh sách file thực tế của thư mục gồm `queue.py`, `stack.py`, `linked_list.py` và `bts.py`. fileciteturn36file0L2-L10

### `algorithms/`

Chứa thuật toán sắp xếp, chương trình benchmark, chương trình tạo biểu đồ và file chạy thử các thuật toán. Các file thực tế gồm `sorting.py`, `benchmark.py`, `plot_benchmark.py` và `test_sorting.py`. fileciteturn45file0L2-L10

### `tests/`

Chứa kiểm thử nghiệp vụ của `LibraryService`, hiện có `test_library_service.py`. fileciteturn46file0L2-L10

### `data/`

Chứa dữ liệu chạy chương trình và kết quả benchmark. Hiện có dữ liệu sách, độc giả, lượt mượn, Queue, lịch sử trả sách, CSV benchmark và hai file ảnh biểu đồ. fileciteturn40file0L2-L10

---

## 9. Luồng xử lý tổng quát

```text
Người dùng
    ↓
main.py
    ↓
LibraryController
    ↓
┌──────────────────────────────────────────────┐
│ BookController                               │
│ BorrowController                             │
│ ReaderController                              │
│ Các View chức năng khác                      │
└──────────────────────────────────────────────┘
    ↓
LibraryService
    ↓
┌──────────────────────────────────────────────┐
│ Models                                       │
│ Data Structures                              │
│ Repositories                                 │
└──────────────────────────────────────────────┘
    ↓
JSON / CSV / biểu đồ trong data/
```

Đây là cách tổ chức thực tế của source hiện tại: `main.py` khởi động `LibraryController`; Controller sử dụng `LibraryService` và các View; Service sử dụng các cấu trúc dữ liệu và Repository để xử lý nghiệp vụ và dữ liệu. fileciteturn43file0L2-L6 fileciteturn47file0L2-L6 fileciteturn33file0L2-L3

---

## 10. Công nghệ sử dụng

- **Python 3**
- **Rich** – giao diện Console và bảng dữ liệu.
- **JSON** – lưu dữ liệu nghiệp vụ.
- **CSV** – lưu kết quả benchmark.
- **Matplotlib** – tạo biểu đồ benchmark.
- **Git / GitHub** – quản lý mã nguồn.

---

## 11. Cài đặt và chạy chương trình

Clone repository:

```bash
git clone https://github.com/dinhanh1991/library_managerment.git
```

Di chuyển vào thư mục project:

```bash
cd library_managerment/LibraryManagement
```

Cài thư viện sử dụng cho giao diện và benchmark:

```bash
pip install rich matplotlib
```

Chạy chương trình:

```bash
python main.py
```

---

## 12. Chạy Benchmark

Chạy benchmark:

```bash
python algorithms/benchmark.py
```

Sau khi chạy, kết quả được ghi vào:

```text
data/benchmark_results.csv
```

Tạo biểu đồ từ kết quả benchmark:

```bash
python algorithms/plot_benchmark.py
```

---

## 13. Mục tiêu của project

Project được phát triển để áp dụng kiến thức **Cấu trúc dữ liệu và Giải thuật** vào một bài toán quản lý cụ thể.

Các nội dung chính được thực hành trong chương trình:

- Thiết kế chương trình thành nhiều module.
- Quản lý dữ liệu sách và độc giả.
- Cài đặt Queue, Stack, Linked List và Binary Search Tree.
- Cài đặt 6 thuật toán sắp xếp.
- Đếm phép so sánh và phép gán trong thuật toán.
- Đo thời gian chạy với nhiều kích thước dữ liệu.
- Lưu và phân tích kết quả benchmark.
- Viết kiểm thử cho các nghiệp vụ chính.
- Quản lý source code bằng Git/GitHub.

---

## 14. Tác giả

**Lê Đình Anh**

Project học tập môn **Cấu trúc dữ liệu và Giải thuật**.
