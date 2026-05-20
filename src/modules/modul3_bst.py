# modul3_bst.py
# Deskripsi: BST dengan kunci ISBN untuk pencarian, insert, dan delete katalog buku
from src.data_structures.bst import BinarySearchTree
from dataclasses import dataclass

@dataclass
class Buku:
    isbn: str
    judul: str
    pengarang: str
    kategori: str
    status: int = 0
    frek_pinjam: int = 0

class BSTNode:
    def __init__(self, buku):
        self.buku = buku
        self.left = None
        self.right = None

class BSTKatalog:
    def __init__(self):
        self.root = None

    def insert(self, buku):
        self.root = self._insert(self.root, buku)

    def _insert(self, node, buku):
        if node is None:
            return BSTNode(buku)
        if buku.isbn < node.buku.isbn:
            node.left = self._insert(node.left, buku)
        elif buku.isbn > node.buku.isbn:
            node.right = self._insert(node.right, buku)
        return node

    def search(self, isbn):
        return self._search(self.root, isbn)

    def _search(self, node, isbn):
        if node is None:
            return None
        if isbn == node.buku.isbn:
            return node.buku
        if isbn < node.buku.isbn:
            return self._search(node.left, isbn)
        return self._search(node.right, isbn)

    def inorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.buku)
            self._inorder(node.right, hasil)

    def delete(self, isbn):
        self.root, deleted = self._delete(self.root, isbn)
        return deleted

    def _delete(self, node, isbn):
        if node is None:
            return node, False
        if isbn < node.buku.isbn:
            node.left, deleted = self._delete(node.left, isbn)
            return node, deleted
        elif isbn > node.buku.isbn:
            node.right, deleted = self._delete(node.right, isbn)
            return node, deleted
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            successor = self._min_value(node.right)
            node.buku = successor.buku
            node.right, _ = self._delete(node.right, successor.buku.isbn)
            return node, True

    def _min_value(self, node):
        current = node
        while current.left:
            current = current.left
        return current
