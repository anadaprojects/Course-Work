import random
import copy
import matplotlib.pyplot as plt

def evaluate_solution(tickets):
    scores = [sum(q[2] for q in ticket) for ticket in tickets]
    return max(scores) - min(scores), scores

def validate_solution(tickets, data):
    used_questions = set()
    total_questions = sum(len(topic) for topic in data)
    for ticket in tickets:
        for topic_idx, question_idx, _ in ticket:
            if (topic_idx, question_idx) in used_questions:
                return False, f"Дублікат питання: тема {topic_idx}, питання {question_idx}"
            used_questions.add((topic_idx, question_idx))
    if len(used_questions) != total_questions:
        return False, f"Використано {len(used_questions)} з {total_questions} питань"
    return True, "OK"

def repair_solution(tickets, data):
    used = set()
    for ticket in tickets:
        for i, (topic_idx, question_idx, diff) in enumerate(ticket):
            key = (topic_idx, question_idx)
            if key in used:
                # знайти інше питання з цієї теми, яке ще не використано
                for new_idx in range(len(data[topic_idx])):
                    new_key = (topic_idx, new_idx)
                    if new_key not in used:
                        ticket[i] = (topic_idx, new_idx, data[topic_idx][new_idx])
                        used.add(new_key)
                        break
            else:
                used.add(key)
    return tickets

def generate_initial_population(data, pop_size):
    min_b = min(len(t) for t in data)
    population = []
    for _ in range(pop_size):
        tickets = [[] for _ in range(min_b)]
        for i, topic in enumerate(data):
            indices = list(range(len(topic)))
            random.shuffle(indices)
            for b in range(min_b):
                k = indices[b]
                difficulty = topic[k]
                tickets[b].append((i, k, difficulty))
        population.append(tickets)
    return population

def crossover(parent1, parent2):
    child = []
    for t1, t2 in zip(parent1, parent2):
        split = random.randint(1, len(t1)-1)
        child.append(t1[:split] + t2[split:])
    return child

def mutate(tickets, data, mutation_rate):
    for ticket in tickets:
        if random.random() < mutation_rate:
            index = random.randint(0, len(ticket) - 1)
            topic_idx = ticket[index][0]
            if len(data[topic_idx]) > 1:
                new_k = random.randint(0, len(data[topic_idx]) - 1)
                ticket[index] = (topic_idx, new_k, data[topic_idx][new_k])
    return tickets

def genetic_algorithm(task, pop_size=20, max_generations=100, mutation_rate=0.2, crossover_prob=0.8, patience=15):
    data = task["data"]
    min_b = min(len(t) for t in data)
    population = generate_initial_population(data, pop_size)

    best = None
    best_score = float('inf')
    best_scores = []
    best_is_valid = False
    generations_no_improve = 0

    for gen in range(max_generations):
        print(f"\n=== Покоління {gen + 1} ===")
        evaluated = []
        for i, tickets in enumerate(population):
            tickets = repair_solution(tickets, data)
            is_valid, msg = validate_solution(tickets, data)
            score, scores = evaluate_solution(tickets)
            evaluated.append(((score, scores, is_valid, msg), tickets))

            if is_valid:
                print(f"  [✓] Особина {i + 1}: Z = {score}, складності: {scores}")
            else:
                print(f"  [!] Особина {i + 1}: Z = {score} (недійсна - {msg}), складності: {scores}")

        evaluated.sort(key=lambda x: (not x[0][2], x[0][0]))
        top_score, top_scores, top_is_valid, top_msg = evaluated[0][0]
        top_tickets = evaluated[0][1]

        if top_is_valid:
            print(f"  [✓] Найкраще дійсне рішення покоління: Z = {top_score}")
        else:
            print(f"  [!] Найкраще рішення покоління: Z = {top_score} (недійсне - {top_msg})")

        if (top_is_valid and not best_is_valid) or \
           (top_is_valid == best_is_valid and top_score < best_score):
            best_score = top_score
            best = top_tickets
            best_scores = top_scores
            best_is_valid = top_is_valid
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        if generations_no_improve >= patience:
            print(f"[Зупинка] Без покращення {patience} поколінь")
            break

        new_population = []
        for _ in range(pop_size):
            valid_solutions = [sol for sol in evaluated if sol[0][2]]
            if len(valid_solutions) >= 2:
                parent1 = copy.deepcopy(random.choice(valid_solutions[:min(5, len(valid_solutions))])[1])
                parent2 = copy.deepcopy(random.choice(valid_solutions[:min(5, len(valid_solutions))])[1])
            else:
                parent1 = copy.deepcopy(random.choice(evaluated[:5])[1])
                parent2 = copy.deepcopy(random.choice(evaluated[:5])[1])

            if random.random() < crossover_prob:
                child = crossover(parent1, parent2)
            else:
                child = copy.deepcopy(parent1)
            child = mutate(child, data, mutation_rate)
            new_population.append(child)
        population = new_population

    if best is None:
        print("[!] Не знайдено жодного рішення.")
        return {
            "tickets": [],
            "scores": [],
            "max": 0,
            "min": 0,
            "diff": 0,
            "is_valid": False,
            "validation_message": "Рішення не знайдено"
        }

    return {
        "tickets": best,
        "scores": best_scores,
        "max": max(best_scores) if best_scores else 0,
        "min": min(best_scores) if best_scores else 0,
        "diff": best_score,
        "is_valid": best_is_valid,
        "validation_message": "OK" if best_is_valid else validate_solution(best, data)[1]
    }

def display_genetic_result(result):
    print("\n================== ГЕНЕТИЧНИЙ АЛГОРИТМ ==================\n")
    if not result["tickets"]:
        print("❌ Рішення не знайдено.")
        return

    if result["is_valid"]:
        print("✅ Знайдено дійсне рішення!\n")
    else:
        print(f"⚠️  Знайдено недійсне рішення: {result['validation_message']}\n")

    print("Розподіл питань по білетах:\n")
    for i, ticket in enumerate(result["tickets"], start=1):
        print(f"Білет B{i}:")
        for (topic, question, difficulty) in ticket:
            print(f"  - Тема T{topic + 1}, Питання №{question + 1}, Складність: {difficulty}")
        print(f"  >> Загальна складність: {result['scores'][i - 1]}\n")

    print("--------------- Метрики -----------------")
    print(f"Статус рішення:                {'Дійсне' if result['is_valid'] else 'Недійсне'}")
    if not result["is_valid"]:
        print(f"Причина недійсності:           {result['validation_message']}")
    print(f"Максимальна складність (Cmax): {result['max']}")
    print(f"Мінімальна складність (Cmin):  {result['min']}")
    print(f"Різниця Z = Cmax - Cmin:       {result['diff']}")
    print("=========================================\n")

    plt.figure(figsize=(10, 5))
    bars = plt.bar([f"B{i+1}" for i in range(len(result['scores']))], result['scores'])

    if result["is_valid"]:
        for bar in bars:
            bar.set_color('lightblue')
        title = "Складність кожного білета (Дійсне рішення)"
    else:
        for bar in bars:
            bar.set_color('lightcoral')
        title = f"Складність кожного білета (Недійсне рішення: {result['validation_message']})"

    plt.axhline(result["max"], color='red', linestyle='--', label='Cmax', alpha=0.7)
    plt.axhline(result["min"], color='green', linestyle='--', label='Cmin', alpha=0.7)
    plt.title(title)
    plt.xlabel("Білети")
    plt.ylabel("Сумарна складність")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()