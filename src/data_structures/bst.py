class Node:
    def __init__(self, isbn, judul, pengarang, status):
        self.isbn = isbn
        self.judul = judul
        self.pengarang = pengarang
        self.status = status
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, isbn, judul, pengarang, status=0):
        new_node = Node(isbn, judul, pengarang, status)
        if self.root is None:
            self.root = new_node
            return
        
        current = self.root
        while True:
            if isbn < current.isbn:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right

    def search(self, node, isbn):
        if node is None or node.isbn == isbn:
            return node
        
        if isbn < node.isbn:
            return self.search(node.left, isbn)
        return self.search(node.right, isbn)

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node)
            self._inorder(node.right, hasil)

    def inorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil