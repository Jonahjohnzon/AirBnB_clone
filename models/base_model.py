#!/usr/bin/python3
"""BaseModel class"""

import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Class"""

    def __init__(self, *args, **kwargs):
        """intialize the class
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if (len(kwargs) != 0):
            for x, y in kwargs.items():
                if (x == "created_at" or x == "updated_at"):
                    self.__dict__[x] = datetime.strptime(y, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[x] = y
        else:
            models.storage.new(self)

    def save(self):
        """change updated_at to curren time"""
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """print: [<class name>] (<self.id>) <self.__dict__>"""
        classname = self.__class__.__name__
        return "[{}] ({}) {}".format(classname, self.id, self.__dict__)

    def to_dict(self):
        """Return dictinry of Basemodel"""
        diction = self.__dict__.copy()
        diction["created_at"] = self.created_at.isoformat()
        diction["updated_at"] = self.updated_at.isoformat()
        diction["__class__"] = self.__class__.__name__
        return diction
