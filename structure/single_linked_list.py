class SingleLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        nval = self.next.value if self.next is not None else None
        return f"{self.value} -> {repr(nval)}"


class SingleLinkedList(object):
    def __init__(self):
        self.begin = None

    def append(self, value):
        node = SingleLinkedListNode(value)
        if self.begin is None:
            self.begin = node
            return node

        current = self.begin
        while current.next is not None:
            current = current.next
        current.next = node
        return node

    def to_list(self):
        values = []
        current = self.begin
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def show_last(self):
        if self.begin is None:
            return "There are no data here"

        temp = self.begin
        while temp.next is not None:
            temp = temp.next
        return temp.value