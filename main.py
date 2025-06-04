import sys

from algorithms.genetic_algorithm import genetic_algorithm
from utils.task_generator import generate_task
from utils.task_csv_reader import read_task_from_csv
from algorithms.greedy_algorithm import greedy_algorithm, print_greedy_result, print_initial_task_data, display_greedy_table

from utils.experiments_runner import (
    run_experiment_iterations,
    run_experiment_population,
    run_experiment_task_size
)

def print_menu():
    print("\nОберіть одну з опцій:")
    print("1 – Сформувати білети за допомогою жадібного алгоритму")
    print("2 – Сформувати білети за допомогою генетичного алгоритму ")
    print("3 – Ввести вручну")
    print("4 – Експеримент 1: вплив параметра K (ітерації без покращення)")
    print("5 – Експеримент 2: вплив розміру популяції (P)")
    print("6 – Експеримент 3: вплив кількості білетів (n)")
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
            print("Дані зчитано з файлу.\n")
        except Exception as e:
            print("Помилка при зчитуванні:", e)
            print("Генеруємо задачу автоматично.")
            from utils.task_generator import generate_task
            task = generate_task()
    else:
        from utils.task_generator import generate_task
        task = generate_task()
        print("Задачу згенеровано автоматично.\n")
    return task



def main():
    while True:
        print_menu()
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            task = get_task_from_user()
            if task:
                print_initial_task_data(task)
                result = greedy_algorithm(task)
                print_greedy_result(result)
                display_greedy_table(result)
 
           

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
