"""
handler_input.py

This module handles user input for upcoming assignments and study habits. 
It provides a form for the user to submit their data, and logs the information.
"""

import streamlit as st
import logging
from config import load_config

# Load the configuration
config = load_config()

# Configure logging based on the config settings
logging.basicConfig(
    filename=config['logging']['log_file'],
    level=config['logging'].get('log_level', 'INFO').upper(),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Handles user input for assignments and study habits. Prompts the user with 
# text areas to input information.
def handle_user_input() -> tuple:
    # Prompt for assignments
    assignments = st.text_area(
        "List your upcoming assignments: [Course], [Assignment Name], [Due Date], [Estimated time]",
        height=150
    )
    
    # Prompt for study habits
    habits = st.text_area(
        "Describe your study habits: Do you tend to procrastinate? Do you do everything in one sitting?",
        height=150
    )

    # Submit button handling
    if st.button("Submit"):
        # Ensure both fields are filled before proceeding
        if assignments and habits:
            st.success("Information successfully submitted!")
            
            # Log the user input for tracking and debugging purposes
            logging.info(f"Assignments: {assignments}")
            logging.info(f"Study Habits: {habits}")

            return assignments, habits
        else:
            st.error("Please fill out both fields.")

    # Return empty strings if the form hasn't been submitted
    return "", ""
