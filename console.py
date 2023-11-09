#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl

# Define a class that inherits from cmd.Cmd
class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    # Define a method to handle empty lines
    def emptyline(self):
        """Do nothing on empty lines"""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "create": self.do_create,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "all": self.do_all,
            "update": self.do_update,
            "count" : self.do_count
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    # Define a method to handle the quit command
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True # Return True to exit the cmd loop

    # Define a method to handle the EOF (Ctrl-D) command
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("") # Print a newline
        return True # Return True to exit the cmd loop
    
    # Define  function to execute the create command
    def do_create(self, argl):
        """Usage: create <class>
        Create a new class and print its id.
        """
        args = parse(argl)
        if len(args) == 0:
            print("** class name missing **")
            return
        classname = args[0]
        if classname not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        # Create a new instance of the class
        instance = classname
        # Save the instance to the JSON file
        instance.save()
        # Print the id of the instance
        print(instance.id)

    # Define  function to execute the show command
    def do_show(self, argl):
        """Usage: <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = parse(argl)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        # Check if the id is given
        if len(args) == 1:
            print("** instance id missing **")
            return
        # Check if the instance exists
        instance_id = args[1]
        key = class_name + "." + instance_id
        if key not in storage.all():
            print("** no instance found **")
            return
        # Print the string representation of the instance
        instance = storage.all()[key]
        print(instance)

    # Define function to execute the destroy command
    def do_destroy(self, argl):
        """Usage: <class>.destroy(<id>)
        Delete a class instance of a given id.
        """
        args = parse(argl)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        # Check if the id is given
        if len(args) == 1:
            print("** instance id missing **")
            return
        # Check if the instance exists
        instance_id = args[1]
        key = class_name + "." + instance_id
        if key not in storage.all():
            print("** no instance found **")
            return
        # Delete the instance from the JSON file
        storage.delete(storage.all()[key])
        # Save the changes
        storage.save()
        
    # Define function to execute the all command
    def do_all(self, argl):
        """Usage: <class>.all()
        Show string representations of all instances of a given class.
        If no class is specified, displays  instantiated objects."""
        args = parse(argl)
        if len(args) == 0:
            # Print all instances
            instances = storage.all().values()
        else:
            # Check if the class name is valid
            class_name = args[0]
            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            # Print only instances of the given class
            instances = [v for v in storage.all().values() if v.__class__.__name__ == args[0]]
            # Convert the instances to a list of strings
            strings = [str(i) for i in instances]
            # Print the list of strings
            print(strings)

    # Define a function to execute the update command
    def do_update(self, argl):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args = parse(argl)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes :
            print("** class doesn't exist **")
            return
        # Check if the id is given
        if len(args) == 1:
            print("** instance id missing **")
            return
        # Check if the instance exists
        instance_id = args[1]
        key = class_name + "." + instance_id
        if key not in storage.all():
            print("** no instance found **")
            return
        # Check if the attribute name is given
        if len(args) == 2:
            print("** attribute name missing **")
            return
        # Check if the attribute value is given
        if len(args) == 3:
            print("** value missing **")
            return
        # Get the instance and the attribute name and value
        instance = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]
        # Convert the attribute value to the correct type
        try:
            attr_value = int(attr_value)
        except ValueError:
            try:
                attr_value = float(attr_value)
            except ValueError:
                # Remove the quotes from the string value
                attr_value = attr_value.strip("\"'")
                # Update the attribute of the instance
                setattr(instance, attr_name, attr_value)
                # Save the changes to the JSON file
                instance.save()

    def do_count(self, arg):
        """Use: Get the number of instances"""
        argss = parse(arg)
        number = 0
        for user in storage.all().values():
            if argss[0] == user.__class__.__name__:
                number += 1
        print(number)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
