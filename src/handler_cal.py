"""
handler_cal.py

This module formats the AI-generated study schedule into a calendar-like layout using Streamlit.
It divides the schedule into two weeks and displays each day with corresponding tasks.
"""

import streamlit as st
import logging
import json

# Generates a calendar view for the AI-generated study schedule.
def gen_cal(output: str) -> None:
    try:
        # Attempt to load the schedule data from JSON
        output = json.loads(output)

        # Validate if expected keys exist in the output
        if "Note" not in output:
            logging.error("Schedule is missing the 'Note' field.")
            st.error("Error: The generated schedule is missing essential information.")
            return

        # Extract dates and tasks (exclude the "Note" key)
        dates = list(output.keys())[:-1]
        week1, week2 = dates[:7], dates[7:14]

        # Create the Streamlit app interface
        st.title("📅 The Tailor's Schedule")

        # Display Week 1
        st.subheader("Week 1")
        cols = st.columns(7)  # Create columns for each day of the week
        for i, day in enumerate(week1):
            with cols[i]:
                st.markdown(f"**{day}**")
                if output.get(day):
                    for task in output[day]:
                        st.write(f"- {task}")
                else:
                    st.write("*No tasks scheduled*")

        # Divider
        st.markdown("---")

        # Display Week 2
        st.subheader("Week 2")
        cols = st.columns(7)
        for i, day in enumerate(week2):
            with cols[i]:
                st.markdown(f"**{day}**")
                if output.get(day):
                    for task in output[day]:
                        st.write(f"- {task}")
                else:
                    st.write("*No tasks scheduled*")

        # Display the note at the bottom of the calendar
        st.markdown("---")
        st.warning(f"📌 **Note:** {output['Note']}")

    except json.JSONDecodeError:
        logging.error("Failed to decode the output as JSON.")
        st.error("Error: The generated schedule could not be decoded properly.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        st.error(f"Error: An unexpected error occurred while generating the schedule.")
