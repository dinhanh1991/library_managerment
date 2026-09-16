from LibraryManagement.models.book import Book
from LibraryManagement.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort
)


books = [
    Book("S003", "The Great Gatsby", "F. Scott Fitzgerald", 1925, 8),
    Book("S001", "Lập trình Python", "Nguyễn Văn A", 2024, 6),
    Book("S004", "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "Nguyễn Nhật Ánh", 2010, 12),
    Book("S002", "Cấu Trức Dữ Liệu Nâng Cao", "Trần Phi Vũ", 2026, 13)
]


print("=====BUBBLE SẮP XẾP THEO TÊN =====")

result, comparisons, assignments = bubble_sort(books.copy(), "title")

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n=====BUBBLE SẮP XẾP THEO NĂM =====")

result, comparisons, assignments = bubble_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
print("\n===== SELECTION SORT THEO TÊN =====")

result, comparisons, assignments = selection_sort(
    books.copy(),
    "title"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n===== SELECTION SORT THEO NĂM =====")

result, comparisons, assignments = selection_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
print("\n===== INSERTION SORT THEO TÊN =====")

result, comparisons, assignments = insertion_sort(
    books.copy(),
    "title"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n===== INSERTION SORT THEO NĂM =====")

result, comparisons, assignments = insertion_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
print("\n===== QUICK SORT THEO TÊN =====")

result, comparisons, assignments = quick_sort(
    books.copy(),
    "title"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n===== QUICK SORT THEO NĂM =====")

result, comparisons, assignments = quick_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
print("\n===== MERGE SORT THEO TÊN =====")

result, comparisons, assignments = merge_sort(
    books.copy(),
    "title"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n===== MERGE SORT THEO NĂM =====")

result, comparisons, assignments = merge_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
print("\n===== HEAP SORT THEO TÊN =====")

result, comparisons, assignments = heap_sort(
    books.copy(),
    "title"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")


print("\n===== HEAP SORT THEO NĂM =====")

result, comparisons, assignments = heap_sort(
    books.copy(),
    "publish_year"
)

for book in result:
    print(book)

print(f"So sánh: {comparisons}")
print(f"Gán: {assignments}")
