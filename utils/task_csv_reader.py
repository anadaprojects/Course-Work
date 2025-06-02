import csv

def read_task_from_csv(filepath="data/tasks.csv"):
    """
    Зчитує задачу з CSV-файлу. Формат:
    - перший рядок: N,ni
    - далі N рядків, по ni чисел (складності)
    """
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
        N = int(first_row[0])
        ni = int(first_row[1])
        data = []

        for row in reader:
            data.append([int(x) for x in row])

        assert len(data) == N and all(len(row) == ni for row in data)

        return {
            "N": N,
            "ni": ni,
            "data": data
        }
