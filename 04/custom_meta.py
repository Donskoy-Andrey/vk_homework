from typing import Any


class CustomMeta(type):
    def setter(cls, name: str, val: Any):
        if not name.startswith("__") and not name.endswith("__"):
            name = f"custom_{name}"
        cls.__dict__[name] = val

    def __init__(mcs, name, bases, classdict: dict, **kwargs):
        super().__init__(name, bases, classdict, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def __new__(mcs, name, bases, classdict: dict, **kwargs):

        new_classdict = dict()

        for key, value in classdict.items():

            if key[:2] != "__" and key[-2:] != "__":
                new_classdict["custom_" + key] = value
            else:
                new_classdict[key] = value

        new_classdict["__setattr__"] = mcs.setter
        cls = super().__new__(mcs, name, bases, new_classdict, **kwargs)

        return cls


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val: int = 99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
