# 📚 Library Management

Ứng dụng **quản lý thư viện trên Console**, được xây dựng bằng **Python** nhằm thực hành **Cấu trúc dữ liệu và Giải thuật** trong một chương trình thực tế.

Project được tổ chức theo hướng module, tách phần giao diện, điều phối, nghiệp vụ, lưu trữ dữ liệu, cấu trúc dữ liệu và thuật toán để dễ học, kiểm thử và mở rộng.

---

## 1. Mục tiêu project

Project tập trung vào các nội dung:

- Quản lý sách và độc giả.
- Quản lý quy trình mượn/trả sách.
- Thực hành Queue, Stack, Linked List và Binary Search Tree.
- Cài đặt nhiều thuật toán sắp xếp và so sánh hiệu năng.
- Tách nghiệp vụ khỏi giao diện Console.
- Lưu dữ liệu bằng JSON và kết quả benchmark bằng CSV.
- Viết unit test cho nghiệp vụ, cấu trúc dữ liệu, repository và UI.
- Thực hành Git/GitHub và GitHub Actions.

---

## 2. Chức năng chính

### 📖 Quản lý sách

- Thêm sách.
- Cập nhật sách.
- Xóa sách.
- Hiển thị danh sách sách.
- Hiển thị trạng thái `Có sẵn` / `Hết`.
- Tìm kiếm theo tên sách hoặc tác giả.
- Tìm kiếm nâng cao theo nhiều tiêu chí.
- Kiểm tra dữ liệu đầu vào của sách.
- Không cho cập nhật/xóa sách khi còn giao dịch mượn đang hoạt động theo các quy tắc nghiệp vụ của project.

Thông tin sách hiện gồm:

```text
book_id | title | author | publish_year | quantity | category | isbn
```

### 👤 Quản lý độc giả

- Thêm độc giả.
- Cập nhật độc giả.
- Xóa độc giả.
- Xem lịch sử giao dịch.
- Kiểm tra các lượt mượn quá hạn.
- Áp dụng các quy tắc nghiệp vụ khi xóa/cập nhật độc giả.

### 📚 Mượn sách

- Kiểm tra số lượng sách trước khi mượn.
- Tạo lượt mượn mới với thời hạn mặc định 14 ngày.
- Lượt mượn mới được quản lý qua Queue với trạng thái `pending`.
- Xử lý người tiếp theo trong Queue theo nguyên tắc FIFO.
- Chuyển giao dịch sang trạng thái `borrowed` khi được xử lý.
- Không cho độc giả đang có lượt mượn quá hạn tạo lượt mượn mới.

### ↩️ Trả sách

- Kiểm tra giao dịch đang mượn.
- Hoàn lại số lượng sách.
- Chuyển giao dịch sang `returned`.
- Lưu lịch sử trả sách.
- Sử dụng Stack cho phần lịch sử trả theo nguyên tắc LIFO.

### 🔎 Tìm kiếm

Hỗ trợ tìm kiếm nâng cao theo các thông tin như:

- Tên sách.
- Tác giả.
- Thể loại.
- Năm xuất bản.
- ISBN.
- Tình trạng sách.

### 📊 Báo cáo và thống kê

Project có `ReportService` và `ReportView` riêng cho phần báo cáo.

Các báo cáo gồm:

- Tổng quan thư viện.
- Thống kê sách.
- Thống kê mượn/trả.
- Thống kê theo thể loại.
- Danh sách quá hạn.
- Top sách được mượn nhiều.
- Top độc giả hoạt động nhiều.
- Thống kê hoạt động trong một khoảng thời gian.

Dashboard chính cũng lấy dữ liệu thống kê từ `ReportService`, giúp tách phần **tính toán dữ liệu** khỏi phần **hiển thị Console**.

---

## 3. Cấu trúc dữ liệu

Project tự cài đặt các cấu trúc dữ liệu cơ bản:

| Cấu trúc | Mục đích | Nguyên tắc |
|---|---|---|
| Queue | Quản lý hàng đợi mượn sách | FIFO |
| Stack | Quản lý lịch sử trả sách | LIFO |
| Linked List | Lưu và thao tác danh sách sách | Danh sách liên kết đơn |
| Binary Search Tree | Tổ chức/tìm kiếm theo `book_id` | BST |

Các implementation nằm trong:

```text
LibraryManagement/data_structures/
```

---

## 4. Thuật toán sắp xếp

File `algorithms/sorting.py` cài đặt 6 thuật toán:

1. Bubble Sort
2. Selection Sort
3. Insertion Sort
4. Quick Sort
5. Merge Sort
6. Heap Sort

Các thuật toán hỗ trợ sắp xếp theo các key như:

