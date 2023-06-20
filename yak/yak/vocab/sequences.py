from yak.primitives.quotation import Quotation


def partition(interpreter):
    """( quot n -- quot_of_quots )"""
    interpreter.datastack.check_available(2)
    partition_size = interpreter.datastack.pop()
    quot = interpreter.datastack.pop()
    partitioned = [ quot[i:i+partition_size] for i in range(0, quot.count, partition_size) ]
    interpreter.datastack.push(partitioned)


def quotation_to_tuple(interpreter):
    """( quot -- tuple )"""
    quot = interpreter.datastack.peek()
    if not isinstance(quot, Quotation):
        raise YakError(f'Unable to convert to tuple: `{quot}` is not a quotation')
    interpreter.datastack.push(tuple(interpreter.datastack.pop()))


def quotation_to_assoc(interpreter):
    """( quot -- assoc )"""
    quot = interpreter.datastack.peek()
    if not isinstance(quot, Quotation):
        raise YakError(f'Unable to convert to assoc: `{quot}` is not a quotation')

    if quot.count % 2 != 0:
        raise YakError(f'Unable to convert to assoc: `{quot}` has odd number of elements')

    interpreter.datastack.push(2)
    partition(interpreter)
    assoc = { k: v for k, v in interpreter.datastack.pop() }
    interpreter.datastack.push(assoc)
