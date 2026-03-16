from typing import List


class Pet:
    def __init__(self, name: str, preferences: dict):
        self.name = name
        # e.g., {"walks": 3, "feeding": 2, "meds": 1, "play": 3, "grooming": 2}
        self.preferences = preferences


class Owner:
    def __init__(self, name: str, owner_of: Pet, time_availability: List[tuple], preferences: dict):
        self.name = name
        self.owner_of = owner_of
        # e.g., [("09:00", "12:00"), ("15:00", "18:00")] in 24-hour time
        self.time_availability = time_availability
        # e.g., {"walks": 3, "feeding": 2, "meds": 1, "play": 3, "grooming": 2}
        self.preferences = preferences


class Task:
    def __init__(self, title: str, description: str, category: str, priority: int, duration: int, scheduled_time: str):
        self.title = title
        self.description = description
        # matches preference keys: "walks", "feeding", "meds", "play", "grooming"
        self.category = category
        # 1 (low) to 3 (high)
        self.priority = priority
        # duration in minutes
        self.duration = duration
        # the date it's scheduled, e.g., "2026-03-15"
        self.scheduled_time = scheduled_time


class Scheduler:
    def __init__(self, assigned_to: Owner):
        self.assigned_to = assigned_to
        # maps task_id (int) -> Task
        self.task_dict = {}
        self._next_id = 1

    def add_task(self, task: Task) -> int:
        """Add a new task to the schedule and return its assigned ID."""
        pass

    def remove_task(self, task_id: int) -> int:
        """Remove a task by its ID and return the ID."""
        pass

    def edit_task(self, task_id: int, **kwargs) -> None:
        """Edit a specific task's fields by its ID."""
        pass

    def generate_daily_schedule(self) -> List[tuple]:
        """Generate and return a daily schedule based on constraints and priorities.

        Returns a list of (time_str, Task) tuples fitted within the owner's
        time_availability windows, ordered by priority and preferences.
        e.g., [("09:00", <Task>), ("09:30", <Task>), ...]
        """
        pass

    def add_reasoning(self) -> str:
        """Return a plain-English explanation of why tasks were scheduled as they were."""
        pass
