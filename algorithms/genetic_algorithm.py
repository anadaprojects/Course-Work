import random
import copy

def evaluate_solution(tickets):
    scores = [sum(q[2] for q in ticket) for ticket in tickets]
    return max(scores) - min(scores), scores

def generate_initial_population(data, pop_size):
    N = len(data)
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
    N = len(data)
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
    N = len(data)
    min_b = min(len(t) for t in data)

    population = generate_initial_population(data, pop_size)
    best = None
    best_score = float('inf')
    best_scores = []
    generations_no_improve = 0

    for _ in range(max_generations):
        evaluated = [(evaluate_solution(t), t) for t in population]
        evaluated.sort(key=lambda x: x[0][0])

        top_score, top_tickets = evaluated[0][0][0], evaluated[0][1]
        if top_score < best_score:
            best_score = top_score
            best = top_tickets
            best_scores = evaluate_solution(top_tickets)[1]
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        if generations_no_improve >= patience:
            break

        new_population = []
        for _ in range(pop_size):
            parent1 = copy.deepcopy(random.choice(evaluated[:5])[1])
            parent2 = copy.deepcopy(random.choice(evaluated[:5])[1])
            if random.random() < crossover_prob:
             child = crossover(parent1, parent2)
            else:
              child = copy.deepcopy(parent1)

            child = mutate(child, data, mutation_rate)
            new_population.append(child)
        population = new_population

    return {
        "tickets": best,
        "scores": best_scores,
        "max": max(best_scores),
        "min": min(best_scores),
        "diff": best_score
    }


import matplotlib.pyplot as plt

def display_genetic_result(result):
    """
    Виводить таблицю та графік результатів генетичного алгоритму.
    """
    print("\n================== ГЕНЕТИЧНИЙ АЛГОРИТМ ==================\n")
    print("Розподіл питань по білетах:\n")

    for i, ticket in enumerate(result["tickets"], start=1):
        print(f"Білет B{i}:")
        for (topic, question, difficulty) in ticket:
            print(f"  - Тема T{topic + 1}, Питання №{question + 1}, Складність: {difficulty}")
        print(f"  >> Загальна складність: {result['scores'][i - 1]}\n")

    print("--------------- Метрики -----------------")
    print(f"Максимальна складність (Cmax): {result['max']}")
    print(f"Мінімальна складність (Cmin): {result['min']}")
    print(f"Різниця Z = Cmax - Cmin:        {result['diff']}")
    print("=========================================\n")

    # Побудова графіка
    plt.figure(figsize=(10, 5))
    bars = plt.bar([f"B{i+1}" for i in range(len(result['scores']))], result['scores'])
    plt.axhline(result["max"], color='red', linestyle='--', label='Cmax')
    plt.axhline(result["min"], color='green', linestyle='--', label='Cmin')
    plt.title("Складність кожного білета")
    plt.xlabel("Білети")
    plt.ylabel("Сумарна складність")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()
