#!/usr/bin/python3
# Import the cmd module
import cmd

# Define a class that inherits from cmd.Cmd
class HBNBCommand(cmd.Cmd):
    # Define a custom prompt
    prompt = "(hbnb) "

    # Define a method to handle the quit command
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True # Return True to exit the cmd loop

    # Define a method to handle the EOF (Ctrl-D) command
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print() # Print a newline
        return True # Return True to exit the cmd loop

    # Define a method to handle empty lines
    def emptyline(self):
        """Do nothing on empty lines"""
        pass # Pass the execution

if __name__ == '__main__':
    HBNBCommand().cmdloop()
