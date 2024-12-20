import json
import sys
from abc import (abstractmethod, ABC)
from datetime import datetime

statuses = ['todo', 'in-progress', 'done']

class Command(ABC):
    def __init__(self, handler: 'Handler'):
        self.handler = handler

    @abstractmethod
    def __call__(self, *args, **kwds):
        pass

    @property
    @abstractmethod
    def title(self):
        pass

class ListCommand(Command):
    title = 'list'
    def __call__(self, status=None, *args):
        if status is None:
            self.print_notes(self.handler.data)
        else:
            if status not in statuses:
                print('status should be todo, in-progress or done')
                return
            self.print_notes(list([note for note in self.handler.data if note['status'] == status]))
    
    def print_notes(self, notes:list, sort_by='id'):
        for note in sorted(notes, key=lambda note: note[sort_by]):
            print(f'[{note['id']}] {note['status']} "{note['content']}" created at {note['createdAt']} updated at {note['updatedAt']}')

class AddCommand(Command):
    title = 'add'
    def __call__(self, content, *args):
        print(f"Task added successfully (ID: {self.handler.add_note(content)})")

class RemoveCommand(Command):
    title = 'del'
    def __call__(self, id, *args):
        self.handler.remove_note(int(id))

class UpdateCommand(Command):
    title = 'update'
    def __call__(self, id, content, *args):
        self.handler.change_note(int(id), content)

class MarkInProgress(Command):
    title = 'mark-in-progress'
    def __call__(self, id, *args):
        self.handler.mark_in_progress(int(id))

class MarkDone(Command):
    title = 'mark-done'
    def __call__(self, id, *args):
        self.handler.mark_done(int(id))

class Handler:
    def __init__(self):
        with open('data.json', 'r+') as file:
            self.data = json.load(file)
    
    def add_note(self, content):
        id = len(self.data)
        self.data.append({
            'id': id,
            'status': 'todo',
            'content': content,
            'createdAt': datetime.now().strftime('%H:%M:%S'),
            'updatedAt': datetime.now().strftime('%H:%M:%S'),
        })
        with open('data.json', 'w') as file:
            json.dump(self.data, file)
        
        return id

    def get_index_by_id(self, id:int):
        for note in self.data:
            if note['id'] == id:
                return self.data.index(note)

    def remove_note(self, id:int):
        index = self.get_index_by_id(id)
        if index is None:
            return print("note is not found")
        self.data.pop(index)

        with open('data.json', 'w') as file:
            json.dump(self.data, file)
    
    def change_note(self, id, content):
        self.data[id]['content'] = content
        self.data[id]['updatedAt'] = datetime.now().strftime('%H:%M:%S')
        with open('data.json', 'w') as file:
            json.dump(self.data, file)
        
    def mark_in_progress(self, id:int):
        self.data[id]['status'] = 'in-progress'
        self.data[id]['updatedAt'] = datetime.now().strftime('%H:%M:%S')
        with open('data.json', 'w') as file:
            json.dump(self.data, file)

    def mark_done(self, id:int):
        self.data[id]['status'] = 'done'
        self.data[id]['updatedAt'] = datetime.now().strftime('%H:%M:%S')
        with open('data.json', 'w') as file:
            json.dump(self.data, file)

class Invoker:
    def __init__(self):
        self.handler = Handler()
        self.commands = map(lambda command: command(self.handler), Command.__subclasses__())
        self.commands_by_name = {}
        for command in self.commands:
            self.commands_by_name[command.title] = command
    
    def __call__(self, command, *args, **kwds):
        self.commands_by_name[command](*args)

try:
    with open('data.json', 'r+') as file:
        if file.read() == '':
            file.write('[]')
except:
    with open('data.json', 'w+') as file:
        file.write('[]')

invoker = Invoker()

inp = sys.argv[1:]
command = inp[0]
if len(inp) > 1:
    args = inp[1:]
    invoker(command, *args)
else:
    invoker(command)
