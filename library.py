import json
import os
from typing import List


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    def from_dict(data: dict) -> 'Book':
        book = Book(data['id'], data['title'], data['author'], data['year'])
        book.status = data['status']
        return book


class Library:
    
    def __init__(self, filename: str = "library.json"):
        self.books: List[Book] = []
        self.filename = filename
        self.next_id = 1
        self.load_books()

    def load_books(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                self.books = [Book.from_dict(data) for data in books_data]
                self.next_id = max(book.id for book in self.books) + 1 if self.books else 1

    def save_books(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        book = Book(self.next_id, title, author, year)
        self.books.append(book)
        self.next_id += 1
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book.id}.")

    def remove_book(self, book_id: int) -> None:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Ошибка: Книга с ID {book_id} не найдена.")

    def search_books(self, query: str) -> List[Book]:
        results = [
            book for book in self.books if (query.lower() in book.title.lower() or
                                             query.lower() in book.author.lower() or
                                             query in str(book.year))
        ]
        return results

    def display_books(self) -> None:
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"{book.id}: {book.title} автор: {book.author} ({book.year}) - {book.status}")

    def change_status(self, book_id: int, new_status: str) -> None:
        if new_status not in ["в наличии", "выдана"]:
            print("Ошибка: Неверный статус. Используйте 'в наличии' или 'выдана'.")
            return
        
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
                return
        print(f"Ошибка: Книга с ID {book_id} не найдена.")


def main() -> None:
    library = Library()

    while True:
        print("\n--- Управление библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        
        choice = input("Выберите действие: ")

        try:
            if choice == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                library.add_book(title, author, year)

            elif choice == '2':
                book_id = int(input("Введите ID книги для удаления: "))

                library.remove_book(book_id)

            elif choice == '3':
                query = input("Введите название или автора для поиска: ")
                results = library.search_books(query)
                if results:
                    print("Результаты поиска:")
                    for book in results:
                        print(f"{book.id}: {book.title} автор: {book.author} ({book.year}) - {book.status}")
                else:
                    print("Книги не найдены.")

            elif choice == '4':
                library.display_books()

            elif choice == '5':
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                library.change_status(book_id, new_status)

            elif choice == '6':
                print("Выход из программы.")
                break

            else:
                print("Ошибка: Неверный выбор. Пожалуйста, выберите правильное действие.")
                
        except ValueError:
            print("Ошибка: Неверный ввод. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
