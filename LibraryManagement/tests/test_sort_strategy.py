import unittest

from LibraryManagement.algorithms.sort_strategy import (
    BubbleSortStrategy,
    SelectionSortStrategy,
    InsertionSortStrategy,
    QuickSortStrategy,
    MergeSortStrategy,
    HeapSortStrategy,
)
from LibraryManagement.models.book import Book


class TestSortStrategy(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("S003", "C", "Author C", 2020, 1),
            Book("S001", "A", "Author A", 2022, 1),
            Book("S002", "B", "Author B", 2021, 1),
        ]

    def test_all_strategies_sort_by_title(self):
        strategies = [
            BubbleSortStrategy(),
            SelectionSortStrategy(),
            InsertionSortStrategy(),
            QuickSortStrategy(),
            MergeSortStrategy(),
            HeapSortStrategy(),
        ]

        for strategy in strategies:
            with self.subTest(strategy=strategy.name):
                books = list(self.books)
                result, comparisons, assignments = strategy.sort(books, "title")
                self.assertEqual([book.title for book in result], ["A", "B", "C"])
                self.assertGreaterEqual(comparisons, 0)
                self.assertGreaterEqual(assignments, 0)


if __name__ == "__main__":
    unittest.main()
