from datetime import datetime
import streamlit as st
from pawpal_system import Owner, Scheduler, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="John")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

# --- Owner section ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jun")

if st.button("Set owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.scheduler = Scheduler(st.session_state.owner)
    st.success(f"Owner set to **{owner_name}**")

if st.session_state.owner:
    st.info(f"Current owner: **{st.session_state.owner.name}**")

st.subheader("Time Availability")

if not st.session_state.owner.time_availability:
    st.session_state.owner.time_availability = [("09:00", "17:00")]

col_start, col_end = st.columns(2)
with col_start:
    new_start = st.time_input("Start", value=datetime.strptime("09:00", "%H:%M").time(), key="new_start")
with col_end:
    new_end = st.time_input("End", value=datetime.strptime("17:00", "%H:%M").time(), key="new_end")

if st.button("+ Add Window"):
    st.session_state.owner.time_availability.append((
        new_start.strftime("%H:%M"),
        new_end.strftime("%H:%M")
    ))
    st.rerun()

if st.session_state.owner.time_availability:
    st.markdown("**Current availability:**")
    for i, (s, e) in enumerate(st.session_state.owner.time_availability):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{s} → {e}**")
        with col2:
            if st.button("Remove", key=f"remove_window_{i}"):
                st.session_state.owner.time_availability.pop(i)
                st.rerun()
else:
    st.caption("No time windows set.")

st.divider()

# --- Pet section ---
st.subheader("Pets")
pet_name = st.text_input("Pet name", value="Sir Loin")

if st.button("Add pet"):
    if pet_name in st.session_state.owner.pets:
        st.warning(f"**{pet_name}** already exists — updating species.")
    st.session_state.owner.add_pets(Pet(name=pet_name))
    st.success(f"Added **{pet_name}** to **{owner_name}**")

if st.session_state.owner and len(st.session_state.owner.pets) > 0:
    st.write("Current pets:")
    for i, pet in enumerate(st.session_state.owner.pets):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{pet.name}**")
        with col2:
            if st.button("Remove", key=f"remove_pet_{i}"):
                st.session_state.owner.pets.pop(i)
                st.rerun()
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    pet_selected = st.selectbox("Pets", [pet.name for pet in st.session_state.owner.pets])
with col3:
    task_category = st.selectbox("Category", ["walks", "feeding", "meds", "play", "grooming"], index=2)
with col4:  
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

if st.button("Add task"):
    st.session_state.scheduler.add_task(pet_selected, todo=task_title, duration=duration, category=task_category)

if st.session_state.scheduler.task_dict:
    st.write("Current tasks:")
    extracted_todo = [element[0].todo for element in st.session_state.scheduler.task_dict.values()]
    st.table(extracted_todo)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    schedule = st.session_state.scheduler.generate_daily_schedule()
    if schedule:
        st.table([
            {
                "Time": time_str,
                "Task": task.todo,
                "Category": task.category,
                "Duration (min)": task.duration,
                "Priority": task.priority,
            }
            for time_str, task in schedule
        ])
        with st.expander("Why was this schedule chosen?"):
            st.text(st.session_state.scheduler.add_reasoning())
    else:
        st.warning("No tasks could be scheduled. Check that tasks and time windows are set.")
