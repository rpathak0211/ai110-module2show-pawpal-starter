from pawpal_system import Owner, Pet, Task, Planner

# --- Create Owner ---
owner = Owner(owner_name="Alex", available_time=60, preferred_schedule="morning")

# --- Create Pets ---
dog = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
cat = Pet(pet_name="Whiskers", pet_type="Cat", age=5, breed="Siamese", special_needs="Indoor only")

# --- Create Tasks and assign to pets ---
dog.add_task(Task(task_name="Morning Walk",    duration=20, priority=3, task_type="Exercise"))
dog.add_task(Task(task_name="Feed Buddy",      duration=10, priority=3, task_type="Feeding"))
cat.add_task(Task(task_name="Clean Litter Box", duration=10, priority=2, task_type="Hygiene"))
cat.add_task(Task(task_name="Playtime",        duration=15, priority=1, task_type="Exercise"))

# --- Register pets with owner ---
owner.add_pet(dog)
owner.add_pet(cat)

# --- Set up Planner and generate schedule ---
planner = Planner(available_time=owner.get_available_time())
planner.load_from_owner(owner)
planner.generate_schedule()

# --- Print Today's Schedule ---
PRIORITY_LABEL = {3: "High", 2: "Medium", 1: "Low"}

print()
print("╔══════════════════════════════════════╗")
print("║         🐾 TODAY'S PAWPAL SCHEDULE   ║")
print("╠══════════════════════════════════════╣")
print(f"║  Owner    : {owner.owner_name:<26}║")
print(f"║  Timing   : {owner.preferred_schedule:<26}║")
print(f"║  Available: {owner.get_available_time()} min{' ' * 22}║")
print("╚══════════════════════════════════════╝")
print()

time_used = 0
for i, task in enumerate(planner.daily_plan, start=1):
    priority_str = PRIORITY_LABEL.get(task.priority, str(task.priority))
    status = "✓ Done" if task.completed else "○ Pending"
    print(f"  {i}. {task.task_name}")
    print(f"     Type: {task.task_type:<12}  Duration: {task.duration} min")
    print(f"     Priority: {priority_str:<9}  Status: {status}")
    print()
    time_used += task.duration

print(f"  Time used: {time_used} / {owner.get_available_time()} min")