- `title`
- `publish_year`
- `book_id`

Kết quả thuật toán bao gồm danh sách sau khi sắp xếp cùng số phép so sánh và phép gán:

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

> **Lưu ý:** Bubble Sort hiện tại không có bước dừng sớm, vì vậy trường hợp tốt nhất của implementation này vẫn là O(n²).

### Strategy Pattern

Phần chọn thuật toán sắp xếp được tách qua `sort_strategy.py`. Mục đích là để có thể thay đổi thuật toán mà không phải sửa phần code điều phối chính.

---

## 5. Benchmark và biểu đồ

`algorithms/benchmark.py` dùng để so sánh hiệu năng của 6 thuật toán.

Các kích thước dữ liệu benchmark hiện tại:

```text
25, 100, 500, 1000, 10000
```

Mỗi kích thước được chạy **5 lần** trên dữ liệu đã xáo trộn và lấy kết quả trung bình.

Benchmark ghi nhận:

- Thời gian chạy trung bình (ms).
- Số phép so sánh.
- Số phép gán.

Kết quả được lưu tại:

```text
data/benchmark_results.csv
```

Sau đó `algorithms/plot_benchmark.py` tạo các biểu đồ:

```text
data/benchmark_all_algorithms.png
data/benchmark_nlogn.png
```

---

## 6. Kiến trúc chương trình

Luồng xử lý tổng quát:

```text
Người dùng
    ↓
main.py
    ↓
LibraryController
    ↓
Views / Controllers chức năng
    ↓
LibraryService (Facade)
    ↓
Domain Services
    ↓
Repositories + Data Structures
    ↓
JSON / CSV
```

### Các tầng chính

**Models**

- Biểu diễn dữ liệu như sách, độc giả và giao dịch mượn/trả.

**Views**

- Hiển thị menu.
- Nhận input từ người dùng.
- Hiển thị bảng, panel và thông báo bằng Rich.

**Controllers**

- Điều phối luồng xử lý từ menu.
- Tách việc điều phối khỏi phần hiển thị.

**Services**

- Chứa nghiệp vụ của hệ thống.
- `LibraryService` đóng vai trò Facade cho các nghiệp vụ chính.
- Các service chuyên trách gồm sách, mượn, trả, độc giả và báo cáo.

**Repositories**

- Đọc/ghi dữ liệu JSON.
- Tách tầng lưu trữ khỏi nghiệp vụ.

**Data Structures**

- Queue.
- Stack.
- Linked List.
- Binary Search Tree.

**Algorithms**

- Sorting.
- Strategy cho lựa chọn thuật toán.
- Benchmark.
- Plot benchmark.

---

## 7. Điểm cần cải thiện hiện tại và kế hoạch refactor

Dù project đã có cấu trúc module rõ ràng và test khá đầy đủ, vẫn còn 2 điểm cần tiếp tục cải thiện để dự án dễ mở rộng hơn trong tương lai:

### 7.1. `LibraryService` đang khá "nặng" và stateful

Trong `services/library_service.py`, `LibraryService` vừa đóng vai trò Facade, vừa chịu trách nhiệm đồng bộ trạng thái qua nhiều property setter như:

- `repository`
- `borrower_repo`
- `queue_repo`
- `reader_repo`
- `return_history_repo`
- `borrow_queue`
- `return_stack`
- `book_linked_list`
- `book_bst`

Những setter này cập nhật dữ liệu thủ công cho `state` và các service con (`book_service`, `borrow_service`, `return_service`, ...). Điểm này không sai về mặt kỹ thuật, nhưng trong dài hạn dễ dẫn đến:

- phụ thuộc chặt chẽ giữa các thành phần;
- rủi ro khi thêm service mới hoặc thay đổi state;
- khó debug khi một thuộc tính không được đồng bộ đúng;
- khó test vì trạng thái được chia rải giữa nhiều object.

### Kế hoạch cải thiện

- Giảm bớt việc đồng bộ state bằng setter thủ công.
- Chuyển `LibraryService` về dạng Facade thuần hơn, chỉ điều phối và không giữ quá nhiều state.
- Tách trạng thái chung sang `LibraryState` hoặc một `AppContext` rõ ràng hơn.
- Cho mọi service phụ thuộc vào cùng một nguồn dữ liệu / state nhất quán, thay vì tự cập nhật lặp lại.

### 7.2. Thiếu cấu trúc chuẩn hóa cho validation

Hiện tại, nhiều phần đang validate dữ liệu riêng lẻ ở các nơi khác nhau, ví dụ:

- `Book` model kiểm tra dữ liệu nhập vào.
- `BookService` kiểm tra `book_id`, `title`, `quantity`, `publish_year`.
- Một số view hoặc controller cũng có validation bổ sung.

