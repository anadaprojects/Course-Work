import math
import statistics
import time
import itertools
import matplotlib.pyplot as plt


from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.greedy_algorithm import greedy_algorithm
from utils.task_generator import generate_custom_task, generate_task

def run_experiment_iterations():
    print("\n=== Експеримент 1: Вплив параметра K (ітерації без покращення) ===")
    print("[DEBUG] Виклик run_experiment_iterations")

    k_values = [3, 5, 10, 20]
    ni = 5
    N = 5
    c_avg = 10
    delta_c = 3

    avg_diffs = []
    avg_times = []

    for patience in k_values:
        diffs = []
        times = []
        for _ in range(5):
            task = generate_custom_task(n=10, ni=ni, N=N, c_avg=c_avg, delta_c=delta_c)
            start = time.time()
            result = genetic_algorithm(task, patience=patience)
            end = time.time()
            diffs.append(result['diff'])
            times.append(end - start)

        avg_diffs.append(statistics.mean(diffs))
        avg_times.append(statistics.mean(times))
        print(f"K = {patience}: середня різниця = {avg_diffs[-1]:.2f}, час = {avg_times[-1]:.2f} с")

    # Побудова графіків
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(k_values, avg_diffs, marker='o')
    plt.title("Середня різниця (Z) від K")
    plt.xlabel("K (ітерації без покращення)")
    plt.ylabel("Z")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(k_values, avg_times, marker='o', color='orange')
    plt.title("Середній час виконання від K")
    plt.xlabel("K")
    plt.ylabel("Час (с)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def run_experiment_population():
    print("\n=== Експеримент 2: Вплив параметрів ГА (P, pc, pm) ===")

    P_values = [30, 50, 100]
    pc_values = [0.6, 0.8, 0.9]
    pm_values = [0.01, 0.05, 0.1]
    k = 5

    combinations = list(itertools.product(P_values, pc_values, pm_values))
    labels = []
    values = []

    for P, pc, pm in combinations:
        diffs = []
        for _ in range(k):
            task = generate_custom_task(n=10, ni=5, N=5, c_avg=10, delta_c=3)
            result = genetic_algorithm(task, pop_size=P, mutation_rate=pm, crossover_prob=pc, patience=10)
            diffs.append(result['diff'])
        avg_diff = statistics.mean(diffs)
        label = f"P={P}, pc={pc}, pm={pm}"
        labels.append(label)
        values.append(avg_diff)
        print(f"{label} => середня різниця: {avg_diff:.2f}")

    # Побудова горизонтального графіка
    plt.figure(figsize=(12, 6))
    plt.barh(labels, values)
    plt.xlabel("Середня різниця Z")
    plt.title("Вплив параметрів ГА на якість рішень")
    plt.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def run_experiment_task_size():
    print("\n=== Експеримент 3: Вплив розмірності задачі (n) ===")

    n_values = [10, 20, 30, 40, 50]
    greedy_diffs_avg = []
    greedy_times_avg = []
    ga_diffs_avg = []
    ga_times_avg = []

    for n in n_values:
        greedy_diffs = []
        greedy_times = []
        ga_diffs = []
        ga_times = []

        for _ in range(20):
            task = generate_custom_task(n=n, ni=5, N=5, c_avg=10, delta_c=3)

            start_greedy = time.time()
            result_greedy = greedy_algorithm(task)
            end_greedy = time.time()

            start_ga = time.time()
            result_ga = genetic_algorithm(task, pop_size=50, mutation_rate=0.05, crossover_prob=0.8, patience=10)
            end_ga = time.time()

            greedy_diffs.append(result_greedy['Z'])
            greedy_times.append(end_greedy - start_greedy)

            ga_diffs.append(result_ga['diff'])
            ga_times.append(end_ga - start_ga)

        greedy_diffs_avg.append(statistics.mean(greedy_diffs))
        greedy_times_avg.append(statistics.mean(greedy_times))
        ga_diffs_avg.append(statistics.mean(ga_diffs))
        ga_times_avg.append(statistics.mean(ga_times))

        print(f"\nn = {n}")
        print(f"  ЖА: Z = {greedy_diffs_avg[-1]:.2f}, час = {greedy_times_avg[-1]:.2f} с")
        print(f"  ГА: Z = {ga_diffs_avg[-1]:.2f}, час = {ga_times_avg[-1]:.2f} с")

    # Побудова графіків
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.plot(n_values, greedy_diffs_avg, marker='o', label='ЖА')
    plt.plot(n_values, ga_diffs_avg, marker='o', label='ГА')
    plt.title("Середня різниця (Z) залежно від n")
    plt.xlabel("Кількість білетів (n)")
    plt.ylabel("Z")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(n_values, greedy_times_avg, marker='o', label='ЖА')
    plt.plot(n_values, ga_times_avg, marker='o', label='ГА')
    plt.title("Середній час виконання залежно від n")
    plt.xlabel("Кількість білетів (n)")
    plt.ylabel("Час (с)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def run_experiment_pi_log():
    print("\n=== Експеримент 4: Логарифмічна залежність π = α · n · log₂(n) ===")
    print("[DEBUG] Виклик run_experiment_pi_log")

    n = 30
    ni = 5
    N = 5
    c_avg = 10
    delta_c = 3
    k = 5

    alphas = [10, 20, 50, 80, 100]
    pi_values = [int(alpha * n * math.log2(n)) for alpha in alphas]
    avg_diffs = []
    avg_times = []

    for pi in pi_values:
        diffs = []
        times = []
        for _ in range(k):
            task = generate_custom_task(n=n, ni=ni, N=N, c_avg=c_avg, delta_c=delta_c)
            start = time.time()
            result = genetic_algorithm(task, patience=pi)
            end = time.time()
            diffs.append(result['diff'])
            times.append(end - start)

        avg_diffs.append(statistics.mean(diffs))
        avg_times.append(statistics.mean(times))
        print(f"π = {pi}: середня різниця = {avg_diffs[-1]:.2f}, час = {avg_times[-1]:.2f} с")

