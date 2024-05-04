"""
Uploading and extracting relevant timesheet information from input data
"""

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


def process_doc(filename: str, save_name: str = "") -> Mapping[str, Mapping[str, float]]:
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
    return service_to_hours


def main():

    result = process_doc(os.path.join(os.path.dirname(__file__), 'test_week.txt'))
    
    print("================DIRECT SERVICES================")
    for task, duration in sorted((result.get('direct', [])).items()):
        print(f"Task: {task}   Duration for the week: {duration} hours.")

    direct_hours_total = sum(result.get("direct", []).values())
    print(f"Total direct hours for week : {direct_hours_total}")

    print("================INDIRECT SERVICES================")
    for task, duration in sorted(result.get('indirect', []).items()):
        print(f"Task: {task}   Duration for the week: {duration} hours.")

    indirect_hour_total = sum(result.get("indirect", []).values())
    print(f"Total indirect hours for week : {indirect_hour_total}")

    print(f"Total hours for the week : {direct_hours_total + indirect_hour_total}")


if __name__ == "__main__":
    main()