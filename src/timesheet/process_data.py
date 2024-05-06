"""
Uploading and extracting relevant timesheet information from input data
"""

import argparse
import os 
import sys
import re
from typing import List, Tuple, Mapping

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))   # locate root dir
sys.path.append(parent_dir)

from constants import *
from src.timesheet.services import SLPService


def process_event(line: str) -> SLPService:
    """
    Processes a single line of a weekly log, converting it into an SLPService object.

    Args:
        line (str): A single log line of form "Week {week number} ({week day}) {start time} - {end time} : {indirect/direct} {category}"
                    e.g. "Week 1 (Thursday) 9:30 AM - 11:30 AM : direct language"

    Returns:
        SLPService: custom object possessing details about the event
    """
    # Extracting fields using regex
    match = re.match(REGEX_PATTERN, line)

    if match:
        # Extracting captured groups
        week_number = match.group(1)
        week_day = match.group(2)
        start_time = match.group(3)
        end_time = match.group(4)
        direct = match.group(5)
        category = match.group(6)

        # Need task type, start time, end time
        start_time_obj = datetime.strptime(start_time, "%I:%M %p").time()
        end_time_obj = datetime.strptime(end_time, "%I:%M %p").time()
        start_datetime = datetime.combine(DUMMY_DATE, start_time_obj)
        end_datetime = datetime.combine(DUMMY_DATE, end_time_obj)
        task_type = category.lower()

        return SLPService(task_type, start_datetime, end_datetime)


    else:
        raise ValueError(f"Could not match input to regex pattern. Input: {line}")


def process_doc(filename: str, save_name: str = "", verbose=False) -> Mapping[str, Mapping[str, float]]:
    """
    Process a document file containing a week's worth of recorded fieldwork activity

    File is expected to be of form 'Week {week number} ({week day}) {start time} - {end time} : {indirect/direct} {category}' on each line

    Args:
        filename (str): Path to document file
        save_name (str, optional): Path to save file for map

    Returns (Mapping[str, Mapping[str, float]]): A map between the category of service as well as the number of hours for that week on the task.
    """
    
    service_to_hours = {
        "direct": {task_name : 0.0 for task_name in DIRECT_SERVICES},
        "indirect": {task_name : 0.0 for task_name in INDIRECT_SERVICES}
    }

    with open(filename, "r+") as f:
        events = f.readlines()
        for event in events:
            service = process_event(event)
            direct_or_indirect = "direct" if service.direct_service else "indirect"
            service_to_hours[direct_or_indirect][service.task_type] += service.get_duration()
    
    if verbose:
        with open(save_name, "w+") as outf:
            headline = "================DIRECT SERVICES================\n"
            print(headline)
            outf.write(headline)

            for task, duration in sorted((service_to_hours.get('direct', [])).items()):
                task_msg = f"Task: {task}   Duration for the week: {duration} hours.\n"
                print(task_msg)
                outf.write(task_msg)

            direct_hours_total = sum(service_to_hours.get("direct", []).values())
            direct_hrs_msg = f"Total direct hours for week : {direct_hours_total}\n"
            print(direct_hrs_msg)

            headline = "================INDIRECT SERVICES================\n"
            print(headline)
            outf.write(headline)
            for task, duration in sorted(service_to_hours.get('indirect', []).items()):
                task_msg = f"Task: {task}   Duration for the week: {duration} hours.\n"
                print(task_msg)
                outf.write(task_msg)

            indirect_hour_total = sum(service_to_hours.get("indirect", []).values())
            indirect_hrs_msg = f"Total indirect hours for week : {indirect_hour_total}\n"
            print(indirect_hrs_msg)
            outf.write(indirect_hrs_msg)
            
            total_hrs_msg = f"Total hours for the week : {direct_hours_total + indirect_hour_total}"
            print(total_hrs_msg)
            outf.write(total_hrs_msg)
    
    return service_to_hours


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", type=str, default=os.path.join(os.path.dirname(__file__), 'data', "week8.txt"), help="Path to file containing time logs.")
    parser.add_argument("--log_regex", type=str, default=REGEX_PATTERN, help="Regex pattern to extract fields with")  # TODO expand on this
    parser.add_argument("--save_name", type=str, default=os.path.join(os.path.dirname(__file__), "save_files", "example.txt"), help="Where to store output")
    parser.add_argument("--verbose", action="store_true", default=False, help="Whether to print out results to terminal.")

    args = parser.parse_args()
    DATA_PATH = args.data_file
    LOG_REGEX = args.log_regex
    SAVE_NAME = args.save_name
    VERBOSE = args.verbose

    print(DATA_PATH, SAVE_NAME, VERBOSE)

    result = process_doc(DATA_PATH, SAVE_NAME, VERBOSE)


if __name__ == "__main__":
    main()