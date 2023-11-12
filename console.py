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
            "count": self.do_count
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
        """Quit command to exit the program."""
        return True

    # Define a method to handle the EOF (Ctrl-D) command
    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    # Define  function to execute the create command
    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argss = parse(arg)
        if len(argss) == 0:
            print("** class name missing **")
        elif argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argss[0])().id)
            storage.save()

    # Define  function to execute the show command
    def do_show(self, argl):
        """Usage: show <class> <id> or <class>.show(<id>)
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
        instance = storage.all()
        print(instance["{}.{}". format(args[0], args[1])])

    # Define function to execute the destroy command
    def do_destroy(self, argl):
        """ Usage: destroy <class> <id> or <class>.destroy(<id>)
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
        if "{}.{}".format(class_name, instance_id) not in storage.all().keys():
            print("** no instance found **")
            return
        # Delete the instance from the JSON file
        del storage.all()["{}.{}".format(class_name, args[1])]
        # Save the changes
        storage.save()

    # Define function to execute the all command
    def do_all(self, argl):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args = parse(argl)
        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objss = []
            for ob in storage.all().values():
                if len(args) > 0 and args[0] == ob.__class__.__name__:
                    objss.append(ob.__str__())
                elif len(args) == 0:
                    objss.append(ob.__str__())
            print(objss)

    def do_update(self, argl):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args = parse(argl)
        objt = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in objt.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args) == 4:
            obj = objt["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valtyp = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtyp(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = objt["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtyp = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtyp(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argss = parse(arg)
        number = 0
        for user in storage.all().values():
            if argss[0] == user.__class__.__name__:
                number += 1
        print(number)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
