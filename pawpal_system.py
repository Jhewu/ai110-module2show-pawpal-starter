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
    def __init__(self, name: str, preferences: dict):
        self.name = name
        if preferences is None:
            self.preferences = {"walks": 3, "feeding": 2, "meds": 1, "play": 3, "grooming": 2}
        else:
            self.preferences = preferences

        # tasks belonging to this pet
        self.tasks: List[Task] = []

    def add_task(self, **kwargs) -> Task:
        """Create a Task from kwargs, auto-set priority from pet preferences, and add it to this pet's list."""
        task = Task()
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.priority = self.preferences.get(task.category, 2)
        self.tasks.append(task)
        return task

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

class Owner:
    def __init__(self, name: str, pets: List[Pet], time_availability: List[tuple], preferences: dict):
        self.name = name

        # all pets this owner manages
        self.pets = pets

        # e.g., [("09:00", "12:00"), ("15:00", "18:00")] in 24-hour time
        self.time_availability = time_availability

        if preferences is None:
            self.preferences = {"walks": 1, "feeding": 2, "meds": 3, "play": 2, "grooming": 2}
        else:
            self.preferences = preferences

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        output = []
        for pet in self.pets: 
            output.extend(pet.get_tasks())
        return output

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

        # maps task_id (int) -> Task, aggregated across all pets
        self.task_dict = {}

        self._next_id = 1 # internal

    def add_task(self, task: Task) -> int:
        """Add a new task to the schedule and return its assigned ID."""

        if self._next_id == 1000: 
            self._next_id = 1 # Reset if it's 1,000 

        while self._next_id in self.task_dict: 
            self._next_id+=1

        self.task_dict[self._next_id] = task
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def remove_task(self, task_id: int) -> int:
        """Remove a task by its ID and return the ID."""
        self.task_dict.pop(task_id)
        return task_id

    def edit_task(self, task_id: int, **kwargs) -> None:
        """Edit a specific task's fields by its ID."""
        task = self.task_dict[task_id]
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

        tasks = list(self.task_dict.values())
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
        pass
