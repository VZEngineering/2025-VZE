""" This is an exercise created by Grok 3 for me to learn and solve -"""

try:
    with open("tasks.txt", "r") as file:
        tasks = file.read().splitlines()
except FileNotFoundError:
    tasks = []


def add_task(tasks):
    task = input("Enter the task: ")
    tasks.append(task)
    print(f"Task '{task}' added")


def list_tasks(tasks):
    if not tasks:
        print("No tasks yet!")
    else:
        for i, task in enumerate(tasks):
            print(f"{i + 1}: {task}")


def done_task(tasks):
    if not tasks:
        print("No tasks to mark as done!")
    else:
        print("which task is done? (Enter ***", len(tasks)+1, "*** to cancel out)")
        for i, task in enumerate(tasks):
            print(f"{i + 1}: {task}")
        while True:
            try:
                num = int(input("Enter the task number: "))
                if 1 <= num <= len(tasks):
                    removed_task = tasks.pop(num - 1)
                    print(f"Task '{removed_task}' is done")
                    break
                elif num == len(tasks) + 1:
                    print("Cancelled marking task as done")
                    break
                else:
                    print("Invalid task number")
            except ValueError:
                print("Input a valid task number from the list")


while True:
    action = input("what do you want to do? (add/list/done/quit): ")
    if action == "add":
        add_task(tasks)  # call the function to add a task
    elif action == "list":
        list_tasks(tasks)  # call the function to list tasks
    elif action == "done":
        done_task(tasks)  # call the function to mark a task as done
    elif action == "quit":
        with open("tasks.txt", "w") as file:
            for task in tasks:
                file.write(task + "\n")
        print("Tasks saved to tasks.txt")
        break
    else:
        print(">>> Unknown command!\n>>> Try: add, list, done or quit")
