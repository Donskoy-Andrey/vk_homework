class Integer:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_{name}"

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self._instance_attr_name)
        except AttributeError:
            return

    def __set__(self, instance, value):
        if isinstance(value, int):
            return setattr(
                instance,
                self._instance_attr_name,
                value
            )
        raise ValueError("The value is not an integer.")

    def __delete__(self, instance):
        return delattr(instance, self._instance_attr_name)


class String:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_{name}"

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self._instance_attr_name)
        except AttributeError:
            return

    def __set__(self, instance, value):
        if isinstance(value, str):
            return setattr(
                instance,
                self._instance_attr_name,
                value
            )
        raise ValueError("The value is not a string.")

    def __delete__(self, instance):
        return delattr(instance, self._instance_attr_name)


class PositiveInteger:
    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_{name}"

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self._instance_attr_name)
        except AttributeError:
            return

    def __set__(self, instance, value):
        if isinstance(value, int) and value > 0:
            return setattr(
                instance,
                self._instance_attr_name,
                value
            )
        raise ValueError("The value is not a positive integer.")

    def __delete__(self, instance):
        return delattr(instance, self._instance_attr_name)


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