Kết quả là:

- logic validation bị lặp lại;
- khó bảo trì khi thay đổi rule nghiệp vụ;
- dễ xảy ra inconsistencies giữa model, service và UI.

### Kế hoạch cải thiện

- Tạo một layer validation riêng, ví dụ: `utils/validators.py` hoặc `validators/`.
- Gom các rule chung vào các hàm như:
  - `is_non_empty_text(value)`
  - `is_valid_int(value, min_value=0)`
  - `is_valid_book_id(value)`
  - `is_valid_publish_year(value)`
- Model, service và view nên gọi vào cùng một validator thay vì check bằng logic riêng lẻ.
- Duy trì validation ở 2 mức:
  - validation cơ bản (type / format / required)
  - validation nghiệp vụ (ví dụ: không cho mượn khi sách hết, không cho xóa sách đang có giao dịch đang hoạt động)

Mục tiêu của các cải tiến trên là làm project **dễ mở rộng, dễ test và ít lỗi khi phát triển**, thay vì chỉ làm đúng ở thời điểm hiện tại.

---

## 8. Cấu trúc project

Cấu trúc dưới đây được cập nhật theo **source code thực tế hiện tại trên branch `main`**, bao gồm đầy đủ các file chính trong `models/` và `repositories/`.

```text
library_managerment/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── LibraryManagement/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── sorting.py
│   │   ├── sort_strategy.py
│   │   ├── benchmark.py
│   │   ├── plot_benchmark.py
│   │   └── test_sorting.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── library_controller.py
│   │   ├── book_controller.py
│   │   ├── borrow_controller.py
│   │   └── reader_controller.py
│   │
│   ├── data/
│   │   ├── books.json
│   │   ├── readers.json
│   │   ├── borrowers_list.json
│   │   ├── borrow_queue.json
│   │   ├── return_history.json
│   │   ├── benchmark_results.csv
│   │   ├── benchmark_all_algorithms.png
│   │   └── benchmark_nlogn.png
│   │
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── queue.py
│   │   ├── stack.py
│   │   ├── linked_list.py
│   │   └── bts.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── borrower.py
│   │   └── reader.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── book_repo.py
│   │   ├── borrower_repo.py
│   │   ├── queue_repo.py
│   │   ├── reader_repo.py
│   │   └── return_history_repo.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   ├── borrow_service.py
│   │   ├── library_service.py
│   │   ├── library_state.py
│   │   ├── reader_service.py
│   │   ├── report_service.py
│   │   └── return_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── book_validator.py
│   │   ├── borrow_validator.py
│   │   ├── reader_validator.py
│   │   ├── return_validator.py
│   │   ├── ui_helpers.py
│   │   └── logging_config.py
│   │
│   ├── views/
│   │   ├── base_view.py
│   │   ├── book_view.py
│   │   ├── borrow_view.py
│   │   ├── bst_view.py
│   │   ├── library_view.py
│   │   ├── linked_list_view.py
│   │   ├── reader_view.py
│   │   ├── report_view.py
│   │   ├── return_view.py
│   │   ├── search_view.py
│   │   └── sort_view.py
│   │
│   └── tests/
│       ├── test_book_integer_validation.py
│       ├── test_book_numeric_validation.py
│       ├── test_book_text_validation.py
│       ├── test_book_view.py
│       ├── test_borrow_business_rules.py
│       ├── test_borrow_queue_consistency.py
│       ├── test_borrower_date_validation.py
│       ├── test_data_structures.py
│       ├── test_library_service.py
│       ├── test_reader_business_rules.py
│       ├── test_report_service.py
│       ├── test_repositories.py
│       ├── test_return_book_borrowed.py
│       ├── test_search_business_rules.py
│       ├── test_service_rollback_io.py
│       ├── test_sort_strategy.py
│       ├── test_sorting_business_rules.py
│       ├── test_ui_and_input.py
│       ├── test_update_book_borrowing.py
│       └── test_validation_layer.py
│
├── .gitignore
└── README.md
```

### Vai trò của từng thư mục

| Thư mục | Vai trò |
|---|---|
| `models/` | Các model/domain object: `Book`, `Borrower`, `Reader`. |
| `repositories/` | Đọc, ghi và quản lý dữ liệu JSON; tách persistence khỏi nghiệp vụ. |
| `services/` | Chứa nghiệp vụ chính của hệ thống và điều phối state. |
| `controllers/` | Điều phối thao tác từ menu đến view/service. |
| `views/` | Giao diện Console và hiển thị dữ liệu bằng Rich. |
| `data_structures/` | Cài đặt Queue, Stack, Linked List và Binary Search Tree. |
| `algorithms/` | Sorting, Strategy Pattern, benchmark và biểu đồ hiệu năng. |
| `utils/` | Validation, hỗ trợ UI và cấu hình logging. |
| `data/` | Dữ liệu JSON và kết quả benchmark. |
| `tests/` | Unit test cho model/service/repository/data structure/UI và business rules. |

