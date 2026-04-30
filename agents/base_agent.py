from abc import ABC, abstractmethod
from datetime import datetime


class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name
        self.status = "idle"
        self.result = None
        self.logs = []

    def log(self, message, level="INFO"):
        entry = {"time": datetime.now(), "level": level, "message": message}
        self.logs.append(entry)
        print(f"[{self.name}] {level}: {message}")

    @abstractmethod
    def run(self, **kwargs):
        pass

    def get_status(self):
        return {"agent": self.name, "status": self.status, "result": self.result}
