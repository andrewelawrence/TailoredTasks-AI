"""
app.py

This module initializes and runs the Streamlit web application. 
It handles configuration loading, user input, schedule generation, 
and renders the HTML/CSS content dynamically.
"""
import logging
import json
from datetime import datetime, timedelta

import streamlit as st
from config import load_config
from handler_api import gen_schedule
from handler_cal import gen_cal
from handler_input import handle_user_input

# Load configuration
config = load_config()

# Configure logging
log_level = config.get("logging", {}).get("log_level", "INFO").upper()
log_file = config.get("logging", {}).get("log_file", "./logs/app.log")
logging.basicConfig(filename=log_file, level=log_level)
logging.info(f"Logging initialized with level: {log_level}, log file: {log_file}")

# Streamlit configuration
st.set_page_config(page_title="TailoredTasks AI", 
                   page_icon="assets/favicons/icons8-ai-ios-17-filled-96.png", 
                   layout="wide",
                   menu_items=None)

# Load HTML and CSS content dynamically from configuration
html_path = config.get("style", {}).get("html_content", "./src/page.html")
css_path = config.get("style", {}).get("css_style", "./src/style.css")

# Helper function to safely load files
def load_file_content(file_path: str, file_type: str) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"{file_type} file not found at: {file_path}")
        st.error(f"Error: {file_type} file not found at {file_path}.")
    except Exception as e:
        logging.error(f"Failed to load {file_type} file: {e}")
        st.error(f"Error loading {file_type} file. Check logs for details.")
    return ""

# Load and render HTML content
page_html = load_file_content(html_path, "HTML")
if page_html:
    st.markdown(page_html, unsafe_allow_html=True)

# Load and render CSS content
page_css = load_file_content(css_path, "CSS")
if page_css:
    st.markdown(f"<style>{page_css}</style>", unsafe_allow_html=True)

# Load and handle user input
assignments, habits = handle_user_input()

# Generate schedule and calendar if inputs are provided
if assignments and habits:
    st.subheader("Generating your schedule, please wait...")
    try:
        generated_schedule = gen_schedule(assignments, habits)
        gen_cal(generated_schedule)
    except Exception as e:
        logging.error(f"Error generating schedule or calendar: {e}")
        st.error("An error occurred while generating the schedule. Check logs for details.")
