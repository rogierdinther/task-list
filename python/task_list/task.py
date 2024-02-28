from datetime import datetime

class Task:
    def __init__(self, id_: int, description: str, done: bool, deadline: datetime = None) -> None:
        self.id = id_
        self.description = description
        self.done = done
        self.deadline = deadline
 
    def set_done(self, done: bool) -> None:
        self.done = done

    def is_done(self) -> bool:
        return self.done
        
    def get_deadline(self) -> datetime:
        return self.deadline


