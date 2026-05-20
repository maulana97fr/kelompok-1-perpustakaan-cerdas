class Buku:
    def __init__(self, isbn, judul, pengarang, kategori):
        self.isbn = isbn
        self.judul = judul
        self.pengarang = pengarang
        self.kategori = kategori
        self.status = 0  # 0: TERSEDIA, 1: DIPINJAM, 2: DIPESAN
        self.frek_pinjam = 0
        self.left = None
        self.right = None

class BSTKatalog:
    def __init__(self):
        self.root = None

    def insert(self, b):
        self.root = self._insert_rec(self.root, b)

    def _insert_rec(self, root, b):
        if root is None:
            return b
        if b.isbn < root.isbn:
            root.left = self._insert_rec(root.left, b)
        elif b.isbn > root.isbn:
            root.right = self._insert_rec(root.right, b)
        return root

    def search(self, isbn):
        return self._search_rec(self.root, isbn)

    def _search_rec(self, root, isbn):
        if root is None or root.isbn == isbn:
            return root
        if isbn < root.isbn:
            return self._search_rec(root.left, isbn)
        return self._search_rec(root.right, isbn)

    def delete(self, isbn):
        self.root, success = self._delete_rec(self.root, isbn)
        return success

    def _delete_rec(self, root, isbn):
        if root is None:
            return root, False
        success = False
        if isbn < root.isbn:
            root.left, success = self._delete_rec(root.left, isbn)
        elif isbn > root.isbn:
            root.right, success = self._delete_rec(root.right, isbn)
        else:
            success = True
            if root.left is None:
                return root.right, success
            elif root.right is None:
                return root.left, success
            temp = self._min_node(root.right)
            root.isbn, root.judul, root.pengarang, root.kategori = temp.isbn, temp.judul, temp.pengarang, temp.kategori
            root.status, root.frek_pinjam = temp.status, temp.frek_pinjam
            root.right, _ = self._delete_rec(root.right, temp.isbn)
        return root, success

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        books = []
        self._inorder_rec(self.root, books)
        return books

    def _inorder_rec(self, root, books):
        if root:
            self._inorder_rec(root.left, books)
            books.append(root)
            self._inorder_rec(root.right, books)