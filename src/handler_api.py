"""
handler_api.py

This module handles API interactions for generating responses using a language model. 
It includes functions for generating study schedules and querying the model with user data.
"""

from config import load_config, load_const
from llmproxy import generate
from datetime import datetime
import logging

# Generates a response from the language model based on the query provided.
def gen(query: str) -> dict:
    try:
        config = load_config()  # Load configuration settings
        response = generate(
            model=config["llm"]["default_model"],
            system=load_const(),
            query=query,
            temperature=config["llm"]["temperature"],
            lastk=config["llm"]["lastk"],
            session_id=config["llm"]["session_id"]
        )
        logging.info("Generated response successfully.")
        return response
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return {"error": str(e)}  # Return an error message if generation fails

# Generates a study schedule based on the user's assignments and study habits.
def gen_schedule(assignments: str, habits: str) -> dict:
    # Get current date in a readable format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Construct the query to the model for generating the schedule
    query = f"""
    Create a study schedule for the TailoredTasks AI user given the following information:
    Current date: {current_date}

    User's Upcoming Assignments: {assignments}

    User's Study Habits: {habits}

    Given the upcoming assignments and study habits above, create a study schedule for the next two weeks.
    Respond with a table that looks like a calendar. Input the user's upcoming assignments into the table you provide.
    Do not create or hallucinate assignments to do. If none are provided, then the schedule should be empty.
    If any are provided, use your best judgement to place them in the schedule.
    """
    
    logging.info("Generating study schedule...")
    response = gen(query)  # Call gen() to generate the response
    return response
