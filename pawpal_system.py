from typing import List

"""
> Run main.py demo
> Main.py implementation should include One owner, two pets, at least 3 tasks, and testing scheduler.
> Trace data flow across classes
> Verify task creation and retrieval
> Inspect at least one class method carefully




"""

class Task:
    def __init__(self):
        self.todo = ""
        self.category = ""        # "walks", "feeding", "meds", "play", "grooming"
        self.priority = 2         # 1 (low) to 3 (high); set by Pet.add_task()
        self.duration = 0         # in minutes
        self.scheduled_time = ""  # e.g., "2026-03-15"
        self.frequency = "once"   # "daily", "weekly", "once"
        self.completed = False

class Pet:
    def __init__(self, name: str, preferences: dict = None):
        self.name = name
        if preferences is None:
            self.preferences = {"walks": 3, "feeding": 2, "meds": 1, "play": 3, "grooming": 2}
        else:
            self.preferences = preferences

        # tasks belonging to this pet
        self.tasks: List[Task] = []

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

class Owner:
    def __init__(self, name: str, pets: List[Pet] = [], time_availability: List[tuple] = [], preferences: dict = None):
        self.name = name

        # all pets this owner manages
        self.pets = pets

        # e.g., [("09:00", "12:00"), ("15:00", "18:00")] in 24-hour time
        self.time_availability = time_availability

        if preferences is None:
            self.preferences = {"walks": 1, "feeding": 2, "meds": 3, "play": 2, "grooming": 2}
        else:
            self.preferences = preferences

    def add_pets(self, pet: Pet): 
        """Append pet to Owner list"""
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        output = []
        for pet in self.pets: 
            output.extend(pet.get_tasks())
        return output

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

        # maps task_id (int) -> (Task, pet), aggregated across all pets
        self.task_dict = {}

        self._next_id = 1 # internal

    def add_task(self, pet_name: str, **kwargs) -> int:
        """
        Create a Task for a pet by name, auto-set priority from that pet's preferences,
        store it on the pet and in task_dict, and return the assigned task ID.    
        """
        pet = next(p for p in self.owner.pets if p.name == pet_name)

        task = Task()
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.priority = pet.preferences.get(task.category, 2)
        pet.tasks.append(task)

        if self._next_id == 1000:
            self._next_id = 1
        while self._next_id in self.task_dict:
            self._next_id += 1

        self.task_dict[self._next_id] = (task, pet)
        task_id = self._next_id
        self._next_id += 1
        return task_id
    
    def mark_as_complete(self, task_id: int) -> bool: 
        """
        Utilizes self.edit_task() to mark as complete. 
        Returns True
        """
        self.edit_task(task_id, completed=True)
        return True

    def remove_task(self, task_id: int) -> int:
        """Remove a task by its ID and return the ID."""
        task = self.task_dict.pop(task_id)[0]
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.tasks.remove(task)
                break
        return task_id
    
    def edit_task(self, task_id: int, **kwargs) -> None:
        """Edit a specific task's fields by its ID."""
        task = self.task_dict[task_id][0]
        for key, value in kwargs.items():
            setattr(task, key, value)

    def get_tasks_for_pet(self, pet: Pet) -> List[Task]:
        """Retrieve all scheduled tasks belonging to a specific pet."""
        return pet.get_tasks()

    def generate_daily_schedule(self) -> List[tuple]:
        """Generate and return a daily schedule based on constraints and priorities.

        Returns a list of (time_str, Task) tuples fitted within the owner's
        time_availability windows, ordered by priority and preferences.
        e.g., [("09:00", <Task>), ("09:30", <Task>), ...]
        """
        # Greedy + 0-1 Knapsack approach:
        # Phase 1 (Knapsack DP): select which tasks to include, maximizing
        #   value = task.priority + owner.preferences[category] within total window minutes.
        # Phase 2 (greedy slot): sort selected tasks by score desc, then slot
        #   them into time windows in order.

        tasks = [t for t, _ in self.task_dict.values()]
        if not tasks or not self.owner.time_availability:
            return []

        def to_minutes(t):
            h, m = map(int, t.split(":"))
            return h * 60 + m

        def to_time_str(mins):
            return f"{mins // 60:02d}:{mins % 60:02d}"

        def score(task):
            pref = self.owner.preferences.get(task.category, 1)
            return task.priority + pref

        windows = [(to_minutes(s), to_minutes(e))
                   for s, e in self.owner.time_availability]
        W = sum(e - s for s, e in windows)

        # --- 0-1 Knapsack DP ---
        # dp[i][cap] = max total score using the first i tasks with cap minutes available
        n = len(tasks)
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        for i, task in enumerate(tasks, 1):
            w, v = task.duration, score(task)
            for cap in range(W + 1):
                dp[i][cap] = dp[i - 1][cap]
                if cap >= w:
                    dp[i][cap] = max(dp[i][cap], dp[i - 1][cap - w] + v)

        # Backtrack to find which tasks were selected
        selected, cap = [], W
        for i in range(n, 0, -1):
            if dp[i][cap] != dp[i - 1][cap]:
                selected.append(tasks[i - 1])
                cap -= tasks[i - 1].duration
        selected.sort(key=score, reverse=True)

        # --- Slot tasks into time windows greedily (highest score first) ---
        schedule = []
        win_idx = 0
        cur = windows[0][0]
        for task in selected:
            while win_idx < len(windows):
                win_s, win_e = windows[win_idx]
                cur = max(cur, win_s)
                if cur + task.duration <= win_e:
                    schedule.append((to_time_str(cur), task))
                    cur += task.duration
                    break
                win_idx += 1
                if win_idx < len(windows):
                    cur = windows[win_idx][0]
            else:
                break  # No remaining windows fit this task

        return schedule

    def add_reasoning(self) -> str:
        """Return a plain-English explanation of why tasks were scheduled as they were."""
        schedule = self.generate_daily_schedule()
        scheduled_ids = {id(t) for _, t in schedule}

        def score(task):
            pref = self.owner.preferences.get(task.category, 1)
            return task.priority + pref

        total_window = sum(
            (int(e.split(":")[0]) * 60 + int(e.split(":")[1])) -
            (int(s.split(":")[0]) * 60 + int(s.split(":")[1]))
            for s, e in self.owner.time_availability
        )

        lines = [
            f"Schedule optimizes for the highest combined score "
            f"(task priority + owner preference) within {total_window} available minutes.\n"
        ]

        if schedule:
            lines.append("Scheduled tasks (highest score first):")
            for time_str, task in schedule:
                pref = self.owner.preferences.get(task.category, 1)
                lines.append(
                    f"  {time_str} — {task.todo!r} | category: {task.category} | "
                    f"priority {task.priority} + owner pref {pref} = score {score(task)} | "
                    f"{task.duration} min"
                )
        else:
            lines.append("No tasks could be scheduled.")

        excluded = [t for t, _ in self.task_dict.values() if id(t) not in scheduled_ids]
        if excluded:
            lines.append("\nExcluded tasks (did not fit or were outscored):")
            for task in excluded:
                lines.append(
                    f"  {task.todo!r} | score {score(task)} | {task.duration} min — "
                    f"excluded due to time constraints or lower priority score"
                )

        return "\n".join(lines)
