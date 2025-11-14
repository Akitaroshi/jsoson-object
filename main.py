import json
import os

FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return []

    with open(FILENAME, "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
            if not isinstance(tasks, list):
                print("Ошибка: данные в файле не являются списком.")
                return []
            return tasks
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def view_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
    else:
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task['title']} — [{task['priority']}]")


def add_task(tasks):
    title = input("Введите название задачи: ")
    priority = input("Введите приоритет (Низкий/Средний/Высокий): ")
    task = {"title": title, "priority": priority}
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена.")


def delete_task(tasks):
    if not tasks:
        print("Нет задач для удаления.")
        return

    view_tasks(tasks)
    try:
        number = int(input("Введите номер задачи: "))
        if 1 <= number <= len(tasks):
            tasks.pop(number - 1)
            save_tasks(tasks)
            print("Задача удалена.")
        else:
            print("Некорректный номер задачи.")
    except ValueError:
        print("Ошибка: введён неверный номер задачи.")


def main():
    print("Добро пожаловать в менеджер задач!")

    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.")


if __name__ == "__main__":
    main()
