# AirBnB_CLONE 

## Welcome to the AirBnB clone project!

Read and go through the steps of AirBnB concept page.

1. First step: Write a command interpreter to manage your AirBnB objects.
   - This is the first step towards building your first full web application: the AirBnB clone.
   - This first step is very important because you will use what you build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

Each task is linked and will help you to:

- Put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances.
- Create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file.
- Create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel.
- Create the first abstracted storage engine of the project: File storage.
- Create all unittests to validate all our classes and storage engine.

## Resources
Read or watch:

- cmd module
- cmd module in depth
- packages concept page
- uuid module
- datetime
- unittest module
- args/kwargs
- Python test cheatsheet
- cmd module wiki page
- python unittest

## Requirements

PYTHON SCRIPTS
 - Allowed editors: vi, vim, emacs.
 - All your files will be interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.8.5).
 - All your files should end with a new line.
 - The first line of all your files should be exactly #!/usr/bin/python3.
 - A README.md file, at the root of the folder of the project, is mandatory.
 - Your code should use the pycodestyle (version 2.8.*).
 - All your files must be executable.

PYTHON UNIT TESTS
 - Allowed editors: vi, vim, emacs.
 - All your files should end with a new line.
 - All your test files should be inside a folder tests.
 - You have to use the unittest module.
 - All your test files should be python files (extension: .py).
 - All your test files and folders should start by test.
 - Your file organization in the tests folder should be the same as your project.
 - For models/base_model.py, unit tests must be in: tests/test_models/test_base_model.py.
 - For models/user.py, unit tests must be in: tests/test_models/test_user.py.
 - All your tests should be executed by using this command: python3 -m unittest discover tests.
 - You can also test file by file by using this command: python3 -m unittest tests/test_models/test_base_model.py.
 - All your modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)').
 - All your classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)').
