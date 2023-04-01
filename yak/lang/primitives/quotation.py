from collections import UserList

from yak.lang.primitives import Value, YakPrimitive, print_object


class Quotation(UserList, YakPrimitive):
    """
    Quotations are 'escaped' collections of values. The can act as anonymous functions.
    They are denoted by square brackets (i.e. `[ dup * ]`) and they are pushed onto the
    datastack when seen.

    Quotations can be called, which will result in the evaluation of their contents
    sequentially from start to finish.
    """

    def __init__(self, initial: list = None):
        super().__init__(initial)

    @property
    def count(self) -> int:
        """
        :returns: the number of elements in the quotation.
        :rtype: int.
        """
        return len(self)

    @property
    def empty(self) -> bool:
        """
        :returns: True if there are no values in the quotation, False otherwise.
        :rtype: bool.
        """
        return self.count == 0

    @property
    def head(self) -> Value:
        """
        :returns: the first element of the quotation.
        :rtype: Value.
        """
        if self.empty:
            return None
        return self[0]

    @property
    def tail(self) -> Value:
        """
        :returns: the quotation minus its first element.
        :rtype: Quotation.
        """
        return self[1:]

    def print_object(self) -> str:
        """
        :returns: representation of the quotation.
        :rtype: str.
        """
        if self.empty:
            return '[ ]'
        contents = ' '.join(print_object(value) for value in self)
        return f'[ {contents} ]'
