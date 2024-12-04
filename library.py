import json
from enum import Enum
from typing import List, Dict, Union


class BookStatus(Enum):
    AVAILABLE = "в наличии"
    ISSUED = "выдана"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: BookStatus = BookStatus.AVAILABLE):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Union[int, str]]) -> 'Book':
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=BookStatus(data["status"])
        )


class LibraryStorage:
    def __init__(self, data_file: str):
        self.data_file = data_file

    def load_books(self) -> List[Book]:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self, books: List[Book]) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)


class Library:
    def __init__(self, storage: LibraryStorage):
        self.storage = storage
        self.books: List[Book] = self.storage.load_books()

    def add_book(self, title: str, author: str, year: int) -> None:
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id=new_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self.storage.save_books(self.books)
        print(f"Книга '{title}' успешно добавлена с ID: {new_id}")

    def remove_book(self, book_id: int) -> None:
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.storage.save_books(self.books)
            print(f"Книга с ID {book_id} успешно удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, keyword: str) -> List[Book]:
        return [
            book for book in self.books
            if keyword.lower() in book.title.lower() or
               keyword.lower() in book.author.lower() or
               keyword == str(book.year)
        ]

    def display_books(self) -> None:
        if not self.books:
            print("Библиотека пуста.")
            return
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<5} {'Статус':<10}")
        print("-" * 70)
        for book in self.books:
            print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<5} {book.status.value:<10}")

    def update_status(self, book_id: int, new_status: str) -> None:
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            if BookStatus.has_value(new_status):
                book.status = BookStatus(new_status)
                self.storage.save_books(self.books)
                print(f"Статус книги с ID {book_id} обновлён на '{new_status}'.")
            else:
                print("Недопустимый статус. Используйте 'в наличии' или 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    storage = LibraryStorage(data_file='library_data.json')
    library = Library(storage=storage)
    print("Добро пожаловать в библиотеку!")

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите номер команды: ").strip()
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            if year.isdigit():
                library.add_book(title, author, int(year))
            else:
                print("Год издания должен быть числом.")
        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            if book_id.isdigit():
                library.remove_book(int(book_id))
            else:
                print("ID должен быть числом.")
        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска: ")
            results = library.search_books(keyword)
            if results:
                for book in results:
                    print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<5} {book.status.value:<10}")
            else:
                print("Книги не найдены.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_status = input("Введите новый статус (в наличии/выдана): ")
            if book_id.isdigit():
                library.update_status(int(book_id), new_status)
            else:
                print("ID должен быть числом.")
        elif choice == "6":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
