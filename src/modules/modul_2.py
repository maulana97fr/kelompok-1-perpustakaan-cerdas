# modul2_stack.py
# Deskripsi: Stack berbasis Linked List untuk log transaksi global dan mekanisme undo

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if self.top is None:
            return None
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
