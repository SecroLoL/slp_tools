"""
This script manages data entry and edits to existing data files.
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

# TODO add functionality to edit existing data files


def add_new_log_file():
    pass 


def add_new_event(log_file: str, event_input: str):
    pass


def add_event_to_log_file():
    pass


def remove_event_from_log_file():
    pass

# TODO: Maybe each log file should have its own class?
