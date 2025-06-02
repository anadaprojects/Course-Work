import random

def generate_task(N=3, ni=3, mean=5, delta=2):
    """
    Генерує задачу з N темами, по ni питань у кожній темі.
    Складності генеруються рівномірно випадково в межах [mean - delta, mean + delta].

    Повертає словник:
        - N: кількість тем
        - ni: кількість питань у кожній темі
        - data: матриця складностей [N][ni]
    """
    data = []
    for i in range(N):
        theme = []
        for k in range(ni):
            difficulty = random.randint(mean - delta, mean + delta)
            theme.append(difficulty)
        data.append(theme)

    return {
        "N": N,
        "ni": ni,
        "data": data
    }
