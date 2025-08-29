# Task Tracker CLI

A simple **command line interface (CLI) application** to track and manage your tasks.  
This project helps you practice working with the filesystem, handling user inputs, and building a functional CLI app without external libraries.

---
## Features
- Add, update, and delete tasks
- Mark tasks as **todo**, **in-progress**, or **done**
- List tasks by status or all at once
- Tasks are stored in a local **JSON file**
- Graceful handling of errors and edge cases
---

## Requirements

- Any programming language (e.g., Python, JavaScript, etc.)
- Native filesystem module (no external libraries/frameworks)
- JSON file stored in the current directory
- JSON file is auto-created if it does not exist
- Uses **positional arguments** in the CLI

---

## Task Properties

Each task will be stored in the JSON file with the following properties:

- **id**: Unique identifier for the task  
- **description**: Short description of the task  
- **status**: `todo`, `in-progress`, or `done`  
- **createdAt**: Date/time the task was created  
- **updatedAt**: Date/time the task was last updated  

---

## Example Usage

```bash
task-tracker add 'New Task'
# Output: 
# Name: New Task
# ID: 1
# Status: TODO
# Created: 2025-08-30 00:00:51
# Updated: 2025-08-30 00:00:51

task-tracker update 1 'Updated name on Task'
# Output: 
# Name: Updated name on Task
# ID: 1
# Status: TODO
# Created: 2025-08-30 00:00:51
# Updated: 2025-08-30 00:02:11

task-tracker status 2 inprogress
# Output
# Name: New Task
# ID: 2
# Status: IN_PROGRESS
# Created: 2025-08-30 00:03:23
# Updated: 2025-08-30 00:04:37

task-tracker list
# Output:
# Name: Updated name on Task
# ID: 1
# Status: TODO
# Created: 2025-08-30 00:03:03
# Updated: 2025-08-30 00:03:07

# Name: New Task
# ID: 2
# Status: IN_PROGRESS
# reated: 2025-08-30 00:03:23
# Updated: 2025-08-30 00:03:23

task-tracker list IN_pRoGreSS
# Output:
# Name: New Task
# ID: 2
# Status: IN_PROGRESS
# Created: 2025-08-30 00:03:23
# Updated: 2025-08-30 00:04:37

task-tracker delete 1
task-tracker list
# Output:
# Name: New Task
# ID: 2
# Status: IN_PROGRESS
# Created: 2025-08-30 00:03:23
# Updated: 2025-08-30 00:04:37

# Example of a malformed command w/ a graceful exit (id 155 does not exist)
task-tracker.py delete 155
# Output: 
# delete command failed with {'command': 'delete', 'id': '155'}
# usage: task-tracker [-h] {add,update,delete,status,list} ...

# A simple command line interface (CLI) application to track and manage your tasks.

# positional arguments:
#   {add,update,delete,status,list}
#     add                 Create a task
#     update              Update a task by ID
#     delete              Delete a task by ID
#     status              Set task status
#     list                List all tasks, optionally filtering by status

# options:
#   -h, --help            show this help message and exit
```