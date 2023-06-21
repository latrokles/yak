import pytest

from yak.primitives.vocabulary import Vocabulary
from yak.primitives.word import Word


@pytest.fixture
def vocab() -> Vocabulary:
    return Vocabulary('test')


def test_store_adds_word_to_vocab(vocab):
    vocab.store(Word('+', vocab.name))
    assert vocab.count == 1


def test_fetch_returns_word_with_name_from_vocab(vocab):
    word = Word('+', vocab.name)
    vocab.store(word)
    assert vocab.fetch('+') == word


def test_fetch_returns_none_if_word_does_not_exist(vocab):
    assert vocab.fetch('+') is None


def test_list_returns_list_of_defined_words_in_vocab(vocab):
    vocab.store(Word('+', vocab.name))
    vocab.store(Word('-', vocab.name))
    vocab.store(Word('=', vocab.name))

    words = vocab.list()
    assert [w.name for w in words] == ['+', '-', '=']


def test_count_returns_list_of_words_in_vocab(vocab):
    vocab.store(Word('+', vocab.name))
    vocab.store(Word('-', vocab.name))
    vocab.store(Word('=', vocab.name))

    assert vocab.count == 3
