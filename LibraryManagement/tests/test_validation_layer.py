import unittest

from LibraryManagement.utils.validators import AppValidator


class ValidationLayerTestCase(unittest.TestCase):
    def test_text_and_number_validation(self):
        self.assertTrue(AppValidator.is_non_empty_text("  Python  "))
        self.assertFalse(AppValidator.is_non_empty_text("   "))
        self.assertFalse(AppValidator.is_non_empty_text(None))

        self.assertTrue(AppValidator.is_non_negative_int(0))
        self.assertTrue(AppValidator.is_non_negative_int(5))
        self.assertFalse(AppValidator.is_non_negative_int(-1))
        self.assertFalse(AppValidator.is_non_negative_int(True))

    def test_book_and_reader_identifiers(self):
        self.assertTrue(AppValidator.is_valid_identifier("B001"))
        self.assertTrue(AppValidator.is_valid_identifier("C-001"))
        self.assertFalse(AppValidator.is_valid_identifier("   "))
        self.assertFalse(AppValidator.is_valid_identifier(None))

    def test_normalize_identifier_and_optional_text(self):
        self.assertEqual(AppValidator.normalize_identifier("  B001  "), "B001")
        self.assertEqual(AppValidator.normalize_optional_text("  Python  "), "Python")
        self.assertEqual(AppValidator.normalize_optional_text(None), "")

        with self.assertRaises(ValueError):
            AppValidator.normalize_identifier(123)
        with self.assertRaises(ValueError):
            AppValidator.normalize_identifier("   ")
        with self.assertRaises(ValueError):
            AppValidator.normalize_optional_text(True)
