"""
Values for constant variables in /src
"""

from datetime import datetime

DIRECT_SERVICES = set([
    "articulation",
    "fluency", 
    "voice",
    "language"
])

INDIRECT_SERVICES = set([
    "chart",
    "clerical",
    "collaboration",
    "documentation",
    "equipment",
    "education",
    "materials",
    "observe",
    "research",
    "scheduling",
    "staffing",
    "scores",
    "transcription"
])


SECONDS_IN_AN_HOUR = 3600

REGEX_PATTERN = pattern = r"Week (\d+) \((\w+)\) (\d{1,2}:\d{2} [AP]M) - (\d{1,2}:\d{2} [AP]M) : (\w+) (\w+)"

DUMMY_DATE = datetime(2000, 1, 1)   # Dummy date to compare times across the same days
