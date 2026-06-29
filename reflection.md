# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
->My initial UML design focused on separating pet information, task management, and schedule generation into different classes to keep the application modular and easy to maintain.
- What classes did you include, and what responsibilities did you assign to each?
->The classes are as follows:

Pet – Stores information about the pet such as name, type, age, and any preferences or special care requirements.
Task – Represents an individual care activity (feeding, walk, medication, grooming, etc.). Each task contains details such as task name, duration, priority, and completion status.
Owner – Stores owner information and preferences, including available time for pet care.
Planner (or ScheduleManager) – Responsible for generating a daily care schedule by organizing tasks based on constraints such as available time and task priority.
Streamlit UI – Handles user interaction by collecting inputs and displaying the generated care plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
->Yes, my design changed during implementation.
->The original skeletons defined the right methods but neither Pet had a tasks list nor did Owner have a pets list. The UML showed the arrows (Owner --> Pet, Pet --> Task) but the code had nothing to back them up.

<!-- Initially, I planned to keep scheduling logic inside the Task class, but this made the class responsible for too many operations. During implementation, I moved scheduling functionality into a separate Planner (or ScheduleManager) class.

This change improved code organization, made testing easier, and allowed task objects to remain focused only on storing task information while the planner handled decision-making and schedule generation. -->

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two constraints: **available time** (the owner's daily time budget in minutes) and **task priority** (1 = low, 2 = medium, 3 = high). Priority was chosen as the primary ordering because a pet owner's most critical tasks — feeding, medication — must happen regardless of how long they take, so sorting by priority first ensures those are always attempted before optional tasks like playtime or grooming.

Time is the hard constraint: no task is added to the plan if it would exceed the remaining budget. This is enforced greedily — the scheduler scans tasks in priority order and takes each one that fits, skipping those that don't and continuing to check smaller tasks that might still fit.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Greedy priority ordering vs. optimal packing (knapsack)**

The scheduler uses a greedy algorithm: it picks tasks in descending priority order and takes each one that fits within the remaining time. This is fast (O(n log n) — one sort, one scan) and predictable, but it does not guarantee the maximum number of tasks or maximum time utilization.

*Example of the gap:* with 30 minutes available and tasks [25 min priority-3, 10 min priority-2, 10 min priority-2], the greedy scheduler picks the 25-min task first (correct — it's highest priority), leaving only 5 min, so both 10-min tasks are skipped. An optimal knapsack solver would pick the two 10-min tasks instead (20 min used, 2 tasks completed vs. 1). But knapsack is NP-hard and exponentially slower for large task lists, which is overkill for a daily pet care app.

This tradeoff is reasonable here because: (1) task priority reflects real urgency — a pet's medication outranks a grooming session even if it costs more time, (2) the owner sets the priorities, so the output is explainable ("I scheduled your high-priority tasks first"), and (3) most real task lists are short enough that the greedy result is nearly optimal anyway.

A second tradeoff: `detect_time_conflicts()` only inspects tasks that have a `start_time` set. Tasks without a wall-clock time are invisible to conflict detection, so two untimed tasks can coexist in the plan even if a human would schedule them at the same time. This was a deliberate simplification — forcing every task to have a start time would add friction to the UI for tasks where timing doesn't matter (e.g., "give treats").

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
