"""
config.py

This module is responsible for loading and logging configuration settings from 
config.json and other associated files. It also handles loading the AI Constitution.
"""

import json
import logging

# Logs the configuration settings recursively, starting from the top-level structure.
def log_config(config: dict) -> None:
    logging.info("Logging configuration data:")

    # Recursive function to log the config dictionary
    def log_dict(d: dict, prefix: str = '') -> None:
        for key, value in d.items():
            if isinstance(value, dict):  # Recurse into nested dictionaries
                log_dict(value, f"{prefix}{key}.")
            else:
                logging.info(f"{prefix}{key}: {value}")
    
    # Start logging the top-level config dictionary
    log_dict(config)

# Loads the configuration from config.json and logs the configuration data.
def load_config() -> dict:
    try:
        with open('config/config.json', 'r') as f:
            config = json.load(f)
        
        log_config(config)
        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration: {e}")
        raise  # Re-raise the error after logging

# Loads the AI Constitution from the prompts.json file.
def load_const() -> str:
    try:
        with open('./assets/prompts.json', 'r') as file:
            const = json.load(file)
            return const.get('system', "")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading AI Constitution: {e}")
        return ""  # Return empty string on failure
