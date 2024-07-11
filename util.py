# genetic_algorithm\util.py
import os
import json
import logging

def get_working_directory():
    scan_file = "requirements.txt"
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)

    if os.path.exists(os.path.join(current_directory, scan_file)):
        working_directory = current_directory
        return working_directory
    elif os.path.exists(os.path.join(parent_directory, scan_file)):
        working_directory = parent_directory
        return working_directory
    else:
        raise FileNotFoundError(f"Cannot determine the working directory because {scan_file} was not found in the current or the parent directory.")
    
def setup_logging(script_name):
    working_directory = get_working_directory()
    log_directory = os.path.join(working_directory, "log")
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, f"{script_name}.log")
    with open(log_file, "w"):
        pass

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(script_name)
    logger.info(f"Logging initialized for {script_name}")

    return logger

def get_parameter(parameter_key):
    working_directory = get_working_directory()
    parameters_filepath = os.path.join(working_directory, "parameters.json")
    with open(parameters_filepath, "r") as parameters_file:
        parameters = json.load(parameters_file)

    parameter = parameters[parameter_key]
    return parameter

def write_parameter(parameter_key, parameter_new_value):
    working_directory = get_working_directory()
    parameters_filepath = os.path.join(working_directory, "parameters.json")
    with open(parameters_filepath, "r") as parameters_file:
        parameters = json.load(parameters_file)

    parameters[parameter_key] = parameter_new_value
    
    with open(parameters_filepath, "w") as parameters_file:
        json.dump(parameters, parameters_file, indent=4)