"""
Defining classes of services provided during clinical internships
"""
import os 
import sys
from typing import List, Tuple, Mapping

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))   # locate root dir
sys.path.append(parent_dir)

from constants import *


class SLPService():

    def __init__(self, task_type: str, start_time: datetime, end_time: datetime):

        self.task_type = task_type 
        
        assert task_type in DIRECT_SERVICES and task_type not in INDIRECT_SERVICES or task_type in INDIRECT_SERVICES and task_type not in DIRECT_SERVICES, task_type   # needs to be a unique task
        self.direct_service = task_type in DIRECT_SERVICES

        self.start_time = start_time
        self.end_time = end_time

    def get_duration(self):
        return (self.end_time - self.start_time).total_seconds() / SECONDS_IN_AN_HOUR