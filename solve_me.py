from ast import arg


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        """Reads tasks.txt"""
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        """Reads completed.txt"""
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        """Saves current tasks in tasks.txt"""
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        """Saves completed tasks in completed.txt"""
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                if item != '\n':
                    item = item.replace('\n', '')
                    f.write(f"{item}\n")

    def run(self, command, args):
        """Runs the code"""
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        """Prints out the list of commands which can be used incase you get stuck."""
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        """Adds a new task, takes in 2 arguments priority and the task which should be between "" if its more than a single word"""
        args[0] = int(args[0])

        def manage(args):
            if args[0] not in self.current_items.keys():
                self.current_items.update({args[0]: args[1]})
            else:
                task = self.current_items[args[0]]
                del self.current_items[args[0]]
                self.current_items.update({args[0]: args[1]})
                args = [args[0]+1, task]
                manage(args)
        manage(args)

        # self.current_items = dict(sorted(self.current_items.items()))
        self.write_current()
        print(f'Added task: "{args[1]}" with priority {args[0]}')

    def done(self, args):
        """Marks a task as done, takes in priority as argument"""
        args[0] = int(args[0])
        try:
            self.completed_items.append(self.current_items[args[0]])
            del self.current_items[args[0]]
            self.write_current()
            self.write_completed()
            print('Marked item as done.')
        except:
            print(f'Error: no incomplete item with priority {args[0]} exists.')

    def delete(self, args):
        """Deletes a task of a particular priority"""
        args[0] = int(args[0])
        try:
            del self.current_items[args[0]]
            self.write_current()
            print(f'Deleted item with priority {args[0]}')
        except:
            print(
                f'Error: item with priority {args[0]} does not exist. Nothing deleted.')

    def ls(self):
        """Lists out all the current items"""
        for i, (key, value) in enumerate(self.current_items.items()):
            print(f'{i+1}. {value} [{key}]')

    def report(self):
        """Prints out the report of pending and completed tasks"""
        print(f'Pending : {len(self.current_items)}')
        self.ls()
        print(f'\nCompleted : {len(self.completed_items)}')
        self.read_completed()
        for index, item in enumerate(self.completed_items):
            print(f'{index+1}. {item}')
