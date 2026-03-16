"""
Task: 

Write a script in main.py that performs the following:
    Imports your classes from pawpal_system.py.
    Creates an Owner and at least two Pets .
    Adds at least three Tasks with different times to those pets.
    Prints a "Today's Schedule" to the terminal.

Run your script: python main.py.

"""

from pawpal_system import *

def main(): 
    # Instantiate pets with preferences
    sir_loin = Pet('sir loin', {"walks": 3, "feeding": 3, "meds": 1, "play": 3, "grooming": 1})

    crispy_bacon = Pet('crispy bacon', {"walks": 1, "feeding": 3, "meds": 1, "play": 2, "grooming": 1})

    # Create time availability 
    availability = [("10:00", "12:00"), ("14:00", "18:00")]

    # Instantiate owner
    jun = Owner('jun', [sir_loin, crispy_bacon], availability, {"walks": 2, "feeding": 2, "meds": 2, "play": 3, "grooming": 1})

    # Instantiate the scheduler
    scheduler = Scheduler(jun)

    # Creates tasks
    task_1 = {"todo": "Walk crispy bacon to the supermarket", "category": "walks", "duration": 60, "scheduled_time": "2026-03-15"}
    task_2 = {"todo": "Feed bacon to crispy bacon", "category": "feeding", "duration": 30, "scheduled_time": "2026-03-15"}
    task_3 = {"todo": "Sizzle Sirloin", "category": "play", "duration": 30, "scheduled_time": "2026-03-15"}

    scheduler.add_task('crispy bacon', **task_1)
    scheduler.add_task('crispy bacon', **task_2)
    scheduler.add_task('sir loin', **task_3)

    # Generate the schedule 
    schedule = scheduler.generate_daily_schedule()
    reason = scheduler.add_reasoning()
    print(schedule)
    print(reason)
    
if __name__ == "__main__": 
    main()