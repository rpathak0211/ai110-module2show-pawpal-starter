from pawpal_system import Owner, Pet, Task, Planner

# --- Create Owner ---
owner = Owner(owner_name="Alex", available_time=60, preferred_schedule="morning")

# --- Create Pets ---
dog = Pet(pet_name="Buddy", pet_type="Dog", age=3, breed="Labrador")
cat = Pet(pet_name="Whiskers", pet_type="Cat", age=5, breed="Siamese", special_needs="Indoor only")

# --- Create Tasks (added out of order intentionally) ---
dog.add_task(Task(task_name="Evening Walk",    duration=20, priority=2, task_type="Exercise",  start_time="18:00", frequency="daily"))
dog.add_task(Task(task_name="Feed Buddy",      duration=10, priority=3, task_type="Feeding",   start_time="07:30", frequency="daily"))
dog.add_task(Task(task_name="Morning Walk",    duration=20, priority=3, task_type="Exercise",  start_time="07:00", frequency="daily"))
cat.add_task(Task(task_name="Clean Litter Box",duration=10, priority=2, task_type="Hygiene",   start_time="09:00"))
cat.add_task(Task(task_name="Playtime",        duration=15, priority=1, task_type="Exercise",  start_time="11:00"))
cat.add_task(Task(task_name="Vet Checkup",     duration=60, priority=3, task_type="Health",    start_time="14:00", frequency="once"))

# Mark one task done to show filtering
dog.tasks[0].mark_complete()   # Evening Walk is done

# --- Register pets with owner ---
owner.add_pet(dog)
owner.add_pet(cat)

# --- Set up Planner ---
planner = Planner(available_time=owner.get_available_time())
planner.load_from_owner(owner)

# ===========================================================================
# 1. Generate schedule
# ===========================================================================
planner.generate_schedule()

print()
print("╔══════════════════════════════════════╗")
print("║         🐾 TODAY'S PAWPAL SCHEDULE   ║")
print("╠══════════════════════════════════════╣")
print(f"║  Owner    : {owner.owner_name:<26}║")
print(f"║  Timing   : {owner.preferred_schedule:<26}║")
print(f"║  Available: {owner.get_available_time()} min{' ' * 22}║")
print("╚══════════════════════════════════════╝")
print()

PRIORITY_LABEL = {3: "High", 2: "Medium", 1: "Low"}
time_used = 0
for i, task in enumerate(planner.daily_plan, start=1):
    priority_str = PRIORITY_LABEL.get(task.priority, str(task.priority))
    status = "✓ Done" if task.completed else "○ Pending"
    time_label = f"  @ {task.start_time}" if task.start_time else ""
    print(f"  {i}. {task.task_name}{time_label}")
    print(f"     Type: {task.task_type:<12}  Duration: {task.duration} min")
    print(f"     Priority: {priority_str:<9}  Status: {status}")
    print()
    time_used += task.duration

print(f"  Time used: {time_used} / {owner.get_available_time()} min")

# ===========================================================================
# 2. Sort by time (HH:MM) — tasks added out of order, now chronological
# ===========================================================================
print()
print("── Sorted by start_time (chronological) ──")
for task in planner.sort_by_time():
    time_label = task.start_time if task.start_time else "no time set"
    print(f"  {time_label}  {task.task_name} ({task.duration} min)")

# ===========================================================================
# 3. Filter: pending tasks only
# ===========================================================================
print()
print("── Pending tasks only ──")
for task in planner.filter_tasks(completed=False):
    print(f"  ○ {task.task_name}")

# ===========================================================================
# 4. Filter: by pet name
# ===========================================================================
print()
print("── Buddy's tasks only ──")
for task in owner.filter_tasks_by_pet("Buddy"):
    status = "✓" if task.completed else "○"
    print(f"  {status} {task.task_name} ({task.duration} min)")

# ===========================================================================
# 5. Recurring tasks
# ===========================================================================
print()
print("── Recurring tasks ──")
for task in planner.get_recurring_tasks():
    print(f"  [{task.frequency}] {task.task_name}")

# ===========================================================================
# 6. Conflicts — tasks that didn't fit in the time budget
# ===========================================================================
print()
print("── Conflicts (didn't fit in 60 min) ──")
conflicts = planner.detect_conflicts()
if conflicts:
    for task in conflicts:
        print(f"  ✗ {task.task_name} ({task.duration} min) — excluded")
else:
    print("  No conflicts.")

# ===========================================================================
# 7. Recurring task completion — mark done, next occurrence auto-created
# ===========================================================================
print()
print("── Recurring task completion ──")
morning_walk = dog.tasks[2]   # Morning Walk (daily, due today)
morning_walk.edit_task(due_date="2026-06-29")

print(f"  Before: '{morning_walk.task_name}' completed={morning_walk.completed}, due={morning_walk.due_date}")
next_walk = planner.mark_task_complete(morning_walk)
print(f"  After:  '{morning_walk.task_name}' completed={morning_walk.completed}")
if next_walk:
    print(f"  Spawned: '{next_walk.task_name}' due={next_walk.due_date} (tomorrow via timedelta(days=1))")
print(f"  Task list now has {len(planner.task_list)} tasks (was 6)")

# ===========================================================================
# 8. Time conflict detection — two tasks at the same time
# ===========================================================================
print()
print("── Time conflict detection ──")

# Use a fresh planner so accumulated state from section 7 doesn't produce noise.
# Two tasks whose windows deliberately overlap:
#   "Grooming"  starts 09:00, lasts 20 min → occupies 09:00–09:20
#   "Vet Call"  starts 09:10, lasts 15 min → occupies 09:10–09:25  ← overlaps
#   "Feed"      starts 09:30, lasts 10 min → occupies 09:30–09:40  ← no overlap
conflict_planner = Planner(available_time=120)
conflict_planner.add_task(Task(task_name="Grooming", duration=20, priority=2,
                               task_type="Hygiene", start_time="09:00"))
conflict_planner.add_task(Task(task_name="Vet Call",  duration=15, priority=3,
                               task_type="Health",  start_time="09:10"))
conflict_planner.add_task(Task(task_name="Feed",      duration=10, priority=3,
                               task_type="Feeding", start_time="09:30"))

time_warnings = conflict_planner.detect_time_conflicts()
if time_warnings:
    for warning in time_warnings:
        print(f"  ⚠ {warning}")
else:
    print("  No time conflicts found.")
print()
