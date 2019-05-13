"""A subclassing of list to provide various array operations.

This was built in order to avoid using NumPy (just as an additional learning-opportunity).
NumPy is great!
"""

# TODO add docstrings to dunder methods

import operator


class InvalidInputException(Exception):
    """Raised when input to Array is not of type list."""


class Array(list):
    """A subclassing of list so that we don't have to rely on NumPy."""

    def __init__(self, data):
        """Implement various array/vector/list methods.

        Parameters
        ----------
        data : list

        """
        self.__check_input(data)
        self.data = data
        super().__init__()
q
    def __repr__(self):
        """Match the representation of a list."""
        return str(self.data)

    def __len__(self):
        """Match the implementation of list."""
        return len(self.data)

    def __getitem__(self, keys):
        """Index like a list."""
        keys = (keys,) if not isinstance(keys, tuple) else keys
        shape = self.shape

        if len(keys) > len(shape):
            raise IndexError(
                "Too many indices. At most {req}, found {found}".format(
                    req=shape, found=len(keys)
                )
            )

        prev_was_slice = False
        val_at_index = self.data

        for key in keys:
            if prev_was_slice:
                val_at_index = [row[key] for row in val_at_index]
            else:
                val_at_index = val_at_index[key]
                if isinstance(key, slice):
                    prev_was_slice = True

        if isinstance(val_at_index, list):
            val_at_index = Array(val_at_index)

        return val_at_index

    def __iter__(self):
        """Iterate over class like a list."""
        self.index = 0
        return self

    def __next__(self):
        if self.index >= self.shape[0]:
            raise StopIteration
        val_at_index = self.data[self.index]

        self.index += 1
        if isinstance(val_at_index, list):
            return Array(val_at_index)
        return val_at_index

    def __add__(self, other):
        return self.__array_opp(operator.add, self, other)

    def __sub__(self, other):
        return self.__array_opp(operator.sub, self, other)

    def __mul__(self, other):
        return self.__array_opp(operator.mul, self, other)

    def __truediv__(self, other):
        return self.__array_opp(operator.truediv, self, other)

    def __pow__(self, other):
        return self.__array_opp(operator.pow, self, other)

    def __gt__(self, other):
        return self.__array_opp(operator.gt, self, other)

    def __lt__(self, other):
        return self.__array_opp(operator.lt, self, other)

    def __ge__(self, other):
        return self.__array_opp(operator.ge, self, other)

    def __le__(self, other):
        return self.__array_opp(operator.le, self, other)

    def __ne__(self, other):
        return self.__array_opp(operator.ne, self, other)

    def __eq__(self, other):
        return self.__array_opp(operator.eq, self, other)

    def __abs__(self):
        return self.abs()

    def abs(self):
        """Return an Array which each elements is its absolute value."""
        return Array([abs(idx) for idx in self])

    @property
    def shape(self):
        """Get shape of list."""
        data = self.data
        shape = [len(data)]
        while True:
            data = data[0]
            if isinstance(data, list):
                shape.append(len(data))
            else:
                return tuple(shape)

    @property
    def transpose(self):
        """[M x N] -> [N x M]."""
        if len(self.shape) > 1:
            return Array([list(row) for row in zip(*self)])
        return self

    @staticmethod
    def __array_opp(opp, left, right):
        if isinstance(right, (int, float)):
            return Array([opp(xi, right) for xi in left])

        if isinstance(right, list):
            # TODO rework logic to be more readable
            right = Array(right)
            left_shape = left.shape
            right_shape = right.shape

            if left_shape == right_shape:
                return Array([opp(xi, yi) for xi, yi in zip(left, right)])

            if (len(left_shape) > (len(right_shape))) and (
                left_shape[1] == right_shape[0]
            ):
                return Array([opp(xi, right) for xi in left])

        raise ValueError(
            "Cannot cast arrays of shape {left_shape} and {right_shape} together".format(
                left_shape=left_shape, right_shape=right_shape
            )
        )

    @staticmethod
    def __check_input(data):
        # TODO shape must be consistent
        if not isinstance(data, list):
            raise InvalidInputException("Input must be of type list")
