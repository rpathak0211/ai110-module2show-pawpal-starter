# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run `python main.py` to generate a schedule from the demo data:

```
╔══════════════════════════════════════╗
║         🐾 TODAY'S PAWPAL SCHEDULE   ║
╠══════════════════════════════════════╣
║  Owner    : Alex                     ║
║  Timing   : morning                  ║
║  Available: 60 min                   ║
╚══════════════════════════════════════╝

  1. Morning Walk
     Type: Exercise      Duration: 20 min
     Priority: High       Status: ○ Pending

  2. Feed Buddy
     Type: Feeding       Duration: 10 min
     Priority: High       Status: ○ Pending

  3. Clean Litter Box
     Type: Hygiene       Duration: 10 min
     Priority: Medium     Status: ○ Pending

  4. Playtime
     Type: Exercise      Duration: 15 min
     Priority: Low        Status: ○ Pending

  Time used: 55 / 60 min
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority | `Planner.prioritize_tasks()` | Sorts pending tasks descending by priority (3 = high). Used internally by `generate_schedule()` to decide order. |
| Sort by duration | `Planner.sort_by_duration(ascending)` | Returns task list sorted shortest- or longest-first without mutating it. Useful for packing the most tasks into a tight schedule. |
| Sort by time | `Planner.sort_by_time()` | Sorts tasks chronologically by `start_time` ("HH:MM") using a numeric lambda key; tasks with no start time are appended last. |
| Filter by status | `Planner.filter_tasks(completed=...)` | Returns only pending or only completed tasks. Filters can be combined (AND logic) with `task_type`. |
| Filter by pet | `Owner.filter_tasks_by_pet(pet_name)` | Returns all tasks belonging to a specific pet by name. |
| Recurring tasks | `Task.next_occurrence()` | Creates a new Task instance for the next daily (`+1 day`) or weekly (`+7 days`) occurrence using Python's `timedelta`. |
| Auto-queue recurrence | `Planner.mark_task_complete(task)` | Marks a task done and automatically appends its next occurrence to `task_list` if `frequency != "once"`. |
| Budget conflict detection | `Planner.detect_conflicts()` | Returns tasks excluded from the daily plan because they exceeded the remaining time budget. Must be called after `generate_schedule()`. |
| Time-overlap detection | `Planner.detect_time_conflicts()` | Pairwise O(n²) scan over timed tasks; returns human-readable warning strings for any overlapping HH:MM windows. Never raises — returns an empty list when there are no conflicts. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
