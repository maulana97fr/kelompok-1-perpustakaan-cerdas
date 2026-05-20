import numpy as np
import random
import time
from dataclasses import dataclass, field
from typing import List

# =========================================================
# CONFIG & PARAMETER SISTEM
# =========================================================
np.random.seed(13)
random.seed(13)

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']
STATUS = {
    'TERSEDIA': 0,
    'DIPINJAM': 1,
    'DIPESAN': 2
}

STATUS_TEXT = {
    0: 'TERSEDIA',
    1: 'DIPINJAM',
    2: 'DIPESAN'
}

# =========================================================
# MODUL 1: QUEUE ANTREAN PEMESANAN (LINKED LIST)
# =========================================================
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


# =========================================================
# MODUL 2: STACK RIWAYAT TRANSAKSI & UNDO (LINKED LIST)
# =========================================================
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


# =========================================================
# MODUL 3: BST KATALOG BUKU
# =========================================================
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


# =========================================================
# MODUL 4: GRAPH REKOMENDASI KO-PINJAM (BFS)
# =========================================================
class GraphRekomendasi:
    def __init__(self):
        self.adj = {}

    def add_edge(self, a, b):
        if a == b:
            return
        if a not in self.adj:
            self.adj[a] = []
        if b not in self.adj:
            self.adj[b] = []

        found = False
        for i, (isbn, bobot) in enumerate(self.adj[a]):
            if isbn == b:
                self.adj[a][i] = (isbn, bobot + 1)
                found = True
                break
        if not found:
            self.adj[a].append((b, 1))

        found = False
        for i, (isbn, bobot) in enumerate(self.adj[b]):
            if isbn == a:
                self.adj[b][i] = (isbn, bobot + 1)
                found = True
                break
        if not found:
            self.adj[b].append((a, 1))

    def bfs_rekomendasi(self, start, max_hop=2):
        if start not in self.adj:
            return []
        visited = set([start])
        queue = [(start, 0)]
        hasil = []
        while queue:
            current, level = queue.pop(0)
            if level >= max_hop:
                continue
            for tetangga, bobot in self.adj[current]:
                if tetangga not in visited:
                    visited.add(tetangga)
                    hasil.append((tetangga, bobot))
                    queue.append((tetangga, level + 1))
        hasil.sort(key=lambda x: x[1], reverse=True)
        return hasil


# =========================================================
# MODUL 5: SORTING LAPORAN BULANAN & RUNTIME COMPARISON
# =========================================================
def shell_sort(data):
    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            while j >= gap and data[j-gap].durasi_hari < temp.durasi_hari:
                data[j] = data[j-gap]
                j -= gap
            data[j] = temp
        gap //= 2
    return data

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    hasil = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i].frek_pinjam > right[j].frek_pinjam:
            hasil.append(left[i])
            i += 1
        else:
            hasil.append(right[j])
            j += 1
    hasil.extend(left[i:])
    hasil.extend(right[j:])
    return hasil

def bandingkan_runtime(transaksi_list, bst_data):
    print("\n--- ANALISIS RUNTIME SORTING (N = 20, 80, 300) ---")
    skala_n = [20, 80, 300]
    
    # Cetak header tabel
    print(f"{'N':<6} | {'Shell Sort (Durasi)':<25} | {'Merge Sort (Populer)':<25}")
    print("-" * 62)
    
    for n in skala_n:
        # Dummy generator data sesuai ukuran sampel N
        sample_shell = []
        for k in range(n):
            sample_shell.append(Peminjaman(k, f"NIM-{k}", f"ISBN-{k}", durasi_hari=random.randint(1, 30)))
            
        sample_merge = []
        for k in range(n):
            b = Buku(f"ISBN-{k}", f"Buku-{k}", f"Author-{k}", "Sains")
            b.frek_pinjam = random.randint(0, 50)
            sample_merge.append(b)
            
        # Hitung waktu Shell Sort
        t0 = time.perf_counter()
        shell_sort(sample_shell.copy())
        t_shell = (time.perf_counter() - t0) * 1000 # convert ke ms
        
        # Hitung waktu Merge Sort
        t1 = time.perf_counter()
        merge_sort(sample_merge.copy())
        t_merge = (time.perf_counter() - t1) * 1000 # convert ke ms
        
        print(f"{n:<6} | {t_shell:.4f} ms".ljust(33) + f" | {t_merge:.4f} ms")


# =========================================================
# DATA GENERATOR (PENUNJANG PARAMETER)
# =========================================================
@dataclass
class Peminjaman:
    transaksi_id: int
    nim: str
    isbn: str
    waktu: float = field(default_factory=time.time)
    durasi_hari: int = 14

def generate_koleksi(n=80):
    kata = ['Algoritma', 'Jaringan', 'Python', 'Data', 'Digital', 'Sistem', 'Kontrol', 'Sinyal', 'Elektronika', 'Fisika']
    hasil = []
    for i in range(1, n+1):
        hasil.append(
            Buku(
                f'ISBN-{i:04d}',
                f'{random.choice(kata)} Vol.{i}',
                f'Penulis-{random.randint(1,20)}',
                random.choice(KATEGORI)
            )
        )
    return hasil


