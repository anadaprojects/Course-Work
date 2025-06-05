from utils.task_generator import generate_task
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.greedy_algorithm import greedy_algorithm
import statistics
import time

# Експеримент 1: Вплив кількості ітерацій без покращення (K)
def run_experiment_iterations():
    print("\nЕксперимент 1: Вплив кількості ітерацій без покращення (K)")
    K_values = [3, 5, 7, 10]
    for K in K_values:
        results = []
        for _ in range(5):
            task = generate_task()
            result = genetic_algorithm(task, patience=K)
            results.append(result['diff'])
        print(f"K = {K}: середня різниця складностей = {statistics.mean(results):.2f}")

# Експеримент 2: Вплив розміру популяції (P)
def run_experiment_population():
    print("\nЕксперимент 2: Вплив розміру популяції (P)")
    P_values = [4, 6, 8, 10]
    for P in P_values:
        results = []
        for _ in range(5):
            task = generate_task()
            result = genetic_algorithm(task, pop_size=P, max_generations=100, mutation_rate=0.1, patience=5)
            results.append(result['diff'])
        print(f"Популяція = {P}: середня різниця складностей = {statistics.mean(results):.2f}")

# Експеримент 3: Вплив розміру задачі (кількості білетів)
def run_experiment_task_size():
    print("\nЕксперимент 3: Вплив розміру задачі (кількості білетів)")
    for _ in range(5):
        task = generate_task()

        start_g = time.time()
        result_g = genetic_algorithm(task, patience=5)
        end_g = time.time()

        start_r = time.time()
        result_r = greedy_algorithm(task)
        end_r = time.time()

        print(f"n = {task['ni']}:")
        print(f"  Генетичний: різниця = {result_g['diff']}, час = {end_g - start_g:.2f} с")
        print(f"  Жадібний   : різниця = {result_r['Z']}, час = {end_r - start_r:.2f} с")

