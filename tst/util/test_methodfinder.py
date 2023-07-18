from yak.util.methodfinder import find_function, find_method


def test_find_method():
    assert find_method('hello').that_returns('HELLO') == ['swapcase', 'upper']
    assert find_method('HeLlo').that_returns('hElLO') == ['swapcase']
    assert find_method('hello', 'hell', 'HELL').that_returns('HELLo') == ['replace']


def test_find_function():
    assert find_function('math', 4).that_returns(24) == ['factorial', 'perm']
