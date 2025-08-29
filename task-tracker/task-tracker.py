import argparse
import os
import json
import time
from enum import Enum
from typing import List

# BRIEF: https://roadmap.sh/projects/task-tracker
# COMMANDS: ADD, UPDATE, DELETE, STATUS, LIST, LIST(STATUS)


class JsonDataContext:
    def __init__(self, filepath):
        self.filepath = filepath
        pass

    def load(self, cls):
        if not os.path.exists(self.filepath):
            # Handle dictionaries, lists & symbols
            default = [] if cls is list else {} if cls is dict else cls()
            self.save(default)
            return default

        with open(self.filepath) as file:
            data = json.load(file)
            if not isinstance(data, cls):
                raise TypeError(data)
            return data

        return None

    def save(self, data):
        with open(self.filepath, "w") as file:
            json_data = json.dumps(
                data, default=lambda object: object.__dict__, indent=4)
            file.write(json_data)
        pass

    def parse_list(data, cls):
        items = []
        for item in data:
            try:
                items.append(cls(**item))
            except TypeError as exception:
                raise ValueError(f'Malformed data: {item}') from exception
        return items


class Task:
    class Status(Enum):
        TODO = 1
        IN_PROGRESS = 2
        DONE = 3

    def __init__(self, id, name, status, created_at, updated_at):
        self.id = id
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        pass

    def __str__(self):
        return f'id: {self.id}\nname: {self.name}\nstatus: {self.status}\ncreated_at: {self.created_at}\nupdated_at: {self.updated_at}'
        pass

    def get_index_by_id(tasks, task_id):
        return next((i for i, task in enumerate(tasks)
                     if int(task.id) == int(task_id)), None)

    def get_by_id(tasks, id):
        index = Task.get_index_by_id(tasks, id)
        if index is None:
            return None
        return tasks[index]

    @staticmethod
    def add(arguments, task_context: JsonDataContext):
        assert arguments.name is not None

        json_data = task_context.load(list)
        tasks = JsonDataContext.parse_list(json_data, Task)

        # Auto increment
        task = Task(
            id=(len(tasks) + 1),
            name=arguments.name,
            status=Task.Status.TODO.value,
            created_at=time.time(),
            updated_at=time.time(),
        )

        tasks.append(task)
        task_context.save(tasks)
        return task

    @staticmethod
    # Updates an existing task and saves to file.
    def update(arguments, task_context: JsonDataContext):
        assert arguments.id is not None
        assert arguments.name is not None

        json_data = task_context.load(list)
        tasks = JsonDataContext.parse_list(json_data, Task)

        index = Task.get_index_by_id(tasks, arguments.id)
        task = tasks[index]

        task.name = arguments.name
        task.updated_at = time.time()

        tasks[index] = task

        task_context.save(tasks)
        return task

    @staticmethod
    # Deletes an existing task
    def delete(arguments, task_context: JsonDataContext):
        assert arguments.id is not None

        json_data = task_context.load(list)
        tasks = JsonDataContext.parse_list(json_data, Task)

        index = Task.get_index_by_id(tasks, arguments.id)
        task = tasks[index]

        tasks.pop(index)

        task_context.save(tasks)
        return task

    @staticmethod
    # Sets the status of an existing task
    def set_status(arguments, task_context: JsonDataContext):
        return "status"
        pass

    @staticmethod
    # Lists all tasks, and filters by optional status
    def list(arguments, task_context: JsonDataContext):
        return 'list'
        pass


class Parameter:
    def __init__(self, name: str, help: str):
        self.name = name
        self.help = help
        pass


class Argument(Parameter):
    def __init__(self, name: str, help: str, optional: bool = False):
        self.optional = optional
        super().__init__(name, help)


class CommandBuilder:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser
        self.subparsers = self.parser.add_subparsers(
            dest='command', required=True)
        self.handler = CommandHandler()
        pass

    def add_command(self, command: Parameter, arguments: List[Argument], handler):
        parser = self.subparsers.add_parser(command.name, help=command.help)
        for argument in arguments:

            # '?' defines the argument as optional, setting to None makes it required.
            nargs = '?' if argument.optional else None

            parser.add_argument(argument.name, help=argument.help,
                                nargs=nargs)
        self.handler.add_handler(command, handler)
        pass

    def build(self):
        return self.handler, self.parser.parse_args()


class CommandHandler:
    def __init__(self):
        self.handlers = {}
        pass

    def add_handler(self, command: Parameter, handler):
        self.handlers[command.name] = handler
        pass

# make this safe .-.
    def handle(self, arguments, context):
        command = arguments.command
        handler = self.handlers[command]
        return handler(arguments, context)


def main():
    HELP_ID = 'The ID of the task (use the list command to get the ID)'

    parser = argparse.ArgumentParser(
        prog="task-tracker",
        description='A simple command line interface (CLI) application to track and manage your tasks.'
    )

    command_builder = CommandBuilder(parser=parser)
    command_builder.add_command(Parameter(name='add', help="Create a task"), [
                                Argument(name='name', help='Name of the task')], Task.add)

    command_builder.add_command(Parameter(name='update', help='Update a task by ID'), [Argument(
        name='id', help=HELP_ID), Argument(name='name', help='Name of the task')], Task.update)

    command_builder.add_command(Parameter(name='delete', help='Delete a task by ID'), [
                                Argument(name='id', help=HELP_ID)], Task.delete)

    command_builder.add_command(Parameter(name='status', help="Set task status"), [Argument(
        name='id', help=HELP_ID), Argument(name='status', help="Status of the task")], Task.set_status)

    command_builder.add_command(
        Parameter(name='list', help="List all tasks, optionally filtering by status"), [
            Argument(name='status', help="Filter tasks by status", optional=True)], Task.list
    )

    command_handler, arguments = command_builder.build()

    task_context = JsonDataContext('tasks.json')
    response = command_handler.handle(arguments, task_context)
    print(response)


main()