### Quan hệ giữa Model và Repository

Có thể hiểu đơn giản:

```text
Model
  ↓
Repository
  ↓
JSON file
```

Ví dụ:

```text
Book
  ↓
BookRepository
  ↓
data/books.json
```

Repository chịu trách nhiệm **lưu trữ/đọc dữ liệu**, còn Model biểu diễn **đối tượng dữ liệu**. Service sử dụng Repository để thực hiện nghiệp vụ mà không cần xử lý trực tiếp việc đọc/ghi JSON.

## 9. Kiểm thử

Bộ unit test nằm trong `LibraryManagement/tests/` và bao phủ nhiều nhóm chức năng:

- Validation dữ liệu sách.
- Book View và UI.
- Quy tắc nghiệp vụ mượn sách.
- Tính nhất quán của Queue.
- Validation ngày mượn/trả.
- Queue, Stack, Linked List và BST.
- `LibraryService`.
- Reader business rules.
- `ReportService`.
- Repository và xử lý dữ liệu JSON.
- Return book.
- Search business rules.
- Sorting business rules.
- UI và input.
- Các trường hợp cập nhật/xóa sách khi đang có giao dịch.

### Kết quả hiện tại

Đã chạy bộ test hiện tại với kết quả:

```text
Ran 108 tests
OK
```

> Kết quả trên phản ánh lần chạy test hiện tại của project; khi code tiếp tục thay đổi, nên chạy lại test trước khi kết luận trạng thái cuối cùng.

### Chạy test

Từ thư mục `LibraryManagement`:

```bash
python -m unittest discover -s tests -v
```

---

## 10. GitHub Actions

Project có workflow kiểm thử tự động khi:

- Push lên `main`.
- Tạo Pull Request vào `main`.

Workflow cài Python 3.12, cài dependency cần thiết và chạy:

```bash
python -m unittest discover -s LibraryManagement/tests -v
```

---

## 11. Công nghệ

- **Python 3.12+**
- **Rich** — giao diện Console.
- **Matplotlib** — biểu đồ benchmark.
- **JSON** — lưu dữ liệu ứng dụng.
- **CSV** — lưu kết quả benchmark.
- **unittest** — unit testing.
- **Git / GitHub** — quản lý source code và CI.

---

## 12. Cài đặt và chạy

### 12.1. Yêu cầu

- Python 3.12 hoặc mới hơn.
- `pip`.
- Git nếu muốn clone repository.

### 12.2. Clone repository

```bash
git clone https://github.com/dinhanh1991/library_managerment.git
cd library_managerment/LibraryManagement
```

### 12.3. Cài thư viện

```bash
python -m pip install rich matplotlib
```

Nếu máy sử dụng `py` thay cho `python`:

```bash
py -m pip install rich matplotlib
```

### 12.4. Chạy chương trình

```bash
python main.py
```

### 12.5. Chạy unit test

```bash
python -m unittest discover -s tests -v
```

### 12.6. Chạy benchmark

```bash
python algorithms/benchmark.py
```

### 12.7. Tạo biểu đồ benchmark

```bash
python algorithms/plot_benchmark.py
```

### Quy trình nhanh

```bash
python main.py
python -m unittest discover -s tests -v
python algorithms/benchmark.py
python algorithms/plot_benchmark.py
```

---

## 13. Dữ liệu và kết quả sinh ra

Dữ liệu ứng dụng được lưu trong:

```text
data/books.json
data/readers.json
data/borrowers_list.json
data/borrow_queue.json
data/return_history.json
```

Kết quả benchmark:

```text
data/benchmark_results.csv
data/benchmark_all_algorithms.png
data/benchmark_nlogn.png
```

---

## 14. Nội dung học tập / yêu cầu bài tập

Project phục vụ việc thực hành các nội dung chính:

| Nội dung | Thực hiện |
|---|---|
| Lập kế hoạch | Có |
| Quản lý sách | Có |
| Queue | Có |
| Stack | Có |
| Linked List | Có |
| Binary Search Tree | Có |
| Thuật toán sắp xếp | 6 thuật toán |
| Benchmark | Có |
| Phân tích độ phức tạp | Có |
| Unit Test | Có |
| Git/GitHub | Có |

---

## 15. Tác giả

**Lê Đình Anh**

Project học tập môn **Cấu trúc dữ liệu và Giải thuật**.
