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
def generate_custom_task(n=5, ni=5, N=5, c_avg=10, delta_c=3):
    """
    Генерує індивідуальну задачу P(n, ni, N, c_avg, delta_c), де:
      n — кількість білетів (довжина списку в кожній темі),
      ni — кількість питань у білеті (ігнорується в генерації, але використовується в алгоритмах),
      N — кількість тем,
      c_avg — середня складність питання,
      delta_c — варіація складності.
    """
    data = []
    min_c = max(1, c_avg - delta_c)
    max_c = min(15, c_avg + delta_c)

    for _ in range(N):
        theme = [random.randint(min_c, max_c) for _ in range(n)]
        data.append(theme)

    return {
        "N": N,
        "data": data,
        "ni": ni
    }
