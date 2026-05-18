# src/modules/katalog_bst.py

class BSTNode:
    def __init__(self, buku):
        self.buku = buku  # Menyimpan objek Buku dari starter code dosen
        self.left = None
        self.right = None

class BSTKatalog:
    def __init__(self):
        self.root = None

    def insert(self, buku):
        """Big-O: O(log n) rata-rata. Kunci = buku.isbn."""
        new_node = BSTNode(buku)
        if self.root is None:
            self.root = new_node
            return
        
        current = self.root
        while True:
            # Membandingkan string ISBN (misal: 'ISBN-0001' < 'ISBN-0005')
            if buku.isbn < current.buku.isbn:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            elif buku.isbn > current.buku.isbn:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right
            else:
                # Jika ISBN sudah ada di pohon, tidak perlu dimasukkan lagi
                break

    def search(self, isbn):
        """Big-O: O(log n) rata-rata."""
        current = self.root
        while current:
            if isbn == current.buku.isbn:
                return current.buku  # Mengembalikan objek Buku jika ditemukan
            elif isbn < current.buku.isbn:
                current = current.left
            else:
                current = current.right
        return None

    def update_status(self, isbn, status_baru):
        """Big-O: O(log n) rata-rata. Mencari node lalu update status"""
        current = self.root
        while current:
            if isbn == current.buku.isbn:
                # Validasi sesuai aturan dosen (0=TERSEDIA, 1=DIPINJAM, 2=DIPESAN)
                if status_baru in [0, 1, 2]:
                    current.buku.status = status_baru
                    return True
                return False
            elif isbn < current.buku.isbn:
                current = current.left
            else:
                current = current.right
        return False

    def inorder(self):
        """Big-O: O(n). Kembalikan list buku terurut ISBN."""
        res = []
        self._helper_inorder(self.root, res)
        return res

    def _helper_inorder(self, node, res):
        """Fungsi pembantu rekursif untuk melakukan In-order Traversal"""
        if node:
            self._helper_inorder(node.left, res)
            res.append(node.buku)
            self._helper_inorder(node.right, res)