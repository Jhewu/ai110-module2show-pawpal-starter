from pawpal_system import *

"""
# TODO: IMPLEMENT THESE INTO THE SYSTEM
Use the Generate tests smart action or Copilot Chat to draft two simple tests:

    Task Completion: Verify that calling mark_complete() actually changes the task's status.
    Task Addition: Verify that adding a task to a Pet increases that pet's task count.

"""

import pytest


@pytest.fixture
def scheduler():
    pet = Pet(name="Buddy", preferences={"walks": 3, "feeding": 2, "meds": 1, "play": 3, "grooming": 2})
    owner = Owner(
        name="Alex",
        pets=[pet],
        time_availability=[("09:00", "12:00")],
        preferences={"walks": 2, "feeding": 2, "meds": 3, "play": 1, "grooming": 1},
    )
    return Scheduler(owner=owner)


def test_mark_as_complete_sets_completed_true(scheduler):
    """mark_as_complete() should flip task.completed from False to True."""
    task_id = scheduler.add_task(
        "Buddy",
        todo="Morning walk",
        category="walks",
        duration=30,
        scheduled_time="2026-03-15",
        frequency="daily",
    )
    task = scheduler.task_dict[task_id][0]
    assert task.completed is False
    scheduler.mark_as_complete(task_id)
    assert task.completed is True


def test_add_task_increases_pet_task_count(scheduler):
    """add_task() should increase the pet's task list length by one per call."""
    pet = scheduler.owner.pets[0]
    before = len(pet.tasks)
    scheduler.add_task(
        "Buddy",
        todo="Feed dinner",
        category="feeding",
        duration=15,
        scheduled_time="2026-03-15",
        frequency="daily",
    )
    assert len(pet.tasks) == before + 1
