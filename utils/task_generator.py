import random

def generate_task():
    """
    Генерує випадкову задачу з:
    - Випадковою кількістю тем (3–10)
    - Випадковою кількістю питань на тему (3–10)
    - Випадковим середнім значенням складності (5–10)
    - Випадковим розкидом складності (1–5)
    
    Повертає:
        - N: кількість тем
        - ni: кількість питань у кожній темі
        - data: список списків складностей [N][ni]
    """
    N = random.randint(3, 10)
    ni = random.randint(3, 10)
    mean = random.randint(5, 10)
    delta = random.randint(1, 5)

    min_diff = max(1, mean - delta)
    max_diff = min(15, mean + delta)

    data = []
    for _ in range(N):
        theme = [random.randint(min_diff, max_diff) for _ in range(ni)]
        data.append(theme)

    return {
        "N": N,
        "ni": ni,
        "data": data
    }
