#!/usr/bin/python3
"""Module contains entry point for command line interpreter"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """class of the command line interpreter"""
    prompt = '(hbnb)'
    class_names = ['BaseModel', 'User', 'Place',
                   'State', 'City', 'Amenity', 'Review']

    def do_create(self, arg):
        """Creates a new instance of BaseModel or User,
        saves it (to the JSON file) and prints the id"""
        if not arg:
            print("** class name missing **")
            return

        if arg not in self.class_names:
            print("** class doesn't exist **")
            return

        try:
            obj = eval(f"{arg}()")
            obj.save()
            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an
        instance based on the class name and id"""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in self.class_names:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name
        and id (save the change into the JSON file)"""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in self.class_names:
            print("** class doesn't exist ")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        if arg and arg not in self.class_names:
            print("**class doesn't exist **")
            return

        print([str(obj) for obj in storage.all().values()
              if not arg or type(obj).__name__ == arg])

    def do_update(self, arg):
        """Updates an instance based on the class name
        and id by adding or updating attribute"""
        args = arg.split(" ")

        if len(args) < 1 or args[0] not in self.class_names:
            print("** class name missing **" if len(args)
                  < 1 else "** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        instance = storage.all()[key]
        setattr(instance, args[2], args[3].strip('"'))
        instance.save()

    def default(self, line):
        """Handle commands which do not have a dedicated method"""
        parts = line.split('.')
        if len(parts) == 2:
            class_name, command = parts
            if class_name in self.class_names:
                command_parts = command.split('(')
                if len(command_parts) == 2 and command_parts[1].endswith(")"):
                    action, args_str = command_parts
                    args_str = args_str[:-1]

                    if action == "all":
                        self.do_all(class_name)
                    elif action == "count":
                        self.count_instances(class_name)
                    elif action == "show":
                        self.do_show(f"{class_name} {args_str}")
                    elif action == "destroy":
                        self.do_destroy(f"{class_name} {args_str}")
                    elif action == "update":
                        update_args = ' '.join(arg.strip('"') for
                                               arg in args_str.split(', '))
                        self.do_update(f"{class_name} {args_str}")
                    else:
                        print("*** Unknown syntax:", line)
                else:
                    print("*** Unknown syntax:", line)
            else:
                print("** class doesn't exist **")
        else:
            print("*** Unknown syntax:", line)

    def count_instances(self, class_name):
        """Count the number of instances of a given class"""
        count = 0
        for key in storage.all():
            if key.startswith(class_name + '.'):
                count += 1
        print(count)

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
