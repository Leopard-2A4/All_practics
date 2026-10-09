# TODO здесь писать код
import os

CHAT_FILE = "chat.log"

def show_chat():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as file:
            print("Текущий текст чата:")
            print(file.read())
    else:
        print("Чат пуст.")

def send_message(name):
    message = input("Введите сообщение: ")
    with open(CHAT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{name}: {message}\n")
    print("Сообщение отправлено.")

def main():
    name = input("Введите ваше имя: ")
    while True:
        print("\nВыберите действие:")
        print("1. Посмотреть чат")
        print("2. Отправить сообщение")
        print("3. Выйти")
        choice = input("Ваш выбор: ")
        if choice == "1":
            show_chat()
        elif choice == "2":
            send_message(name)
        elif choice == "3":
            print("Выход из чата.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

main()