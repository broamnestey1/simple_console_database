import os
import json

books = {}
books_show = {}

def clearTerminal(): #функция очистки терминала
    os.system('cls' if os.name == 'nt' else 'clear')

class Book:
    id = 0 #инициализация id
    file_name = "data.txt" # файл БД

    def __init__(self, id=id, title=None, author=None, year=None, status=None): # Инициализация переменных для заполнения БД. Возможно можно было реализовать через геттеры и сеттеры еще. Написал самым простым способом
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def add_book(self): # Добавление книги в библиотеку
        try:
            if os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0:
                with open(self.file_name, 'r', encoding='utf-8') as file:
                    try:
                        books_data = json.load(file)
                    except json.JSONDecodeError:
                        books_data = {}
            else:
                books_data = {}
                
            if books_data:
                max_id = max(books_data.keys()) # данная переменная для того чтобы понять, имеется ли в файле уже данные, выявление максимального айди элемента, а далее отсчет со следующего элемента
            else:
                max_id = 0

            max_id = int(max_id)
                
            self.id = max_id + 1
            self.title = input("Введите название книги: ")
            self.author = input("Введите автора книги: ")
            
            flag_on_value_date = True
            while flag_on_value_date: # проверка на цифры
                self.year = input("Введите год написания книги: ")
                if self.year.isdigit():
                    print(self.year)
                    flag_on_value_date = False
                else:
                    print("Нужен год написания книги в виде цифр!")
            
            self.status = 1  # По умолчанию, при добавлении книги будет присваиваться значение - 1 (в наличии), 0 (недоступна)

            book_exist = False
            for book_id in books_data: # Проверка на существование книги в библиотеке по трем данным
                book = books_data[book_id]
                if self.title.lower() in book['title'].lower() and self.author.lower() in book['author'].lower() and self.year == str(book['year']):
                    print("Данная книга уже существует!")
                    book_exist = True
                    break
            
            if not book_exist: # Если книги не сущетсвует, заполнение БД книгой
                books_data[self.id] = {
                    "id": self.id,
                    "title": self.title,
                    "author": self.author,
                    "year": self.year,
                    "status": self.status
                }
                    
                with open(self.file_name, 'w', encoding='utf-8') as file: # Запись в файл
                    json.dump(books_data, file, ensure_ascii=False, indent=4)
                print("Книга успешно добавлена!")
            
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден")
        self.exit_on_metod()

    def show_all_books(self): # Метод для чтобы показать все книги, имеющиеся в БД(файле)
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                if books_data:
                    for book_id in books_data:
                        book = books_data[book_id]
                        print(f"ID: {book['id']}")
                        print(f"Название: {book['title']}")
                        print(f"Автор: {book['author']}")
                        print(f"Год написания: {book['year']}")
                        print(f"Статус: {'В наличии' if book['status'] == 1 else 'Недоступна'}")
                        print("-------------------")
                else:
                    print("Библиотека пуста!")
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден")
        self.exit_on_metod()


    def search_book(self): # Поиск книги        
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                books_data = json.load(file)

                if books_data:
                    while True:
                        search_word = input("Для поиска книги введите название, автора или год написания книги (для выхода введите - q): ")
                        if search_word == 'q':
                            break
            
                        found = False  # Флаг для отслеживания найденных книг

                        for book_id in books_data:
                            book = books_data[book_id]
                            if search_word.lower() in book['title'].lower() or search_word.lower() in book['author'].lower() or search_word == str(book['year']):
                                print(f"ID: {book['id']}")
                                print(f"Название: {book['title']}")
                                print(f"Автор: {book['author']}")
                                print(f"Год написания: {book['year']}")
                                print(f"Статус: {'В наличии' if book['status'] == 1 else 'Недоступна'}")
                                print("-------------------")
                                found = True  # Устанавливаем флаг в True, если найдена хотя бы одна книга

                            if not found:
                                print("Такой книги не существует в этой библиотеке!")
                else:
                    print("Библиотека пуста!")
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден")

        self.exit_on_metod()

    def exit_on_metod(self): # Реализация меню выхода для всех методов манипулирования с БД
        while True:
            choice = input("q - Для выхода в меню!")
            if choice == 'q':
                break
            elif not choice.isnumeric():
                print("Выберите пункты, приведенные в меню!")
            elif choice.isnumeric():
                print("Выберите пункты, приведенные в меню!")
        clearTerminal()

    def delete_book(self): # Удаление книги
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
            
            if books_data:
                delete_book_id = input("Введите ID книги для удаления: ")

                if delete_book_id.isdigit(): # Проверка на то что введенное значение цифра, далее поиск айди и удаление
                    delete_book_id = int(delete_book_id)
                    if str(delete_book_id) in books_data:
                        del books_data[str(delete_book_id)]
                        with open(self.file_name, 'w', encoding='utf-8') as file:
                            json.dump(books_data, file, ensure_ascii=False, indent=4)
                        print(f"Книга с ID {delete_book_id} удалена успешно.")
                    else:
                        print(f"Книги с ID {delete_book_id} нет в библиотеке.")
                else:
                    print("Некорректный ID книги.")
            else:
                print("Библиотека пуста!")

        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден")
        
        self.exit_on_metod()

    def change_status(self): # Смена статуса книги
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                books_data = json.load(file)

            if books_data:
                book_id = input("Введите ID книги для изменения статуса: ")
                if book_id.isdigit():
                    book_id = int(book_id)
                    if str(book_id) in books_data:
                        new_status = input("Введите новый статус (1 - в наличии, 0 - недоступна): ")
                        if new_status in ['0', '1']:
                            books_data[str(book_id)]['status'] = int(new_status)
                            with open(self.file_name, 'w', encoding='utf-8') as file:
                                json.dump(books_data, file, ensure_ascii=False, indent=4)
                            print(f"Статус книги с ID {book_id} успешно изменен.")
                        else:
                            print("Некорректное значение статуса.")
                    else:
                        print(f"Книги с ID {book_id} нет в библиотеке.")
                else:
                    print("Некорректный ID книги.")
            else:
                print("Библиотека пуста!")

        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден")
        self.exit_on_metod()

    def print_menu(self): # Напечатать меню
        print("Добро пожаловать в нашу библиотеку!")
        print("Выберите пункт меню, для работы с библиотекой:")
        print("1. Отобразить все книги.")
        print("2. Добавить книгу.")
        print("3. Искать книгу.")
        print("4. Удалить книгу.")
        print("5. Изменение статуса книги.")
        print("___________________")
        print("q - для выхода")
    
    def menu(self): # Основной цикл меню
        self.print_menu()
        while True:
            choice = input()
            if choice == 'q':
                break
            elif not choice.isnumeric():
                print("Выберите пункты, приведенные в меню!")
            elif not 0 < int(choice) < 6:
                print("Выберите пункты, приведенные в меню!")
            elif int(choice) == 1:
                clearTerminal()
                self.show_all_books()
                self.print_menu()
            elif int(choice) == 2:
                clearTerminal()
                self.add_book()
                self.print_menu()
            elif int(choice) == 3:
                clearTerminal()
                self.search_book()
                self.print_menu()
            elif int(choice) == 4:
                clearTerminal()
                self.delete_book()
                self.print_menu()
            elif int(choice) == 5:
                clearTerminal()
                self.change_status()
                self.print_menu()

b = Book()
b.menu()