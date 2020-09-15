from typing import Any, Union, Optional


class Node:
    def __init__(self, data: Any = None):
        self.__data = data
        self.__next = None
        self.__previous = None


    @property
    def value(self) -> Any:
        return self.__data


    @property
    def next(self) -> Union["Node", None]:
        return self.__next


    @next.setter
    def next(self, value: "Node"):
        self.__next = value


    @property
    def previous(self) -> Union["Node", None]:
        return self.__previous


    @previous.setter
    def previous(self, value: "Node"):
        self.__previous = value


class DoubleLinkedList:
    """ Structure for store double linked list"""


    def __init__(self):
        self.__head = None  # type: Optional[Node]
        self.__tail = None  # type: Optional[Node]
        self.__pointer = None  # type: Optional[Node]
        self.__size = 0  # type: int


    def push_back(self, value: Any) -> None:
        """ Push value to the end of the linked list"""
        node = Node(value)

        if self.__size == 0:
            self.__head = node
            self.__tail = node
        else:
            node.previous = self.__head
            node.previous.next = node
            self.__head = node

        self.__size += 1


    def push_front(self, value: Any) -> None:
        """ Push value to the start of the linked list"""
        node = Node(value)

        if self.__size == 0:
            self.__head = node
            self.__tail = node
        else:
            node.next = self.__tail
            node.next.previous = node
            self.__tail = node

        self.__size += 1


    def empty(self) -> bool:
        """ Determinate if linked list is empty """
        return self.__size == 0


    @property
    def head(self) -> "Node":
        """ Get reference to head Node """
        return self.__head


    @property
    def tail(self) -> "Node":
        """ Get reference to tail Node"""
        return self.__tail


    @property
    def value(self) -> Any:
        """ Return value of the pointer Node. Raise exception if pointer is not set """
        if self.__pointer is None:
            raise KeyError('Pointer not set')
        return self.__pointer.value


    def next(self):
        """ Move pointer to the next Node """
        self.__pointer = self.__pointer.next


    def previous(self):
        """ Move pointer to the previous Node """
        self.__pointer = self.__pointer.previous


    @property
    def pointer(self):
        """ Get pointed Node reference """
        return self.__pointer


    @pointer.setter
    def pointer(self, target: Node):
        """ SEt pointer to target node"""
        self.__pointer = target


    def __len__(self):
        return self.__size


    def __bool__(self):
        return not self.empty()
