import json
import re

TIMESTAMP_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

# define the pattern for matching the timestamp format
def timestamp_matching(timestamp:str):
    global TIMESTAMP_PATTERN
    return TIMESTAMP_PATTERN.match(timestamp)

# text loader

def load_text():
    with open('README.md', 'r') as readme_file:
        return readme_file.read()

# db loader
def load_db():
    with open("app_db.json") as f:
        return json.load(f)

db = load_db()
readme_text = load_text()

