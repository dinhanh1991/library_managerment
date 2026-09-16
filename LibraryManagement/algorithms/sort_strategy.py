from LibraryManagement.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort,
)


class SortStrategy:
    """Strategy interface for book sorting algorithms."""

    name = ""

    def sort(self, books, key):
        raise NotImplementedError


class BubbleSortStrategy(SortStrategy):
    name = "Bubble Sort"

    def sort(self, books, key):
        return bubble_sort(books, key)


class SelectionSortStrategy(SortStrategy):
    name = "Selection Sort"

    def sort(self, books, key):
        return selection_sort(books, key)


class InsertionSortStrategy(SortStrategy):
    name = "Insertion Sort"

    def sort(self, books, key):
        return insertion_sort(books, key)


class QuickSortStrategy(SortStrategy):
    name = "Quick Sort"

    def sort(self, books, key):
        return quick_sort(books, key)


class MergeSortStrategy(SortStrategy):
    name = "Merge Sort"

    def sort(self, books, key):
        return merge_sort(books, key)


class HeapSortStrategy(SortStrategy):
    name = "Heap Sort"

    def sort(self, books, key):
        return heap_sort(books, key)
