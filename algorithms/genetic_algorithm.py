import random
import copy

def evaluate_solution(tickets):
    scores = [sum(q[2] for q in ticket) for ticket in tickets]
    return max(scores) - min(scores), scores

def validate_solution(tickets, data):
    """Перевіряє коректність розподілу питань"""
    used_questions = set()
    total_questions = sum(len(topic) for topic in data)
    
    for ticket in tickets:
        for topic_idx, question_idx, difficulty in ticket:
            question_id = (topic_idx, question_idx)
            if question_id in used_questions:
                return False, f"Дублікат питання: тема {topic_idx}, питання {question_idx}"
            used_questions.add(question_id)
    
    if len(used_questions) != total_questions:
        return False, f"Використано {len(used_questions)} з {total_questions} питань"
    
    return True, "OK"

def generate_initial_population(data, pop_size):
    N = len(data)
    
    # Перевіряємо, чи можна створити білети
    topic_lengths = [len(topic) for topic in data]
    if not all(length > 0 for length in topic_lengths):
        raise ValueError("Всі теми повинні містити хоча б одне питання")
    
    min_b = min(topic_lengths)
    max_b = max(topic_lengths)
    
    if min_b != max_b:
        print(f"Увага: різна кількість питань у темах ({min_b}-{max_b}). Використовуватимемо {min_b} білетів.")
    
    population = []
    for _ in range(pop_size):
        tickets = [[] for _ in range(min_b)]
        
        # Розподіляємо питання з кожної теми
        for topic_idx, topic in enumerate(data):
            # Беремо тільки перші min_b питань, щоб уникнути невикористаних питань
            questions = [(topic_idx, i, difficulty) for i, difficulty in enumerate(topic[:min_b])]
            random.shuffle(questions)
            
            # Розподіляємо по одному питанню на білет
            for ticket_idx, question in enumerate(questions):
                tickets[ticket_idx].append(question)
        
        # Перемішуємо питання в кожному білеті
        for ticket in tickets:
            random.shuffle(ticket)
            
        population.append(tickets)
    
    return population

def crossover(parent1, parent2):
    """Порядкове схрещування з збереженням унікальності питань"""
    child = [[] for _ in range(len(parent1))]
    
    # Для кожної теми окремо
    topics = {}
    for ticket_idx, ticket in enumerate(parent1):
        for topic_idx, question_idx, difficulty in ticket:
            if topic_idx not in topics:
                topics[topic_idx] = []
            topics[topic_idx].append((ticket_idx, question_idx, difficulty))
    
    # Схрещуємо розподіл кожної теми
    for topic_idx, questions in topics.items():
        # Беремо половину розподілу від першого батька, половину від другого
        if random.random() < 0.5:
            # Використовуємо розподіл з parent1
            for ticket_idx, question_idx, difficulty in questions:
                child[ticket_idx].append((topic_idx, question_idx, difficulty))
        else:
            # Використовуємо розподіл з parent2 для цієї теми
            for ticket_idx, ticket in enumerate(parent2):
                for topic_idx2, question_idx, difficulty in ticket:
                    if topic_idx2 == topic_idx:
                        child[ticket_idx].append((topic_idx2, question_idx, difficulty))
    
    return child

def mutate(tickets, data, mutation_rate):
    """Мутація через обмін питаннями між білетами"""
    if random.random() < mutation_rate:
        # Вибираємо два випадкові білети
        ticket1_idx = random.randint(0, len(tickets) - 1)
        ticket2_idx = random.randint(0, len(tickets) - 1)
        
        if ticket1_idx != ticket2_idx and len(tickets[ticket1_idx]) > 0 and len(tickets[ticket2_idx]) > 0:
            # Вибираємо випадкові питання з кожного білета
            q1_idx = random.randint(0, len(tickets[ticket1_idx]) - 1)
            q2_idx = random.randint(0, len(tickets[ticket2_idx]) - 1)
            
            # Обмінюємо питання
            tickets[ticket1_idx][q1_idx], tickets[ticket2_idx][q2_idx] = \
                tickets[ticket2_idx][q2_idx], tickets[ticket1_idx][q1_idx]
    
    return tickets

