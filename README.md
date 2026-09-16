# 📚 Library Management

Ứng dụng quản lý thư viện chạy trên **Console**, được phát triển bằng **Python** để thực hành **Cấu trúc dữ liệu và Giải thuật** trong một chương trình thực tế.

## 1. Chức năng chính

### Quản lý sách
- Thêm, xóa và cập nhật sách.
- Hiển thị danh sách sách và tình trạng `Có sẵn` / `Hết`.
- Tìm kiếm theo tên sách hoặc tác giả.
- Tìm kiếm nâng cao theo tên, tác giả, thể loại, năm xuất bản, ISBN và tình trạng.

Thông tin sách gồm:

```text
book_id | title | author | publish_year | quantity | category | isbn
```

### Quản lý độc giả
- Thêm, cập nhật và xóa độc giả.
- Không cho xóa độc giả đang có giao dịch mượn.
- Xem lịch sử giao dịch.
- Xem các lượt mượn quá hạn.

### Mượn và trả sách
- Kiểm tra sách còn số lượng trước khi mượn.
- Mỗi lượt mượn có thời hạn 14 ngày.
- Lượt mượn mới được đưa vào Queue với trạng thái `pending`.
- Xử lý người tiếp theo trong Queue chuyển trạng thái sang `borrowed`.
- Không cho độc giả đang có lượt mượn quá hạn tạo lượt mượn mới.
- Khi trả sách, số lượng được hoàn lại, giao dịch được chuyển sang `returned` và lưu vào lịch sử.

## 2. Cấu trúc dữ liệu

Project tự cài đặt các cấu trúc dữ liệu cơ bản:

| Cấu trúc | Mục đích | Nguyên tắc |
|---|---|---|
| Queue | Quản lý hàng đợi mượn sách | FIFO |
| Stack | Lưu lịch sử trả sách | LIFO |
| Linked List | Lưu và tìm kiếm danh sách sách | Danh sách liên kết đơn |
| Binary Search Tree | Tổ chức sách theo `book_id` | BST |

Các module tương ứng nằm trong `LibraryManagement/data_structures/`.

## 3. Thuật toán sắp xếp

File `algorithms/sorting.py` cài đặt 6 thuật toán:

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Quick Sort
5. Merge Sort
6. Heap Sort

Các thuật toán hỗ trợ sắp xếp theo:

- `title`
- `publish_year`
- `book_id`

Mỗi thuật toán trả về:

```text
(sorted_books, comparisons, assignments)
```

### Độ phức tạp lý thuyết

| Thuật toán | Best | Average | Worst |
|---|---:|---:|---:|
| Bubble Sort | O(n²) | O(n²) | O(n²) |
| Selection Sort | O(n²) | O(n²) | O(n²) |
| Insertion Sort | O(n) | O(n²) | O(n²) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) |

> Lưu ý: implementation Bubble Sort hiện tại không có bước dừng sớm, nên trường hợp tốt nhất thực tế vẫn là O(n²).

## 4. Benchmark

`algorithms/benchmark.py` dùng để so sánh hiệu năng của 6 thuật toán.

Các kích thước dữ liệu hiện tại:

```text
25, 100, 500, 1000, 10000
```

Mỗi kích thước chạy **5 lần** trên dữ liệu đã được xáo trộn và lấy giá trị trung bình.

Benchmark ghi nhận:

- Thời gian chạy trung bình (ms).
- Số phép so sánh.
- Số phép gán.

Kết quả được lưu tại:

```text
data/benchmark_results.csv
```

`algorithms/plot_benchmark.py` tạo:

```text
data/benchmark_all_algorithms.png
data/benchmark_nlogn.png
```

## 5. Kiểm thử

Project hiện có bộ test trong `LibraryManagement/tests/`, gồm:

```text
tests/
├── test_book_view.py
├── test_borrow_business_rules.py
├── test_borrow_queue_consistency.py
├── test_data_structures.py
├── test_library_service.py
├── test_reader_business_rules.py
├── test_return_book_borrowed.py
├── test_search_business_rules.py
├── test_sorting_business_rules.py
├── test_ui_and_input.py
└── test_update_book_borrowing.py
```

Các nhóm test bao phủ:

- Book CRUD và hiển thị tình trạng sách.
- Quy tắc mượn sách.
- Queue và tính nhất quán khi xử lý hàng đợi.
- Queue, Stack, Linked List và Binary Search Tree.
- Return và đồng bộ lịch sử trả.
- Reader CRUD, lịch sử và quá hạn.
- Tìm kiếm nâng cao.
- 6 thuật toán sắp xếp.
- Input và các luồng UI chính.
- Chặn cập nhật/xóa sách khi có giao dịch đang hoạt động.

Chạy toàn bộ test bằng:

```bash
python -m unittest discover -s tests -v
```

## 6. Cấu trúc project

```text
LibraryManagement/
├── algorithms/
│   ├── sorting.py
│   ├── benchmark.py
│   ├── plot_benchmark.py
│   └── test_sorting.py
│
├── controllers/
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
│   └── benchmark images
│
├── data_structures/
│   ├── queue.py
│   ├── stack.py
│   ├── linked_list.py
│   └── bts.py
│
├── models/
├── repositories/
├── services/
│   └── library_service.py
├── utils/
├── views/
├── tests/
├── .gitignore
├── __init__.py
└── main.py
```

## 7. Kiến trúc chương trình

```text
Người dùng
    ↓
main.py
    ↓
LibraryController
    ↓
Views / Controllers
    ↓
LibraryService
    ↓
Models + Data Structures + Repositories
    ↓
JSON / CSV / biểu đồ
```

- **Models**: biểu diễn dữ liệu.
- **Views**: giao diện Console và nhập/xuất.
- **Controllers**: điều phối thao tác người dùng.
- **Service**: xử lý nghiệp vụ trung tâm.
- **Repositories**: đọc/ghi dữ liệu JSON.
- **Data Structures**: cài đặt Queue, Stack, Linked List và BST.
- **Algorithms**: sắp xếp và benchmark.

## 8. Công nghệ

- Python 3
- Rich
- Matplotlib
- JSON
- CSV
- Git / GitHub

## 9. Cài đặt và chạy

Clone repository:

```bash
git clone https://github.com/dinhanh1991/library_managerment.git
```

Di chuyển vào thư mục chương trình:

```bash
cd library_managerment/LibraryManagement
```

Cài thư viện:

```bash
pip install rich matplotlib
```

Chạy chương trình:

```bash
python main.py
```

## 10. Chạy benchmark

```bash
python algorithms/benchmark.py
```

Tạo biểu đồ:

```bash
python algorithms/plot_benchmark.py
```

## 11. Mục tiêu học tập

Project được xây dựng nhằm thực hành:

- Thiết kế chương trình Python theo module.
- Áp dụng Queue, Stack, Linked List và Binary Search Tree.
- Cài đặt và so sánh 6 thuật toán sắp xếp.
- Đếm phép so sánh và phép gán.
- Đo hiệu năng trên nhiều kích thước dữ liệu.
- Thiết kế tầng Repository và Service.
- Viết kiểm thử cho các nghiệp vụ chính.
- Quản lý source code bằng Git/GitHub.

## 12. Tác giả

**Lê Đình Anh**

Project học tập môn **Cấu trúc dữ liệu và Giải thuật**.
