from datetime import datetime

class Command:
    def __init__(self, command_line: str):
        self.command_line = command_line
        
        parts = command_line.split(" ", 1)
        self.name = parts[0]
        if (len(parts) == 1):
            self.argumentString = None
        else:
            self.argumentString = parts[1]

class DeadlineCommand:
    def __init__(self, argument_string: str):
        parts = argument_string.split(" ")
        self.task_id = int(parts[0])
        self.date = datetime.strptime(parts[1], "%Y-%m-%d").date()


class TodayCommand:
    def __init__(self) -> None:
        pass
    

def create_command(inputString: str) -> Command:
    parts = inputString.split(" ", 1)
    name = parts[0]
    if (name == "today"):
        return TodayCommand()
    elif (name != "deadline"):
        return Command(inputString)
    else:
        return DeadlineCommand(parts[1])