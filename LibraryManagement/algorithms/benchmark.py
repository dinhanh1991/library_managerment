import copy
import csv
import random
import time
from pathlib import Path

from LibraryManagement.models.book import Book
from LibraryManagement.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    heap_sort,
    quick_sort,
    merge_sort
)


# ============================================================
# ĐƯỜNG DẪN DỮ LIỆU
# ============================================================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


# ============================================================
# TẠO DỮ LIỆU SÁCH NGẪU NHIÊN
# ============================================================

def create_books(n):

    books = []

    for i in range(n):

        book = Book(
            f"S{i + 1:04d}",
            f"Book {i + 1}",
            f"Author {i + 1}",
            2000 + (i % 25),
            5
        )

        books.append(book)

    random.shuffle(books)

    return books


# ============================================================
# CHẠY BENCHMARK
# ============================================================

def run_benchmark():

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Quick Sort", quick_sort),
        ("Merge Sort", merge_sort),
        ("Heap Sort", heap_sort)
    ]

    sizes = [25, 100, 500, 1000, 10000]

    key = "title"

    number_of_runs = 5

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    csv_file = DATA_DIR / "benchmark_results.csv"

    all_results = []

    print()
    print("=" * 95)
    print("                  📊 BENCHMARK THUẬT TOÁN SẮP XẾP")
    print("=" * 95)

    print(f"Tiêu chí sắp xếp: Tên sách")
    print(f"Số lần chạy mỗi thuật toán: {number_of_runs}")
    print(f"Kích thước dữ liệu: {sizes}")

    # ========================================================
    # BENCHMARK TỪNG KÍCH THƯỚC
    # ========================================================

    for size in sizes:

        print()
        print("=" * 95)
        print(
            f"             SO SÁNH VỚI {size:,} CUỐN SÁCH"
        )
        print("=" * 95)

        original_books = create_books(size)

        results = []

        # ----------------------------------------------------
        # Chạy từng thuật toán
        # ----------------------------------------------------

        for name, algorithm in algorithms:

            total_time = 0
            total_comparisons = 0
            total_assignments = 0

            # Chạy nhiều lần
            for _ in range(number_of_runs):

                # Dùng cùng dữ liệu đầu vào
                books = copy.deepcopy(original_books)

                start_time = time.perf_counter()

                result, comparisons, assignments = algorithm(
                    books,
                    key
                )

                end_time = time.perf_counter()

                execution_time = (
                    end_time - start_time
                ) * 1000

                total_time += execution_time
                total_comparisons += comparisons
                total_assignments += assignments

            # Tính trung bình
            average_time = total_time / number_of_runs
            average_comparisons = (
                total_comparisons / number_of_runs
            )
            average_assignments = (
                total_assignments / number_of_runs
            )

            result_data = {
                "size": size,
                "name": name,
                "comparisons": average_comparisons,
                "assignments": average_assignments,
                "time": average_time
            }

            results.append(result_data)
            all_results.append(result_data)

        # ====================================================
        # HIỂN THỊ BẢNG
        # ====================================================

        print()

        print(
            f"{'Thuật toán':<20}"
            f"{'So sánh':>18}"
            f"{'Phép gán':>18}"
            f"{'Thời gian (ms)':>22}"
        )

        print("-" * 95)

        for result in results:

            print(
                f"{result['name']:<20}"
                f"{result['comparisons']:>18,.0f}"
                f"{result['assignments']:>18,.0f}"
                f"{result['time']:>22.6f}"
            )

        print("-" * 95)

        # Thuật toán nhanh nhất
        fastest = min(
            results,
            key=lambda result: result["time"]
        )

        print(
            f"🏆 Nhanh nhất: {fastest['name']} "
            f"({fastest['time']:.6f} ms)"
        )

    # ========================================================
    # LƯU CSV
    # ========================================================

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "So luong sach",
            "Thuat toan",
            "So phep so sanh trung binh",
            "So phep gan trung binh",
            "Thoi gian trung binh (ms)"
        ])

        for result in all_results:

            writer.writerow([
                result["size"],
                result["name"],
                f"{result['comparisons']:.0f}",
                f"{result['assignments']:.0f}",
                f"{result['time']:.6f}"
            ])

    # ========================================================
    # HOÀN THÀNH
    # ========================================================

    print()
    print("=" * 95)
    print("✅ BENCHMARK HOÀN TẤT")
    print(f"📁 Đã lưu kết quả: {csv_file}")
    print("=" * 95)
