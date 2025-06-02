import random
import copy

def evaluate_solution(tickets):
    scores = [sum(q[2] for q in ticket) for ticket in tickets]
    return max(scores) - min(scores), scores

def generate_initial_population(data, N, ni, pop_size):
    population = []
    for _ in range(pop_size):
        tickets = [[] for _ in range(ni)]
        for i in range(N):
            indices = list(range(ni))
            random.shuffle(indices)
            for b in range(ni):
                difficulty = data[i][indices[b]]
                tickets[b].append((i, indices[b], difficulty))
        population.append(tickets)
    return population

def crossover(parent1, parent2):
    return copy.deepcopy(random.choice([parent1, parent2]))

def mutate(tickets, data, N, ni, mutation_rate):
    for ticket in tickets:
        if random.random() < mutation_rate:
            i = random.randint(0, N - 1)
            new_k = random.randint(0, ni - 1)
            ticket[i] = (i, new_k, data[i][new_k])
    return tickets

def genetic_algorithm(task, pop_size=10, max_generations=100, mutation_rate=0.1, patience=10):
    N = task["N"]
    ni = task["ni"]
    data = task["data"]

    population = generate_initial_population(data, N, ni, pop_size)
    best = None
    best_score = float('inf')
    best_scores = []
    generations_no_improve = 0

    for gen in range(max_generations):
        evaluated = []
        for t in population:
            diff, scores = evaluate_solution(t)
            evaluated.append((diff, t, scores))

        evaluated.sort(key=lambda x: x[0])

        if evaluated[0][0] < best_score:
            best_score = evaluated[0][0]
            best = evaluated[0][1]
            best_scores = evaluated[0][2]
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        if generations_no_improve >= patience:
            break

        new_population = []
        for _ in range(pop_size):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child, data, N, ni, mutation_rate)
            new_population.append(child)
        population = new_population

    return {
        "tickets": best,
        "scores": best_scores,
        "max": max(best_scores),
        "min": min(best_scores),
        "diff": best_score
    }
