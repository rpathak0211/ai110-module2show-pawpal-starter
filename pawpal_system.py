from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta


def _to_minutes(hhmm: str) -> int:
    """Convert a 'HH:MM' string to total minutes since midnight."""
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


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
    frequency: str = "once"       # "once" | "daily" | "weekly"
    start_time: str = ""          # optional "HH:MM" wall-clock start
    due_date: str = ""            # optional "YYYY-MM-DD" due date

    def edit_task(self, **kwargs) -> None:
        """Update any task attribute by passing it as a keyword argument."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Task:
        """Return a new incomplete Task due on the next daily or weekly occurrence.

        Uses timedelta(days=1) for daily tasks and timedelta(weeks=1) for weekly tasks,
        anchored to due_date if set, otherwise today. Raises ValueError for one-off tasks.
        """
        delta = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(self.frequency)
        if delta is None:
            raise ValueError(f"'{self.task_name}' is not a recurring task (frequency='{self.frequency}').")
        base = date.fromisoformat(self.due_date) if self.due_date else date.today()
        return Task(
            task_name=self.task_name,
            duration=self.duration,
            priority=self.priority,
            task_type=self.task_type,
            completed=False,
            frequency=self.frequency,
            start_time=self.start_time,
            due_date=str(base + delta),
        )

    def get_task_details(self) -> dict:
        """Return a dictionary of all task attributes."""
        return {
            "task_name": self.task_name,
            "duration": self.duration,
            "priority": self.priority,
            "task_type": self.task_type,
            "completed": self.completed,
            "frequency": self.frequency,
            "start_time": self.start_time,
            "due_date": self.due_date,
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

    def filter_tasks_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the named pet, or an empty list if not found."""
        for pet in self.pets:
            if pet.pet_name == pet_name:
                return pet.tasks
        return []


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

    # ------------------------------------------------------------------
    # Algorithmic layer
    # ------------------------------------------------------------------

    def sort_by_duration(self, ascending: bool = True) -> list[Task]:
        """Return task_list sorted by duration without mutating the list.

        Shortest-first (ascending=True) is useful for packing the most tasks into
        a tight schedule; longest-first surfaces high-cost tasks for review.
        """
        return sorted(self.task_list, key=lambda t: t.duration, reverse=not ascending)

    def sort_by_time(self) -> list[Task]:
        """Return task_list in chronological order by start_time (HH:MM).

        Uses a lambda key that converts 'HH:MM' to (int, int) so comparison is
        numeric, not lexicographic. Tasks with no start_time are appended last.
        """
        timed = [t for t in self.task_list if t.start_time]
        untimed = [t for t in self.task_list if not t.start_time]
        return sorted(timed, key=lambda t: tuple(int(x) for x in t.start_time.split(":"))) + untimed

    def filter_tasks(self, completed: bool | None = None, task_type: str | None = None) -> list[Task]:
        """Return tasks matching the given filters; pass None for a parameter to skip it.

        Filters are applied in sequence (AND logic). Example:
            filter_tasks(completed=False, task_type='Exercise')
            → all pending exercise tasks.
        """
        result = self.task_list
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if task_type is not None:
            result = [t for t in result if t.task_type == task_type]
        return result

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task done and automatically queue its next occurrence if recurring.

        Calls task.mark_complete(), then delegates to task.next_occurrence() for
        daily/weekly tasks and appends the result to task_list. Returns the new
        Task, or None if the task frequency is 'once'.
        """
        task.mark_complete()
        if task.frequency != "once":
            next_task = task.next_occurrence()
            self.task_list.append(next_task)
            return next_task
        return None

    def get_recurring_tasks(self) -> list[Task]:
        """Return tasks that repeat on a daily or weekly schedule."""
        return [t for t in self.task_list if t.frequency != "once"]

    def detect_conflicts(self) -> list[Task]:
        """Return tasks excluded from the daily plan because they exceeded the time budget.

        Must be called after generate_schedule().
        """
        scheduled = set(id(t) for t in self.daily_plan)
        return [t for t in self.prioritize_tasks() if id(t) not in scheduled]

    def detect_time_conflicts(self) -> list[str]:
        """Return warning strings for tasks whose HH:MM time windows overlap; never raises.

        Uses a pairwise O(n²) scan over tasks that have a start_time set. Two tasks
        overlap when A.start < B.end AND B.start < A.end. Tasks without a start_time
        are skipped — they are invisible to this check by design.
        """
        warnings = []
        timed = [t for t in self.task_list if t.start_time]
        for i, a in enumerate(timed):
            for b in timed[i + 1:]:
                a_start = _to_minutes(a.start_time)
                b_start = _to_minutes(b.start_time)
                if a_start < b_start + b.duration and b_start < a_start + a.duration:
                    warnings.append(
                        f"Conflict: '{a.task_name}' ({a.start_time}, {a.duration} min) "
                        f"overlaps '{b.task_name}' ({b.start_time}, {b.duration} min)"
                    )
        return warnings
