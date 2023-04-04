import pytest

from yak.primitives import Value
from yak.primitives.stack import Stack, StackUnderflowError


@pytest.fixture
def stack(values: list[Value]) -> Stack:
    return Stack(values)


@pytest.mark.parametrize('values', [[0, 1, 2, 3, 4]])
def test_peek_returns_without_removing_the_value_at_the_top_of_the_stack(stack):
    assert stack.peek() == 4
    assert stack.count == 5


@pytest.mark.parametrize('values', [[0, 1, 3]])
def test_pop_returns_and_removes_the_value_at_the_top_of_the_stack(stack):
    assert stack.pop() == 3
    assert stack.count == 2


@pytest.mark.parametrize('values', [[]])
def test_push_appends_value_to_the_top_of_the_stack(stack):
    stack.push(1)
    assert stack.peek() == 1


@pytest.mark.parametrize('values', [[]])
def test_push_all_adds_all_values_to_stack_in_order(stack):
    stack.push_all([1, 2, 3, 4])
    assert stack.peek() == 4
    assert stack == Stack([1, 2, 3, 4])


@pytest.mark.parametrize('values', [[]])
def test_empty_returns_true_if_stack_is_has_no_values(stack):
    assert stack.empty() is True


@pytest.mark.parametrize('values', [[1]])
def test_empty_returns_false_if_stack_is_has_values(stack):
    assert stack.empty() is False


@pytest.mark.parametrize('values', [[]])
def test_not_empty_returns_false_if_stack_is_has_no_values(stack):
    assert stack.not_empty() is False


@pytest.mark.parametrize('values', [[1]])
def test_not_empty_returns_true_if_stack_is_has_values(stack):
    assert stack.not_empty() is True


@pytest.mark.parametrize('values', [[1]])
def test_clear_removes_all_elements_from_the_stack(stack):
    stack.clear()
    assert stack.empty()


@pytest.mark.parametrize('values', [[1]])
def test_check_available_raises_stack_error_if_there_arent_enough_values_in_stack(stack):
    with pytest.raises(StackUnderflowError):
        stack.check_available(3)


@pytest.mark.parametrize('values', [[1, 2]])
def test_from_the_top_returns_a_reversed_iterator_over_stack_values(stack):
    assert list(stack.from_the_top()) == [2, 1]
