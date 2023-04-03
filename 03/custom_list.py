class CustomList(list):

    def __add__(self, other):

        new_list = []

        if len(self) >= len(other):
            new_list.extend(self)
            for i, elem in enumerate(other):
                new_list[i] += elem

        else:
            new_list.extend(other)
            for i, elem in enumerate(self):
                new_list[i] += elem

        return CustomList(new_list)

    def __sub__(self, other):

        new_list = []
        if len(self) >= len(other):
            new_list.extend(self)
            for i, elem in enumerate(other):
                new_list[i] -= elem

        else:
            new_list.extend([-i for i in other])
            for i, elem in enumerate(self):
                new_list[i] += elem

        return CustomList(new_list)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return CustomList(other) - self

    def __str__(self):
        return f"Elements: {super.__str__(self)}, Sum of Elements: {sum(self)}"

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)
