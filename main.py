import sys
from algorithms.greedy_algorithm import greedy_algorithm
from algorithms.genetic_algorithm import genetic_algorithm
from utils.task_generator import generate_task
from utils.task_csv_reader import read_task_from_csv
from utils.experiments_runner import (
    run_experiment_iterations,
    run_experiment_population,
    run_experiment_task_size
)

def print_menu():
    print("\nОберіть одну з опцій:")
    print("1 – Згенерувати розклад за допомогою жадібного алгоритму (A1)")
    print("2 – Згенерувати розклад за допомогою генетичного алгоритму без локального покращення (A2)")
    print("3 – Провести експеримент для визначення оптимальної кількості послідовних ітерацій (експеримент 1)")
    print("4 – Провести експеримент для дослідження впливу розміру популяції (експеримент 2)")
    print("5 – Провести експеримент для дослідження впливу розмірності задачі (експеримент 3)")
    print("0 – Вийти")

def get_task_from_user():
    print("\nОберіть джерело задачі:")
    print("1 – Зчитати з файлу (data/tasks.csv)")
    print("2 – Згенерувати автоматично")
    sub_choice = input("Ваш вибір: ").strip()
    if sub_choice == "1":
        try:
            from utils.task_csv_reader import read_task_from_csv
            task = read_task_from_csv()
            print("✅ Дані зчитано з файлу.\n")
        except Exception as e:
            print("❌ Помилка при зчитуванні:", e)
            print("⚠️  Генеруємо задачу автоматично.")
            from utils.task_generator import generate_task
            task = generate_task()
    else:
        from utils.task_generator import generate_task
        task = generate_task()
        print("✅ Задачу згенеровано автоматично.\n")
    return task


def main():
    while True:
        print_menu()
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            task = get_task_from_user()
            result = greedy_algorithm(task)
            print("Розклад (жадібний алгоритм):", result)

        elif choice == "2":
            task = get_task_from_user()
            result = genetic_algorithm(task)
            print("Розклад (генетичний алгоритм):", result)

        elif choice == "3":
            run_experiment_iterations()

        elif choice == "4":
            run_experiment_population()

        elif choice == "5":
            run_experiment_task_size()

        elif choice == "0":
            print("Завершення роботи програми.")
            sys.exit()

        else:
            print("\u274c Невідома опція. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
