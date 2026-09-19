import csv
from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# ĐƯỜNG DẪN DỮ LIỆU
# ============================================================

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
csv_file = DATA_DIR / "benchmark_results.csv"


# ============================================================
# ĐỌC DỮ LIỆU TỪ FILE CSV
# ============================================================

data = {}

with open(csv_file, "r", encoding="utf-8-sig") as file:

    reader = csv.DictReader(file)

    for row in reader:

        size = int(row["So luong sach"])
        algorithm = row["Thuat toan"]
        execution_time = float(
            row["Thoi gian trung binh (ms)"]
        )

        if size not in data:
            data[size] = {}

        data[size][algorithm] = execution_time


# ============================================================
# DANH SÁCH KÍCH THƯỚC DỮ LIỆU
# ============================================================

sizes = sorted(data.keys())

algorithms = [
    "Bubble Sort",
    "Selection Sort",
    "Insertion Sort",
    "Heap Sort",
    "Quick Sort",
    "Merge Sort"
]


# ============================================================
# BIỂU ĐỒ 1 - SO SÁNH CẢ 6 THUẬT TOÁN
# ============================================================

plt.figure(figsize=(10, 6))

for algorithm in algorithms:

    times = []

    for size in sizes:
        times.append(data[size][algorithm])

    plt.plot(
        sizes,
        times,
        marker="o",
        label=algorithm
    )

plt.title("So sánh thời gian chạy của các thuật toán sắp xếp")

plt.xlabel("Số lượng sách")

plt.ylabel("Thời gian chạy (ms)")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    DATA_DIR / "benchmark_all_algorithms.png",
    dpi=300
)

plt.show()


# ============================================================
# BIỂU ĐỒ 2 - SO SÁNH NHÓM O(n log n)
# ============================================================

fast_algorithms = [
    "Heap Sort",
    "Quick Sort",
    "Merge Sort"
]

plt.figure(figsize=(10, 6))

for algorithm in fast_algorithms:

    times = []

    for size in sizes:
        times.append(data[size][algorithm])

    plt.plot(
        sizes,
        times,
        marker="o",
        label=algorithm
    )

plt.title("So sánh thời gian chạy nhóm thuật toán O(n log n)")

plt.xlabel("Số lượng sách")

plt.ylabel("Thời gian chạy (ms)")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    DATA_DIR / "benchmark_nlogn.png",
    dpi=300
)

plt.show()


# ============================================================
# THÔNG BÁO
# ============================================================

print()
print("=" * 70)
print("✅ Đã tạo 2 biểu đồ benchmark:")
print("=" * 70)
print(f"1. {DATA_DIR / 'benchmark_all_algorithms.png'}")
print(f"2. {DATA_DIR / 'benchmark_nlogn.png'}")
print("=" * 70)
