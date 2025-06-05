import sys

from algorithms.genetic_algorithm import genetic_algorithm,  display_genetic_result
from utils.task_generator import generate_task
from utils.task_csv_reader import read_task_from_csv
from algorithms.greedy_algorithm import greedy_algorithm, print_greedy_result, print_initial_task_data, display_greedy_table, display_greedy_chart

from utils.experiments_runner import (
    run_experiment_iterations,
    run_experiment_population,
    run_experiment_task_size
)

def print_menu():
    print("\nОберіть одну з опцій:")
    print("1 – Сформувати білети за допомогою жадібного алгоритму")
    print("2 – Сформувати білети за допомогою генетичного алгоритму ")
    print("3 – Експеримент 1: вплив параметра K (ітерації без покращення)")
    print("4 – Експеримент 2: вплив розміру популяції (P)")
    print("5 – Експеримент 3: вплив кількості білетів (n)")
    print("0 – Вийти")


def get_task_from_user():
    print("\nОберіть джерело задачі:")
    print("1 – Зчитати з файлу (data/tasks.csv)")
    print("2 – Згенерувати автоматично")
    print("3 – Ввести вручну")
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
    elif sub_choice == "2":
        from utils.task_generator import generate_task
        task = generate_task()
        print("Задачу згенеровано автоматично.\n")
    elif sub_choice == "3":
        try:
            N = int(input("Введіть кількість тем: "))
            data = []
            for i in range(N):
                line = input(f"Введіть складності питань для теми {i+1} через пробіл: ")
                theme = [int(x) for x in line.strip().split()]
                data.append(theme)
            task = {"N": N, "data": data}
            print("Задачу введено вручну.\n")
        except Exception as e:
            print("Помилка при введенні:", e)
            from utils.task_generator import generate_task
            task = generate_task()
            print("Задачу згенеровано автоматично.\n")
    else:
        from utils.task_generator import generate_task
        task = generate_task()
        print("Невірний вибір. Задачу згенеровано автоматично.\n")

    # Уніфікація структури для роботи алгоритмів
    task["ni"] = min(len(row) for row in task["data"])
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
                display_greedy_chart(result)

 
           

        elif choice == "2":
             task = get_task_from_user()
             result = genetic_algorithm(task)
             display_genetic_result(result)

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
