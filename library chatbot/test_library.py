import unittest

from lib2 import Library


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()

    def test_book_search_returns_matching_books(self):
        results = self.library.search_books("python")
        self.assertTrue(results)
        self.assertEqual(results[0]["title"], "Python Crash Course")

    def test_borrow_book_updates_stock(self):
        result = self.library.borrow_book(1)
        self.assertTrue(result["success"])
        self.assertEqual(self.library.books[1].available, 4)
        self.assertEqual(self.library.books[1].borrowed, 1)

    def test_return_book_restores_stock(self):
        self.library.borrow_book(2)
        result = self.library.return_book(2)
        self.assertTrue(result["success"])
        self.assertEqual(self.library.books[2].available, 4)
        self.assertEqual(self.library.books[2].borrowed, 0)

    def test_borrowing_limit_is_enforced(self):
        for book_id in [1, 2, 3]:
            self.library.borrow_book(book_id)

        result = self.library.borrow_book(4)
        self.assertFalse(result["success"])
        self.assertIn("limit", result["message"].lower())


if __name__ == "__main__":
    unittest.main()
