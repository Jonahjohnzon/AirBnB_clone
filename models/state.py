#!/usr/bin/python3
"""Defines the State class inherited from BaseModel."""
target = __import__("models.base_model")
BaseModel = target

class State(BaseModel):
    """Represent a state.

    Attributes:
        name (str): The name of the state.
    """

    name = ""
