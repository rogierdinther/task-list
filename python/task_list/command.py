class Command:
    def __init__(self, command_line: str):
        self.command_line = command_line
        
        parts = command_line.split(" ", 1)
        self.name = parts[0]
        if (len(parts) == 1):
            self.argumentString = None
        else:
            self.argumentString = parts[1]