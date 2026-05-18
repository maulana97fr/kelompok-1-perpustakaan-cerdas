# src/main.py
# File utama untuk running program CLI
import random

random.seed(13)

class LLNode:
    """Single node for the manual Linked List."""
    def __init__(self, value=None, next_node=None):
        self.value = value
        self.next = next_node

class Stack:
    """Stack implementation using a Linked List with O(1) operations."""
    def __init__(self):
        self.top = None
        self._size = 0

    def is_empty(self):
        return self.top is None

    def push(self, value):
        """Add an element to the top of the stack."""
        self.top = LLNode(value, self.top)
        self._size += 1

    def pop(self):
        """Remove and return the top element from the stack."""
        if self.is_empty():
            return None
        node = self.top
        self.top = node.next
        self._size -= 1
        return node.value

    def peek(self):
        return None if self.is_empty() else self.top.value

    def __len__(self):
        return self._size

def fitur_undo(undo_stack):
    """Undo Function: Reverts the last transaction and updates availability."""
    transaksi = undo_stack.pop()
    if transaksi is None:
        return None

    tipe = None
    node = None
    if isinstance(transaksi, dict):
        tipe = transaksi.get("tipe")
        node = transaksi.get("node")
    elif isinstance(transaksi, (tuple, list)) and len(transaksi) >= 2:
        tipe, node = transaksi[0], transaksi[1]

    if tipe == "PINJAM" and node is not None and hasattr(node, "tersedia"):
        node.tersedia = True

    return transaksi
    
if __name__ == "__main__":
<<<<<<< HEAD
    main()
    
=======
    class Buku:
        def __init__(self, judul):
            self.judul = judul
            self.tersedia = False

    undo_stack = Stack()
    buku_test = Buku("Harry Potter")

    # Display status before Undo
    print(f"\n[!] Before Undo: {buku_test.judul} | tersedia = {buku_test.tersedia}")

    # Push the transaction into the Stack
    undo_stack.push({"tipe": "PINJAM", "node": buku_test, "judul": buku_test.judul})

    # Execute Undo
    print("--- Running Undo Feature ---")
    fitur_undo(undo_stack)

    # Display status after Undo
    print(f"[!] After Undo: {buku_test.judul} | tersedia = {buku_test.tersedia}\n")
>>>>>>> f33c5047b4fffb3913a4d2a6c0b5ee367a4bd72c
