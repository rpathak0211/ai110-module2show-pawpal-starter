import pytest
from pawpal_system import Task, Pet, Owner, Planner


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

def test_task_defaults():
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    assert task.completed is False

def test_task_mark_complete():
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    task.mark_complete()
    assert task.completed is True

def test_task_edit():
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    task.edit_task(duration=30, priority=2)
    assert task.duration == 30
    assert task.priority == 2

def test_task_get_details():
    task = Task(task_name="Feed", duration=10, priority=3, task_type="Feeding")
    details = task.get_task_details()
    assert details["task_name"] == "Feed"
    assert details["duration"] == 10
    assert details["priority"] == 3
    assert details["completed"] is False


# ---------------------------------------------------------------------------
# Pet tests
# ---------------------------------------------------------------------------

def test_pet_add_task():
    pet = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    pet.add_task(task)
    assert task in pet.tasks

def test_pet_remove_task():
    pet = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    pet.add_task(task)
    pet.remove_task(task)
    assert task not in pet.tasks

def test_pet_display_info():
    pet = Pet(pet_name="Whiskers", pet_type="Cat", age=5, breed="Siamese", special_needs="Indoor only")
    info = pet.display_pet_info()
    assert "Whiskers" in info
    assert "Siamese" in info
    assert "Indoor only" in info

def test_pet_update_info():
    pet = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    pet.update_info(age=4, breed="Golden Retriever")
    assert pet.age == 4
    assert pet.breed == "Golden Retriever"


# ---------------------------------------------------------------------------
# Owner tests
# ---------------------------------------------------------------------------

def test_owner_add_pet():
    owner = Owner(owner_name="Alex", available_time=60, preferred_schedule="morning")
    pet = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    owner.add_pet(pet)
    assert pet in owner.pets

def test_owner_remove_pet():
    owner = Owner(owner_name="Alex", available_time=60, preferred_schedule="morning")
    pet = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    owner.add_pet(pet)
    owner.remove_pet(pet)
    assert pet not in owner.pets

def test_owner_get_all_tasks():
    owner = Owner(owner_name="Alex", available_time=60, preferred_schedule="morning")
    dog = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    cat = Pet(pet_name="Whiskers", pet_type="Cat", age=5, breed="Siamese")
    t1 = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    t2 = Task(task_name="Feed", duration=10, priority=3, task_type="Feeding")
    dog.add_task(t1)
    cat.add_task(t2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    all_tasks = owner.get_all_tasks()
    assert t1 in all_tasks
    assert t2 in all_tasks
    assert len(all_tasks) == 2

def test_owner_get_available_time():
    owner = Owner(owner_name="Alex", available_time=90, preferred_schedule="evening")
    assert owner.get_available_time() == 90


# ---------------------------------------------------------------------------
# Planner tests
# ---------------------------------------------------------------------------

def test_planner_prioritize_tasks():
    planner = Planner(available_time=60)
    low = Task(task_name="Play", duration=15, priority=1, task_type="Exercise")
    high = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    mid = Task(task_name="Feed", duration=10, priority=2, task_type="Feeding")
    planner.add_task(low)
    planner.add_task(high)
    planner.add_task(mid)
    ordered = planner.prioritize_tasks()
    assert ordered[0].priority == 3
    assert ordered[1].priority == 2
    assert ordered[2].priority == 1

def test_planner_skips_completed_tasks():
    planner = Planner(available_time=60)
    done = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    done.mark_complete()
    pending = Task(task_name="Feed", duration=10, priority=2, task_type="Feeding")
    planner.add_task(done)
    planner.add_task(pending)
    ordered = planner.prioritize_tasks()
    assert done not in ordered
    assert pending in ordered

def test_planner_generate_schedule_fits_time():
    planner = Planner(available_time=30)
    t1 = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    t2 = Task(task_name="Feed", duration=10, priority=3, task_type="Feeding")
    t3 = Task(task_name="Play", duration=15, priority=1, task_type="Exercise")
    planner.add_task(t1)
    planner.add_task(t2)
    planner.add_task(t3)
    schedule = planner.generate_schedule()
    total = sum(t.duration for t in schedule)
    assert total <= 30

def test_planner_generate_schedule_drops_tasks_that_dont_fit():
    planner = Planner(available_time=20)
    big = Task(task_name="Long Walk", duration=30, priority=3, task_type="Exercise")
    small = Task(task_name="Feed", duration=10, priority=2, task_type="Feeding")
    planner.add_task(big)
    planner.add_task(small)
    schedule = planner.generate_schedule()
    assert big not in schedule
    assert small in schedule

def test_planner_load_from_owner():
    owner = Owner(owner_name="Alex", available_time=45, preferred_schedule="morning")
    dog = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    dog.add_task(task)
    owner.add_pet(dog)
    planner = Planner(available_time=0)
    planner.load_from_owner(owner)
    assert task in planner.task_list
    assert planner.available_time == 45

def test_planner_explain_plan_no_schedule():
    planner = Planner(available_time=60)
    result = planner.explain_plan()
    assert "generate_schedule" in result

def test_planner_explain_plan_after_schedule():
    planner = Planner(available_time=60)
    task = Task(task_name="Walk", duration=20, priority=3, task_type="Exercise")
    planner.add_task(task)
    planner.generate_schedule()
    result = planner.explain_plan()
    assert "Walk" in result
    assert "20" in result
