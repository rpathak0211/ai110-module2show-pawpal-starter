import streamlit as st
from pawpal_system import Owner, Pet, Task, Planner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize Owner in session state only once — re-runs won't overwrite it.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_name="Jordan",
        available_time=60,
        preferred_schedule="morning",
    )

owner = st.session_state.owner

st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Section 1: Owner info
# ---------------------------------------------------------------------------
st.subheader("Owner Info")
col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value=owner.owner_name)
with col2:
    available_time = st.number_input("Available time (min)", min_value=5, max_value=480, value=owner.available_time)
with col3:
    preferred_schedule = st.selectbox(
        "Preferred schedule",
        ["morning", "afternoon", "evening"],
        index=["morning", "afternoon", "evening"].index(owner.preferred_schedule),
    )

if st.button("Save owner info"):
    owner.update_preferences(
        owner_name=owner_name,
        available_time=available_time,
        preferred_schedule=preferred_schedule,
    )
    st.success(f"Owner updated: {owner.owner_name}")

st.divider()

# ---------------------------------------------------------------------------
# Section 2: Add a pet → Owner.add_pet(Pet(...))
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    pet_type = st.selectbox("Type", ["Dog", "Cat", "Other"])
with col3:
    breed = st.text_input("Breed", value="Mixed")
with col4:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
special_needs = st.text_input("Special needs (optional)", value="")

if st.button("Add pet"):
    new_pet = Pet(
        pet_name=pet_name,
        pet_type=pet_type,
        age=age,
        breed=breed,
        special_needs=special_needs,
    )
    owner.add_pet(new_pet)   # Owner.add_pet() handles storing the pet
    st.success(f"Added {pet_name} to {owner.owner_name}'s pets!")

if owner.pets:
    st.write("**Current pets:**")
    for pet in owner.pets:
        st.markdown(f"- **{pet.pet_name}** ({pet.pet_type}, {pet.breed}, age {pet.age}) — {len(pet.tasks)} task(s)")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Section 3: Add a task → Pet.add_task(Task(...))
# ---------------------------------------------------------------------------
st.subheader("Add a Task")

PRIORITY_MAP = {"Low": 1, "Medium": 2, "High": 3}

if owner.pets:
    pet_names = [p.pet_name for p in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.pet_name == selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority_label = st.selectbox("Priority", ["Low", "Medium", "High"], index=2)
    with col4:
        task_type = st.selectbox("Type", ["Exercise", "Feeding", "Hygiene", "Enrichment", "Other"])

    if st.button("Add task"):
        new_task = Task(
            task_name=task_name,
            duration=int(duration),
            priority=PRIORITY_MAP[priority_label],
            task_type=task_type,
        )
        selected_pet.add_task(new_task)   # Pet.add_task() appends to pet's task list
        st.success(f"Added '{task_name}' to {selected_pet.pet_name}!")

    if selected_pet.tasks:
        st.write(f"**{selected_pet.pet_name}'s tasks:**")
        rows = [t.get_task_details() for t in selected_pet.tasks]
        st.table(rows)
    else:
        st.info(f"No tasks for {selected_pet.pet_name} yet.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Section 4: Generate schedule → Planner.load_from_owner() + generate_schedule()
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        planner = Planner(available_time=owner.available_time)
        planner.load_from_owner(owner)        # pulls all tasks from owner's pets
        planner.generate_schedule()           # greedy priority-based selection
        st.success("Schedule generated!")
        st.text(planner.explain_plan())       # formatted plan summary
