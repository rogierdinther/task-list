from datetime import datetime
from typing import Dict, List

from task_list.console import Console
from task_list.task import Task
from task_list.command import Command, DeadlineCommand, create_command, TodayCommand, DeleteCommand

class TaskCollection:
    def __init__(self):
        self.tasks: Dict[str, List[Task]] = dict()

    def get_tasks_for_deadline(self, deadline: datetime):
        tasks: Dict[str, List[Task]] = dict()
        for project, task_list in self.tasks.items():
            task_list_for_deadline = [t for t in task_list if t.get_deadline() == deadline]
            if (task_list_for_deadline):
                tasks[project] = task_list_for_deadline
        return tasks

    def get_task(self, id):
        for project, task_list in self.tasks.items():
            for task in task_list:
                if task.id == id:
                    return task
        return None
    
    def delete_task(self, id: int) -> None:
        for project, task_list in self.tasks.items():
            for task in task_list:
                if task.id == id:
                    task_list.remove(task)
        return

class TaskList:
    QUIT = "quit"

    def __init__(self, console: Console) -> None:
        self.console = console
        self.last_id: int = 0
        self.task_collection = TaskCollection()

    def run(self) -> None:
        while True:
            inputString = self.console.input("> ")
            if inputString == self.QUIT:
                break

            command = create_command(inputString)

            self.execute(command)

    def execute(self, command: Command) -> None:
        if isinstance(command, DeadlineCommand):
            self.deadline(command)
        # elif isinstance(command, DeleteCommand):
        #     self.delete(command)
        elif isinstance(command, TodayCommand):
            self.today()
        elif command.name == "show":
            self.show()
        elif command.name == "add":
            self.add(command.argumentString)
        elif command.name == "delete":
            self.delete(command.argumentString)
        elif command.name == "check":
            self.check(command.argumentString)
        elif command.name == "uncheck":
            self.uncheck(command.argumentString)
        elif command.name == "help":
            self.help()
        else:
            self.error(command.name)

    def today(self):
        deadline = datetime.now().date() 
        tasks_with_deadline = self.task_collection.get_tasks_for_deadline(deadline)
        if len(tasks_with_deadline.items()) == 0:
            self.console.print("Nothing to do")
            self.console.print("")
        else:
            self.console.print("todos")
            self.console.print("  [ ] 1: Do the thing.")
            self.console.print("")

    def show(self) -> None:
        for project, tasks in self.task_collection.tasks.items():
            self.console.print(project)
            for task in tasks:
                self.console.print(f"  [{'x' if task.is_done() else ' '}] {task.id}: {task.description}")
            self.console.print()

    def add(self, command_line: str) -> None:
        sub_command_rest = command_line.split(" ", 1)
        sub_command = sub_command_rest[0]
        if sub_command == "project":
            self.add_project(sub_command_rest[1])
        elif sub_command == "task":
            project_task = sub_command_rest[1].split(" ", 1)
            self.add_task(project_task[0], project_task[1])

    # def delete(self, command: DeleteCommand) -> None:
        # self.task_collection.delete_task(command.task_id)
    def delete(self, command_line: str) -> None:
        self.task_collection.delete_task(int(command_line))

    def deadline(self, command: DeadlineCommand):
        task = self.task_collection.get_task(command.task_id)
        task.deadline = command.date

    def add_project(self, name: str) -> None:
        self.task_collection.tasks[name] = []

    def add_task(self, project: str, description: str) -> None:
        project_tasks = self.task_collection.tasks.get(project)
        if project_tasks is None:
            self.console.print(f"Could not find a project with the name {project}.")
            self.console.print()
            return
        project_tasks.append(Task(self.next_id(), description, False, None))

    def check(self, id_string: str) -> None:
        self.set_done(id_string, True)

    def uncheck(self, id_string: str) -> None:
        self.set_done(id_string, False)

    def set_done(self, id_string: str, done: bool) -> None:
        id_ = int(id_string)
        task = self.task_collection.get_task(id_)
        if task:
            task.set_done(done)
            return
        self.console.print(f"Could not find a task with an ID of {id_}")
        self.console.print()

    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def error(self, command: str) -> None:
        self.console.print(f"I don't know what the command {command} is.")
        self.console.print()

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id

