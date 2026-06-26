from __future__ import annotations
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes — Pet and Task use @dataclass for clean attribute declaration
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    pet_name: str
    pet_type: str
    age: int
    breed: str
    special_needs: str = ""

    def update_info(self, **kwargs) -> None:
        pass

    def display_pet_info(self) -> str:
        pass


@dataclass
class Task:
    task_name: str
    duration: int          # minutes
    priority: int          # 1 (low) – 3 (high)
    task_type: str
    completed: bool = False

    def edit_task(self, **kwargs) -> None:
        pass

    def mark_complete(self) -> None:
        pass

    def get_task_details(self) -> dict:
        pass


# ---------------------------------------------------------------------------
# Regular classes — Owner, Planner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, owner_name: str, available_time: int, preferred_schedule: str) -> None:
        self.owner_name: str = owner_name
        self.available_time: int = available_time          # total minutes available today
        self.preferred_schedule: str = preferred_schedule  # e.g. "morning", "evening"

    def update_preferences(self, **kwargs) -> None:
        pass

    def get_available_time(self) -> int:
        pass


class Planner:
    def __init__(self, available_time: int) -> None:
        self.task_list: list[Task] = []
        self.daily_plan: list[Task] = []
        self.available_time: int = available_time

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> list[Task]:
        pass

    def prioritize_tasks(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
