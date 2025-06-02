def greedy_algorithm(task):
    """
    Жадібний алгоритм для формування білетів з приблизно рівною складністю
    Вхід: task — словник з ключами:
        - N: кількість тем
        - ni: кількість питань на тему (однаково для всіх тем)
        - data: список списків складностей питань [N][ni]
    Вихід: список білетів (по одному питанню з кожної теми)
    """
    N = task["N"]
    ni = task["ni"]
    data = task["data"]

    n = ni  # кількість білетів = кількість питань у кожній темі
    tickets = [[] for _ in range(n)]     # білети — списки вибраних питань (індекси)
    ticket_scores = [0 for _ in range(n)]  # сумарна складність кожного білета

    for i in range(N):  # проходимо по кожній темі
        # Отримуємо список (індекс, складність) і сортуємо за спаданням складності
        questions = sorted([(k, data[i][k]) for k in range(ni)], key=lambda x: -x[1])

        used = set()  # індекси питань, які вже використали з цієї теми
        for k, difficulty in questions:
            # Знайти білет, у якому ще немає питання з цієї теми і найменша складність
            candidate = None
            min_score = float('inf')
            for b in range(n):
                if len(tickets[b]) == i and ticket_scores[b] < min_score:
                    candidate = b
                    min_score = ticket_scores[b]

            if candidate is not None:
                tickets[candidate].append((i, k, difficulty))  # зберігаємо (тема, номер, складність)
                ticket_scores[candidate] += difficulty
                used.add(k)

            if len(used) == ni:
                break

    return {
        "tickets": tickets,
        "scores": ticket_scores,
        "max": max(ticket_scores),
        "min": min(ticket_scores),
        "diff": max(ticket_scores) - min(ticket_scores)
    }
