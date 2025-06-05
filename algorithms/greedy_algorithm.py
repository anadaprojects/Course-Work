from tabulate import tabulate # type: ignore

def greedy_algorithm(task):
    N = task["N"]
    data = task["data"]
    ni_list = [len(t) for t in data]
    n = min(ni_list)  # кількість білетів = мінімальна кількість питань серед тем

    tickets = [[] for _ in range(n)]
    ticket_scores = [0] * n
    xikb = [[[0 for _ in range(n)] for _ in range(len(data[i]))] for i in range(N)]

    for i in range(N):
        questions = sorted([(k, data[i][k]) for k in range(len(data[i]))], key=lambda x: -x[1])
        used = set()
        for k, cik in questions:
            candidate = None
            min_score = float("inf")
            for b in range(n):
                if len(tickets[b]) == i and ticket_scores[b] < min_score:
                    candidate = b
                    min_score = ticket_scores[b]
            if candidate is not None:
                tickets[candidate].append((i, k, cik))
                ticket_scores[candidate] += cik
                xikb[i][k][candidate] = 1
                used.add(k)
            if len(used) == len(data[i]):
                break

    Cmax = max(ticket_scores)
    Cmin = min(ticket_scores)
    Z = Cmax - Cmin

    return {
        "xikb": xikb,
        "tickets": tickets,
        "scores": ticket_scores,
        "Cmax": Cmax,
        "Cmin": Cmin,
        "Z": Z
    }

def print_initial_task_data(task):
    print("\n========== ПОЧАТКОВІ ДАНІ ЗАДАЧІ ==========\n")
    print(f"Кількість тем: {task['N']}")
    ni_list = [len(t) for t in task["data"]]
    print("Кількість питань у кожній темі:", ", ".join(f"Тема {i+1}: {n}" for i, n in enumerate(ni_list)))
    print("\nСкладності питань по темах:")
    for i, topic in enumerate(task["data"], start=1):
        difficulties = ", ".join(str(x) for x in topic)
        print(f"  Тема {i}: {difficulties}")
    print("\n===========================================\n")

def display_greedy_table(result):
    data = []
    for i, ticket in enumerate(result["tickets"], start=1):
        for (topic, question, difficulty) in ticket:
            data.append([
                f"B{i}",
                f"T{topic + 1}",
                question + 1,
                difficulty,
                result["scores"][i - 1]
            ])
    headers = ["Білет", "Тема", "Питання №", "Складність", "Загальна складність білета"]
    print("\n" + tabulate(data, headers=headers, tablefmt="fancy_grid"))

def print_greedy_result(result):
    print("\n================== ЖАДІБНИЙ АЛГОРИТМ ==================\n")
    print("Розподіл питань по білетах:\n")
    for i, ticket in enumerate(result["tickets"], start=1):
        print(f"Білет B{i}:")
        for (topic, question, difficulty) in ticket:
            print(f"  - Тема T{topic + 1}, Питання №{question + 1}, Складність: {difficulty}")
        print(f"  >> Загальна складність: {result['scores'][i - 1]}\n")
    print("--------------- Метрики -----------------")
    print(f"Максимальна складність (Cmax): {result['Cmax']}")
    print(f"Мінімальна складність (Cmin): {result['Cmin']}")
    print(f"Різниця Z = Cmax - Cmin:        {result['Z']}")
    print("=========================================\n")


import matplotlib.pyplot as plt

def display_greedy_chart(result):
    plt.figure(figsize=(10, 5))
    x_labels = [f"B{i+1}" for i in range(len(result["scores"]))]
    plt.bar(x_labels, result["scores"])
    plt.axhline(result["Cmax"], color='red', linestyle='--', label='Cmax')
    plt.axhline(result["Cmin"], color='green', linestyle='--', label='Cmin')
    plt.title("Складність кожного білета (Жадібний алгоритм)")
    plt.xlabel("Білети")
    plt.ylabel("Сумарна складність")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()