# =========================================================
# MODUL 6: CLI PERPUSTAKAAN & MAIN CONTROL
# =========================================================
def main():
    bst = BSTKatalog()
    stack_undo = Stack()
    graph = GraphRekomendasi()
    antrian = {}
    transaksi = []
    histori_pinjam = []

    anggota = [f'24{str(i).zfill(8)}' for i in range(1,61)]

    for buku in generate_koleksi(80):
        bst.insert(buku)
        antrian[buku.isbn] = Queue()

    # -----------------------------------------------------
    # OTOMATISASI PARAMETER SISTEM: MINIMUM 300 EVENT CAMPURAN
    # -----------------------------------------------------
    print("Memproses inisialisasi parameter sistem...")
    print("Mengeksekusi otomatis 300 event campuran sesuai rancangan dokumen...")
    for _ in range(300):
        action = random.choice(['PINJAM', 'PESAN'])
        nim_dummy = random.choice(anggota)
        isbn_dummy = f'ISBN-{random.randint(1, 80):04d}'
        buku_dummy = bst.search(isbn_dummy)
        
        if buku_dummy:
            if action == 'PINJAM' and buku_dummy.status == STATUS['TERSEDIA']:
                buku_dummy.status = STATUS['DIPINJAM']
                buku_dummy.frek_pinjam += 1
                durasi_acak = random.choice([7, 10, 14, 21, 30])
                trx = Peminjaman(len(transaksi)+1, nim_dummy, isbn_dummy, durasi_hari=durasi_acak)
                transaksi.append(trx)
                histori_pinjam.append(isbn_dummy)
                if len(histori_pinjam) >= 2:
                    graph.add_edge(histori_pinjam[-1], histori_pinjam[-2])
            elif action == 'PESAN':
                antrian[isbn_dummy].enqueue(nim_dummy)
    print("Inisialisasi selesai. Sistem siap digunakan.\n")

    print('SMART LIBRARY MANAGEMENT & RECOMMENDATION SYSTEM')
    print('Ketik BANTUAN untuk melihat instruksi operasional')

    while True:
        try:
            cmd = input('\n>> ').strip().split()
        except (KeyboardInterrupt, EOFError):
            print('\nProgram selesai')
            break

        if len(cmd) == 0:
            continue

        perintah = cmd[0].upper()

        if perintah == 'BANTUAN':
            print('\n=== DAFTAR PERINTAH ===')
            print('CARI_BUKU <isbn>')
            print('PINJAM <nim> <isbn>')
            print('KEMBALIKAN <isbn>')
            print('PESAN <nim> <isbn>')
            print('BATALKAN_PESAN <nim> <isbn>')
            print('ANTRIAN <isbn>')
            print('DELETE <isbn>')
            print('KATALOG')
            print('REKOMENDASI <isbn>')
            print('LAPORAN_BULAN')
            print('BATALKAN_TERAKHIR')
            print('KELUAR')

        elif perintah == 'CARI_BUKU':
            if len(cmd) < 2:
                print('Format salah. Contoh: CARI_BUKU ISBN-0005')
                continue
            isbn = cmd[1].upper()
            buku = bst.search(isbn)
            if buku:
                print('\n=== DATA BUKU ===')
                print('ISBN      :', buku.isbn)
                print('Judul     :', buku.judul)
                print('Pengarang :', buku.pengarang)
                print('Kategori  :', buku.kategori)
                print('Status    :', STATUS_TEXT[buku.status])
                print('Big-O search BST = O(log n)')
            else:
                print('Buku tidak ditemukan')

        elif perintah == 'PINJAM':
            if len(cmd) < 3:
                print('Format salah. Contoh: PINJAM 2400000001 ISBN-0005')
                continue
            nim, isbn = cmd[1], cmd[2].upper()
            buku = bst.search(isbn)

            if buku is None:
                print('Buku tidak ditemukan')
                continue

            if buku.status == STATUS['TERSEDIA']:
                buku.status = STATUS['DIPINJAM']
                buku.frek_pinjam += 1
                durasi_acak = random.choice([7, 14, 21, 30])
                trx = Peminjaman(len(transaksi)+1, nim, isbn, durasi_hari=durasi_acak)
                transaksi.append(trx)
                stack_undo.push(('PINJAM', isbn))
                histori_pinjam.append(isbn)
                if len(histori_pinjam) >= 2:
                    graph.add_edge(histori_pinjam[-1], histori_pinjam[-2])
                print(f'Peminjaman Berhasil! Durasi: {durasi_acak} hari.')
                print('Big-O BST Search = O(log n)')
            else:
                print('Buku tidak tersedia')

        elif perintah == 'KEMBALIKAN':
            if len(cmd) < 2:
                print('Format salah')
                continue
            isbn = cmd[1].upper()
            buku = bst.search(isbn)
            if buku:
                buku.status = STATUS['TERSEDIA']
                stack_undo.push(('KEMBALIKAN', isbn))
                print('Buku berhasil dikembalikan')
                print('Big-O update BST = O(log n)')
            else:
                print('Buku tidak ditemukan')

        elif perintah == 'PESAN':
            if len(cmd) < 3:
                print('Format salah')
                continue
            nim, isbn = cmd[1], cmd[2].upper()
            if isbn not in antrian:
                print('ISBN tidak ditemukan')
                continue
            antrian[isbn].enqueue(nim)
            stack_undo.push(('PESAN', nim, isbn))
            print('Masuk antrian pemesanan')
            print('Big-O Queue enqueue = O(1)')

        elif perintah == 'BATALKAN_PESAN':
            if len(cmd) < 3:
                print('Format salah')
                continue
            nim, isbn = cmd[1], cmd[2].upper()
            if isbn not in antrian:
                print('ISBN tidak ditemukan')
                continue
            sukses = antrian[isbn].batal_pesan(nim)
            if sukses:
                print('Pesanan dibatalkan')
            else:
                print('Data tidak ditemukan')

        elif perintah == 'ANTRIAN':
            if len(cmd) < 2:
                print('Format salah')
                continue
            isbn = cmd[1].upper()
            if isbn not in antrian:
                print('ISBN tidak ditemukan')
                continue
            data = antrian[isbn].tampil()
            print('\n=== ANTRIAN ===')
            if len(data) == 0:
                print('Kosong')
            else:
                for i, item in enumerate(data, start=1):
                    print(i, item)
            print('Big-O Queue traversal = O(n)')

        elif perintah == 'DELETE':
            if len(cmd) < 2:
                print('Format salah')
                continue
            isbn = cmd[1].upper()
            sukses = bst.delete(isbn)
            if sukses:
                print('Buku berhasil dihapus')
                print('Big-O delete BST = O(log n)')
            else:
                print('Buku tidak ditemukan')

        elif perintah == 'KATALOG':
            print('\n=== KATALOG BUKU ===')
            data = bst.inorder()
            for b in data:
                print(b.isbn, '|', b.judul[:20].ljust(20), '|', b.kategori, '|', STATUS_TEXT[b.status])
            print('Big-O inorder BST = O(n)')

        elif perintah == 'REKOMENDASI':
            if len(cmd) < 2:
                print('Format salah')
                continue
            isbn = cmd[1].upper()
            hasil = graph.bfs_rekomendasi(isbn)
            print('\n=== REKOMENDASI ===')
            if len(hasil) == 0:
                print('Belum ada rekomendasi pola ko-pinjam.')
            else:
                for rec, skor in hasil[:5]:
                    buku = bst.search(rec)
                    if buku:
                        print(rec, '|', buku.judul, '| skor hubungan =', skor)
            print('Big-O BFS = O(V+E)')

        elif perintah == 'LAPORAN_BULAN':
            print('\n=== LAPORAN BULANAN ===')
            shell_data = shell_sort(transaksi.copy())
            merge_data = merge_sort(bst.inorder())
            
            print('\nTop transaksi durasi (Shell Sort):')
            for trx in shell_data[:5]:
                print(f"NIM: {trx.nim} | ISBN: {trx.isbn} | Durasi: {trx.durasi_hari} hari")

            print('\nTop buku populer (Merge Sort):')
            for b in merge_data[:5]:
                print(f"ISBN: {b.isbn} | {b.judul[:20].ljust(20)} | Frekuensi Pinjam: {b.frek_pinjam}")
            
            print('\nBig-O Shell Sort = ~O(n^1.5)')
            print('Big-O Merge Sort = O(n log n)')
            
            # Memenuhi spesifikasi perbandingan runtime N = 20, 80, 300
            bandingkan_runtime(transaksi, bst.inorder())

        elif perintah == 'BATALKAN_TERAKHIR':
            aksi = stack_undo.pop()
            if aksi is None:
                print('Stack kosong / Tidak ada riwayat aksi.')
            else:
                tipe_aksi = aksi[0]
                if tipe_aksi == 'PINJAM':
                    isbn = aksi[1]
                    buku = bst.search(isbn)
                    if buku:
                        buku.status = STATUS['TERSEDIA']
                        buku.frek_pinjam = max(0, buku.frek_pinjam - 1)
                elif tipe_aksi == 'KEMBALIKAN':
                    isbn = aksi[1]
                    buku = bst.search(isbn)
                    if buku:
                        buku.status = STATUS['DIPINJAM']
                elif tipe_aksi == 'PESAN':
                    nim, isbn = aksi[1], aksi[2]
                    antrian[isbn].batal_pesan(nim)
                print('Undo berhasil memulihkan kondisi:', aksi)
                print('Big-O Stack pop = O(1)')

        elif perintah == 'KELUAR':
            print('Program selesai')
            break
        else:
            print('Perintah tidak dikenal')

if __name__ == '__main__':
    main()
