import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.data_structures.bts import BinarySearchTree
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower


class DataStructuresTestCase(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("B002", "Data Structures", "Bob", 2023, 2),
            Book("B001", "Python Basics", "Alice", 2024, 3),
            Book("B003", "Algorithms", "Carol", 2022, 1),
        ]

    def test_linked_list_add_search_delete(self):
        linked_list = BookLinkedList()

        self.assertFalse(linked_list.add_book(None))
        self.assertIsNone(linked_list.head)

        for book in self.books:
            self.assertTrue(linked_list.add_book(book))

        self.assertEqual(linked_list.search_book("B001").title, "Python Basics")
        self.assertIsNone(linked_list.search_book("B999"))
        self.assertTrue(linked_list.delete_book("B002"))
        self.assertIsNone(linked_list.search_book("B002"))
        self.assertFalse(linked_list.delete_book("B999"))

    def test_bst_insert_search_duplicate_and_inorder(self):
        tree = BinarySearchTree()
        for book in self.books:
            tree.insert(book)

        self.assertEqual(tree.search("B001").title, "Python Basics")
        self.assertIsNone(tree.search("B999"))

        tree.insert(Book("B001", "Duplicate", "Other", 2025, 9))
        self.assertEqual(tree.search("B001").title, "Python Basics")

        output = io.StringIO()
        with redirect_stdout(output):
            tree.inorder(tree.root)

        lines = output.getvalue().splitlines()
        self.assertEqual([line.split("|")[0].strip() for line in lines], ["B001", "B002", "B003"])

    def test_queue_is_fifo(self):
        queue = Queue()
        first = Borrower("R001", "Reader One", "B001")
        second = Borrower("R002", "Reader Two", "B002")

        self.assertTrue(queue.is_empty())
        queue.enqueue(first)
        queue.enqueue(second)

        self.assertIs(queue.dequeue(), first)
        self.assertIs(queue.dequeue(), second)
        self.assertIsNone(queue.dequeue())
        self.assertTrue(queue.is_empty())

    def test_stack_is_lifo(self):
        stack = Stack()
        first = Borrower("R001", "Reader One", "B001")
        second = Borrower("R002", "Reader Two", "B002")

        stack.push(first)
        stack.push(second)

        self.assertIs(stack.pop(), second)
        self.assertIs(stack.pop(), first)
        self.assertIsNone(stack.pop())
        self.assertTrue(stack.is_empty())


if __name__ == "__main__":
    unittest.main()
