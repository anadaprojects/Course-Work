import csv

def read_task_from_csv(filepath="data/tasks.csv"):
    """
    Зчитує задачу з CSV-файлу. Формат:
    - перший рядок: N — кількість тем
    - далі N рядків, кожен — список складностей питань для теми
    """
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
        N = int(first_row[0])  # Кількість тем
        data = []

        for _ in range(N):
            row = next(reader)
            data.append([int(x) for x in row])

        return {
            "N": N,
            "ni_list": [len(row) for row in data],  # Кількість питань на кожну тему
            "data": data
        }
