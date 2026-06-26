from __future__ import annotations
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes — Pet and Task use @dataclass for clean attribute declaration
# ---------------------------------------------------------------------------

@dataclass
class Task:
    task_name: str
    duration: int          # minutes
    priority: int          # 1 (low) – 3 (high)
    task_type: str
    completed: bool = False

    def edit_task(self, **kwargs) -> None:
        """Update any task attribute by passing it as a keyword argument."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def get_task_details(self) -> dict:
        """Return a dictionary of all task attributes."""
        return {
            "task_name": self.task_name,
            "duration": self.duration,
            "priority": self.priority,
            "task_type": self.task_type,
            "completed": self.completed,
        }


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    age: int
    breed: str
    special_needs: str = ""
    tasks: list[Task] = field(default_factory=list)

    def update_info(self, **kwargs) -> None:
        """Update any pet attribute by passing it as a keyword argument."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def display_pet_info(self) -> str:
        """Return a formatted string summary of the pet's profile and task count."""
        lines = [
            f"Name:          {self.pet_name}",
            f"Type:          {self.pet_type}",
            f"Breed:         {self.breed}",
            f"Age:           {self.age}",
            f"Special needs: {self.special_needs or 'None'}",
            f"Tasks:         {len(self.tasks)}",
        ]
        return "\n".join(lines)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)


# ---------------------------------------------------------------------------
# Regular classes — Owner, Planner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, owner_name: str, available_time: int, preferred_schedule: str) -> None:
        """Initialize an owner with their name, daily time budget, and schedule preference."""
        self.owner_name: str = owner_name
        self.available_time: int = available_time          # total minutes available today
        self.preferred_schedule: str = preferred_schedule  # e.g. "morning", "evening"
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Unregister a pet from this owner."""
        self.pets.remove(pet)

    def update_preferences(self, **kwargs) -> None:
        """Update any owner attribute by passing it as a keyword argument."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        return self.available_time

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all owned pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Planner:
    def __init__(self, available_time: int) -> None:
        """Initialize the planner with a time budget and empty task and plan lists."""
        self.task_list: list[Task] = []
        self.daily_plan: list[Task] = []
        self.available_time: int = available_time

    # ------------------------------------------------------------------
    # Loading tasks from an Owner (Scheduler ↔ Owner bridge)
    # ------------------------------------------------------------------

    def load_from_owner(self, owner: Owner) -> None:
        """Pull all tasks from the owner's pets and sync available time."""
        self.task_list = owner.get_all_tasks()
        self.available_time = owner.get_available_time()

    # ------------------------------------------------------------------
    # Core scheduling methods
    # ------------------------------------------------------------------

    def add_task(self, task: Task) -> None:
        """Add a task to the planner's task list."""
        self.task_list.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the planner's task list."""
        self.task_list.remove(task)

    def prioritize_tasks(self) -> list[Task]:
        """Return incomplete tasks sorted by priority descending (3 = highest)."""
        pending = [t for t in self.task_list if not t.completed]
        return sorted(pending, key=lambda t: t.priority, reverse=True)

    def generate_schedule(self) -> list[Task]:
        """Fill the daily plan greedily: highest-priority tasks first,
        stopping when available_time is exhausted."""
        self.daily_plan = []
        time_remaining = self.available_time
        for task in self.prioritize_tasks():
            if task.duration <= time_remaining:
                self.daily_plan.append(task)
                time_remaining -= task.duration
        return self.daily_plan

    def explain_plan(self) -> str:
        """Return a formatted string summarizing the current daily plan."""
        if not self.daily_plan:
            return "No plan generated yet. Call generate_schedule() first."

        total_minutes = sum(t.duration for t in self.daily_plan)
        lines = [
            f"Daily Plan  ({len(self.daily_plan)} tasks, {total_minutes} min):",
            "-" * 40,
        ]
        for i, task in enumerate(self.daily_plan, start=1):
            status = "done" if task.completed else "pending"
            lines.append(
                f"  {i}. [{task.task_type}] {task.task_name} "
                f"— {task.duration} min  (priority {task.priority}, {status})"
            )
        lines.append("-" * 40)
        lines.append(f"Time used: {total_minutes} / {self.available_time} min")
        return "\n".join(lines)