def mutate_alternative(tickets, data, mutation_rate):
    """Альтернативна мутація через заміну питання в межах теми"""
    N = len(data)
    
    for ticket_idx, ticket in enumerate(tickets):
        if random.random() < mutation_rate and len(ticket) > 0:
            # Вибираємо випадкове питання в білеті
            question_idx = random.randint(0, len(ticket) - 1)
            topic_idx, old_q_idx, old_difficulty = ticket[question_idx]
            
            # Якщо в темі є інші питання
            if len(data[topic_idx]) > 1:
                # Знаходимо всі питання цієї теми в інших білетах
                other_questions = []
                for other_ticket_idx, other_ticket in enumerate(tickets):
                    if other_ticket_idx != ticket_idx:
                        for other_q_idx, (other_topic_idx, other_q_num, other_diff) in enumerate(other_ticket):
                            if other_topic_idx == topic_idx:
                                other_questions.append((other_ticket_idx, other_q_idx, other_q_num, other_diff))
                
                # Якщо знайшли питання цієї теми в інших білетах, обмінюємося
                if other_questions:
                    other_ticket_idx, other_q_idx, other_q_num, other_diff = random.choice(other_questions)
                    
                    # Обмін питаннями
                    tickets[ticket_idx][question_idx] = (topic_idx, other_q_num, other_diff)
                    tickets[other_ticket_idx][other_q_idx] = (topic_idx, old_q_idx, old_difficulty)
    
    return tickets

def genetic_algorithm(task, pop_size=20, max_generations=100, mutation_rate=0.2, patience=15, use_validation=True):
    data = task["data"]
    N = len(data)
    
    # Перевірка вхідних даних
    topic_lengths = [len(topic) for topic in data]
    min_b = min(topic_lengths)
    max_b = max(topic_lengths)
    
    print(f"Кількість тем: {N}")
    print(f"Кількість питань у темах: {topic_lengths}")
    print(f"Буде створено {min_b} білетів\n")

    population = generate_initial_population(data, pop_size)
    
    # Валідація початкової популяції
    if use_validation:
        print("Перевірка початкової популяції...")
        for i, tickets in enumerate(population[:3]):  # Перевіряємо перші 3 рішення
            is_valid, message = validate_solution(tickets, data)
            print(f"Рішення {i+1}: {message}")
        print()

    best = None
    best_score = float('inf')
    best_scores = []
    generations_no_improve = 0

    for generation in range(max_generations):
        # Оцінка популяції
        evaluated = []
        for tickets in population:
            if use_validation:
                is_valid, _ = validate_solution(tickets, data)
                if not is_valid:
                    # Призначаємо дуже погану оцінку некоректним рішенням
                    evaluated.append(((float('inf'), []), tickets))
                    continue
            
            score, scores = evaluate_solution(tickets)
            evaluated.append(((score, scores), tickets))
        
        # Сортування за якістю
        evaluated.sort(key=lambda x: x[0][0])

        # Оновлення найкращого рішення
        top_score, top_scores = evaluated[0][0]
        top_tickets = evaluated[0][1]
        
        if top_score < best_score:
            best_score = top_score
            best = copy.deepcopy(top_tickets)
            best_scores = top_scores
            generations_no_improve = 0
            print(f"Покоління {generation+1}: нова найкраща оцінка = {best_score:.2f}")
        else:
            generations_no_improve += 1

        # Критерій зупинки
        if generations_no_improve >= patience:
            print(f"Зупинка через відсутність покращень протягом {patience} поколінь")
            break

        # Створення нового покоління
        new_population = []
        elite_size = max(1, pop_size // 10)  # 10% еліти
        
        # Зберігаємо найкращі рішення (елітизм)
        for i in range(elite_size):
            if evaluated[i][0][0] != float('inf'):
                new_population.append(copy.deepcopy(evaluated[i][1]))
        
        # Генеруємо решту популяції
        while len(new_population) < pop_size:
            # Турнірна селекція
            tournament_size = 3
            parents = random.sample(evaluated[:pop_size//2], tournament_size)
            parent1 = min(parents, key=lambda x: x[0][0])[1]
            
            parents = random.sample(evaluated[:pop_size//2], tournament_size)
            parent2 = min(parents, key=lambda x: x[0][0])[1]
            
            # Схрещування та мутація
            child = crossover(copy.deepcopy(parent1), copy.deepcopy(parent2))
            child = mutate_alternative(child, data, mutation_rate)
            new_population.append(child)
        
        population = new_population

    print(f"Алгоритм завершено після {generation+1} поколінь")
    
    # Фінальна валідація
    if use_validation and best is not None:
        is_valid, message = validate_solution(best, data)
        print(f"Фінальна валідація: {message}")

    return {
        "tickets": best,
        "scores": best_scores,
        "max": max(best_scores) if best_scores else 0,
        "min": min(best_scores) if best_scores else 0,
        "diff": best_score
    }


import matplotlib.pyplot as plt

def display_genetic_result(result):
    """
    Виводить таблицю та графік результатів генетичного алгоритму.
    """
    if result["tickets"] is None:
        print("Не вдалося знайти рішення!")
        return
        
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

