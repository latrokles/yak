from collections import deque

from yak.primitives import Value, YakError, YakPrimitive, print_object


class YakStackError(YakError):
    """Raised during a stack operation failure."""


class Stack(deque, YakPrimitive):
    """Stack data structure. Mostly a wrapper around `collections.deque`."""
    name: str

    @property
    def count(self) -> int:
        """
        Return the number of elements the stack.
        :returns: number of elements in the stack.
        :rtype: int.
        """
        return len(self)

    def pop(self) -> Value:
        """
        Remove and return the value at the top of the stack.
        :returns: value at the top of the stack.
        :rtype: Any.
        :raises YakStackError if stack is empty.
        """
        self.check_available(1)
        return super().pop()

    def peek(self) -> Value:
        """
        Return the value at the top of the stack, without removing it.
        :returns: the value at the top of the stack.
        :rtype: Any.
        :raises YakStackError if stack is empty.
        """
        self.check_available(1)
        return self[-1]

    def push(self, value: Value):
        """
        Push `value` onto the stack.
        :param value: value to push onto the top of the stack.
        :type value: Any.
        """
        self.append(value)

    def push_all(self, values: list[Value]):
        """
        Push all `values` onto the stack.
        :param values: values to push.
        :type values: list[Any].
        """
        self.extend(values)

    def empty(self) -> bool:
        """
        Check if stack is empty.
        :returns: `True` if stack is empty, `False` otherwise.
        :rtype: bool.
        """
        return self.count == 0

    def not_empty(self) -> bool:
        """
        Check if stack is not empty.
        :returns: `True` is stack is not empty, `False` otherwise.
        :rtype: bool.
        """
        return not self.empty()

    def clear(self):
        """Clear stack."""
        super().__init__()

    def check_available(self, count: int):
        """
        Check if there are `count` values in the array.
        :param count: the number of values to check for in the array.
        :type count: int.
        :raises YakStackError if the available values are fewer than count.
        """
        if count > self.count:
            err = f'Underflow: expected={count}, actual={self.count}'
            raise YakStackError(err)

    def print_object(self) -> str:
        contents = [print_object(value) for value in self]
        contents[-1] = f'{contents[-1]} <- TOS'
        return '\n'.join(contents)
