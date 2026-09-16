import unittest

from LibraryManagement.algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort,
)
from LibraryManagement.models.book import Book


class TestSortingBusinessRules(unittest.TestCase):

    def setUp(self):
        self.algorithms = [
            bubble_sort,
            selection_sort,
            insertion_sort,
            quick_sort,
            merge_sort,
            heap_sort,
        ]

        self.books = [
            Book("S003", "The Great Gatsby", "Author C", 1925, 5),
            Book("S001", "Python Basics", "Author A", 2024, 5),
            Book("S004", "Data Structures", "Author D", 2010, 5),
            Book("S002", "Algorithms", "Author B", 2020, 5),
        ]

    def assert_sorted_by_key(self, algorithm, key):
        books = self.books.copy()

        result, comparisons, assignments = algorithm(books, key)

        values = []
        for book in result:
            if key == "title":
                values.append(book.title)
            elif key == "publish_year":
                values.append(book.publish_year)
            else:
                values.append(book.book_id)

        self.assertEqual(values, sorted(values))
        self.assertGreaterEqual(comparisons, 0)
        self.assertGreaterEqual(assignments, 0)

    def test_all_algorithms_sort_by_title(self):
        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                self.assert_sorted_by_key(algorithm, "title")

    def test_all_algorithms_sort_by_publish_year(self):
        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                self.assert_sorted_by_key(algorithm, "publish_year")

    def test_all_algorithms_sort_by_book_id(self):
        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                self.assert_sorted_by_key(algorithm, "book_id")

    def test_empty_and_single_item_lists(self):
        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                empty_result, comparisons, assignments = algorithm([], "title")
                self.assertEqual(empty_result, [])
                self.assertGreaterEqual(comparisons, 0)
                self.assertGreaterEqual(assignments, 0)

                book = self.books[0]
                single_result, comparisons, assignments = algorithm([book], "title")
                self.assertEqual(single_result, [book])
                self.assertGreaterEqual(comparisons, 0)
                self.assertGreaterEqual(assignments, 0)

    def test_duplicate_values_are_supported(self):
        books = [
            Book("S003", "Python", "A", 2024, 1),
            Book("S001", "Python", "B", 2020, 1),
            Book("S002", "Algorithms", "C", 2024, 1),
            Book("S004", "Algorithms", "D", 2020, 1),
        ]

        for algorithm in self.algorithms:
            with self.subTest(algorithm=algorithm.__name__):
                result, _, _ = algorithm(books.copy(), "title")
                titles = [book.title for book in result]
                self.assertEqual(titles, sorted(titles))
                self.assertEqual(len(result), len(books))


if __name__ == "__main__":
    unittest.main()
