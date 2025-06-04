from tabulate import tabulate

def greedy_algorithm(task):
    """
    Жадібний алгоритм для формування білетів із приблизно рівною складністю.

    Вхід:
        task — словник з ключами:
            - N: кількість тем
            - ni: кількість питань на тему (однакова для всіх тем)
            - data: список списків складностей питань [N][ni]

    Вихід:
        - xikb: матриця вибору питань (бінарна)
        - Cmax: максимальна складність серед білетів
        - Cmin: мінімальна складність серед білетів
        - Z: цільова функція (Cmax - Cmin)
    """
    N = task["N"]
    ni = task["ni"]
    data = task["data"]
    n = ni  # кількість білетів дорівнює кількості питань на тему

    # Ініціалізація білетів і складностей
    tickets = [[] for _ in range(n)]
    ticket_scores = [0] * n

    # Бінарна матриця вибору xikb[i][k][b] = 1, якщо питання k з теми i у білеті b
    xikb = [[[0 for _ in range(n)] for _ in range(ni)] for _ in range(N)]

    for i in range(N):  # для кожної теми
        # Відсортувати питання за спаданням складності
        questions = sorted([(k, data[i][k]) for k in range(ni)], key=lambda x: -x[1])

        used = set()
        for k, cik in questions:
            # Знайти білет, у якому ще немає питання з теми i, і який має найменшу складність
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

            if len(used) == ni:
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
    """
    Виводить початкові дані задачі: кількість тем, питань і складності.
    """
    print("\n========== ПОЧАТКОВІ ДАНІ ЗАДАЧІ ==========\n")
    print(f"Кількість тем: {task['N']}")
    print(f"Кількість питань у кожній темі: {task['ni']}")
    print("\nСкладності питань по темах:")

    for i, topic in enumerate(task["data"], start=1):
        difficulties = ", ".join(str(x) for x in topic)
        print(f"  Тема {i}: {difficulties}")
    
    print("\n===========================================\n")


def display_greedy_table(result):
    """
    Виводить результат жадібного алгоритму у вигляді таблиці.
    """
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
    """
    Форматований вивід результатів жадібного алгоритму.
    """
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
