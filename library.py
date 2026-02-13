from abc import ABC, abstractmethod
import os

class Person(ABC):
    def __init__(self, name):
        self._name = name

    @abstractmethod
    def get_role(self):
        pass

    def get_name(self):
        return self._name

class Librarian(Person):
    def get_role(self):
        return "Библиотекарь"

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self._borrowed_books = []

    def get_role(self):
        return "Пользователь"

    def borrow_book(self, book):
        if book.borrow():
            self._borrowed_books.append(book.get_title())
            print("Книга успешно выдана")
        else:
            print("Книга уже занята!")

    def return_book(self, book):
        if book.get_title() in self._borrowed_books:
            book.return_book()
            self._borrowed_books.remove(book.get_title())
            print("Книга возвращена")

class Book:
    def __init__(self, title, author, status="Доступна"):
        self._title = title
        self._author = author
        self._status = status

    def borrow(self):
        if self._status == "Доступна":
            self._status = "Выдана"
            return True
        return False

    def return_book(self):
        self._status = "Доступна"

    def get_title(self):
        return self._title

    def get_info(self):
        return f"{self._title} - {self._author} ({self._status})"

    def get_status(self):
        return self._status

class LibrarySystem:
    def __init__(self):
        self._books = []
        self._users = []
        self.load_data()


    def load_data(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    title, author, status = line.strip().split(";")
                    self._books.append(Book(title, author, status))

        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    name = line.strip()
                    self._users.append(User(name))

    def save_data(self):
        with open("books.txt", "w", encoding="utf-8") as f:
            for book in self._books:
                f.write(f"{book._title};{book._author};{book._status}\n")

        with open("users.txt", "w", encoding="utf-8") as f:
            for user in self._users:
                f.write(user.get_name() + "\n")

    def add_book(self):
        title = input("Название книги: ")
        author = input("Автор: ")
        self._books.append(Book(title, author))
        print("Книга добавлена")

    def remove_book(self):
        title = input("Название книги: ")
        for book in self._books:
            if book.get_title() == title:
                self._books.remove(book)
                print("Книга удалена")
                return
        print("Книга не найдена")

    def register_user(self):
        name = input("Имя пользователя: ")
        self._users.append(User(name))
        print("Пользователь зарегистрирован")

    def show_users(self):
        print("Пользователи:")
        for user in self._users:
            print(user.get_name())

    def show_books(self):
        print("Книги:")
        for book in self._books:
            print(book.get_info())

    def user_borrow_book(self):
        name = input("Ваше имя: ")
        title = input("Название книги: ")

        user = self.find_user(name)
        book = self.find_book(title)

        if user and book:
            user.borrow_book(book)

    def user_return_book(self):
        name = input("Ваше имя: ")
        title = input("Название книги: ")

        user = self.find_user(name)
        book = self.find_book(title)

        if user and book:
            user.return_book(book)

    def find_user(self, name):
        for user in self._users:
            if user.get_name() == name:
                return user
        print("Пользователь не найден")
        return None

    def find_book(self, title):
        for book in self._books:
            if book.get_title() == title:
                return book
        print("Книга не найдена")
        return None

def main():
    system = LibrarySystem()

    print("Выберите роль:")
    print("1: Библиотекарь")
    print("2: Пользователь")

    role = input("Ваш выбор: ")

    if role == "1":
        print("1: Добавить книгу")
        print("2: Удалить книгу")
        print("3: Зарегистрировать пользователя")
        print("4: Показать пользователей")
        print("5: Показать книги")

        choice = input("Выберите действие: ")

        if choice == "1":
            system.add_book()
        elif choice == "2":
            system.remove_book()
        elif choice == "3":
            system.register_user()
        elif choice == "4":
            system.show_users()
        elif choice == "5":
            system.show_books()

    elif role == "2":
        print("1: Взять книгу")
        print("2: Вернуть книгу")

        choice = input("Выберите действие: ")

        if choice == "1":
            system.user_borrow_book()
        elif choice == "2":
            system.user_return_book()

    system.save_data()

if __name__ == "__main__":
    main()
