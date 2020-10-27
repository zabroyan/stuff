from OrodaelTurrim.Structure.TypeStrucutre import DoubleLinkedList
import pytest


@pytest.fixture(scope='module')
def dll():
    return DoubleLinkedList()


@pytest.mark.order1
def test_empty_dll(dll):
    assert dll.empty()
    assert not bool(dll)


@pytest.mark.order2
def test_push_back(dll):
    dll.push_back(5)
    assert dll.head.value == 5

    dll.push_back(6)
    assert dll.head.value == 6


@pytest.mark.order3
def test_push_front(dll):
    dll.push_front(2)
    assert dll.tail.value == 2

    dll.push_front(1)

    assert dll.tail.value == 1


@pytest.mark.order4
def test_size(dll):
    assert len(dll) == 4


@pytest.mark.order5
def test_iterator_exception(dll):
    with pytest.raises(KeyError):
        _ = dll.value


@pytest.mark.order6
def test_iterator(dll):
    dll.pointer = dll.head
    assert dll.value == 6


@pytest.mark.order7
@pytest.mark.parametrize('value', [6, 5, 2, 1])
def test_iterator_iteration_back(dll, value):
    assert dll.value == value
    dll.previous()

