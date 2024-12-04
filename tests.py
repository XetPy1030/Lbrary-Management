import unittest
from library import Library, LibraryStorage, BookStatus

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library(storage=LibraryStorage(data_file='test_library.json'))

    def tearDown(self):
        import os
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    def test_add_book(self):
        self.library.add_book("Тестовая книга", "Автор", 2023)
        self.assertEqual(len(self.library.books), 1)

    def test_remove_book(self):
        self.library.add_book("Тестовая книга", "Автор", 2023)
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        self.library.add_book("Тестовая книга", "Автор", 2023)
        results = self.library.search_books("Тестовая")
        self.assertEqual(len(results), 1)

    def test_update_status(self):
        self.library.add_book("Тестовая книга", "Автор", 2023)
        self.library.update_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, BookStatus.ISSUED)

if __name__ == "__main__":
    unittest.main()
