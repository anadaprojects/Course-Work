import csv
import random

class Task:
    def __init__(self, task_id, income, duration, deadline):
        self.id = task_id
        self.income = income
        self.duration = duration
        self.deadline = deadline

    def __repr__(self):
        return f"Task({self.id}, income={self.income}, duration={self.duration}, deadline={self.deadline})"

def generate_tasks(n):
    tasks = []
    for i in range(n):
        income = random.randint(1, 20)
        duration = random.randint(1, 15)
        deadline = random.randint(duration + 2, duration + 10)
        tasks.append(Task(f"J{i+1}", income, duration, deadline))
    return tasks

def read_tasks_from_csv(path):
    tasks = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tasks.append(Task(row['id'], int(row['income']), int(row['duration']), int(row['deadline'])))
    return tasks
