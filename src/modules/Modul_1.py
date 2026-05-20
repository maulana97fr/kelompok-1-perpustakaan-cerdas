# modul1_queue.py
# Deskripsi: Queue berbasis Linked List per-buku untuk antrean pemesanan

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def batal_pesan(self, nim):
        prev = None
        cur = self.head
        while cur:
            if cur.data == nim:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur == self.tail:
                    self.tail = prev
                self.size -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def tampil(self):
        hasil = []
        cur = self.head
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil
