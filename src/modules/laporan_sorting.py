import numpy as np
import time
import random

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

from modules.laporan_sorting import *

np.random.seed(13)
random.seed(13)

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']

STATUS = {'TERSEDIA': 0,'DIPINJAM': 1,'DIPESAN': 2}

# DATA CLASS

@dataclass
class Buku:
    isbn: str
    judul: str
    pengarang: str
    kategori: str
    status: int = 0


@dataclass
class Peminjaman:
    transaksi_id: int
    anggota_id: str
    isbn: str
    tgl_pinjam: float
    durasi_hari: int = 14


# LINKED LIST NODE

class LLNode:

    def __init__(self, data=None):

        self.data = data
        self.next = None


# QUEUE

class Queue:
    """FIFO Queue untuk antrian pemesanan buku."""

    def __init__(self):

        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, data):
        """Big-O: O(1)"""

        new_node = LLNode(data)

        if self.tail is None:

            self.head = new_node
            self.tail = new_node

        else:

            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def dequeue(self):
        """Big-O: O(1)"""

        if self.head is None:

            return None

        data = self.head.data

        self.head = self.head.next

        if self.head is None:

            self.tail = None

        self._size -= 1

        return data

    def is_empty(self):

        return self._size == 0

    def __len__(self):

        return self._size


# STACK

class Stack:

    def __init__(self):

        self.top = None
        self._size = 0

    def push(self, data):
        """Big-O: O(1)"""

        new_node = LLNode(data)

        new_node.next = self.top

        self.top = new_node

        self._size += 1

    def pop(self):
        """Big-O: O(1)"""

        if self.top is None:

            return None

        data = self.top.data

        self.top = self.top.next

        self._size -= 1

        return data

    def peek(self):

        return self.top.data if self.top else None

    def is_empty(self):

        return self._size == 0


# BST NODE

class BSTNode:

    def __init__(self, buku):

        self.buku = buku
        self.left = None
        self.right = None


# BST KATALOG

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

        else:

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

    def update_status(self, isbn, status):

        buku = self.search(isbn)

        if buku:

            buku.status = status

    def inorder(self):

        hasil = []

        self._inorder(self.root, hasil)

        return hasil

    def _inorder(self, node, hasil):

        if node:

            self._inorder(node.left, hasil)

            hasil.append(node.buku)

            self._inorder(node.right, hasil)


# GRAPH REKOMENDASI

class GraphRekBuku:

    def __init__(self):

        self.adj = {}

    def add_copinjam(self, isbn_a, isbn_b):

        if isbn_a not in self.adj:

            self.adj[isbn_a] = []

        self.adj[isbn_a].append(isbn_b)

    def rekomendasikan(self, isbn, max_hop=2):

        if isbn not in self.adj:

            return []

        visited = set()

        q = Queue()

        q.enqueue((isbn, 0))

        visited.add(isbn)

        hasil = []

        while not q.is_empty():

            current, level = q.dequeue()

            if level >= max_hop:

                continue

            for tetangga in self.adj.get(current, []):

                if tetangga not in visited:

                    visited.add(tetangga)

                    hasil.append(tetangga)

                    q.enqueue((tetangga, level + 1))

        return hasil


# GENERATE KOLEKSI

def generate_koleksi(n=80):

    kata = ['Algoritma','Jaringan','Python','Data','Digital','Sistem','Kontrol','Sinyal','Elektronika','Fisika']

    return [

        Buku(
            f'ISBN-{i:04d}',
            f'{random.choice(kata)} Vol.{i}',
            f'Penulis-{random.randint(1,20)}',
            random.choice(KATEGORI)
        )

        for i in range(1, n+1)
    ]


# MAIN PROGRAM

def main():

    bst = BSTKatalog()

    antrian_pesan = {}

    riwayat_global = Stack()

    graf_rek = GraphRekBuku()

    tx_counter = 0

    for buku in generate_koleksi(80):

        bst.insert(buku)

        antrian_pesan[buku.isbn] = Queue()

    print('Smart Library System')
    print('Ketik BANTUAN untuk daftar perintah')

    while True:

        cmd = input('\n>> ').split()

        if len(cmd) == 0:

            continue

        perintah = cmd[0].upper()

        # KATALOG

        if perintah == 'KATALOG':

            data = bst.inorder()

            print('\n=== DAFTAR BUKU ===')

            for buku in data:

                print(
                    buku.isbn,
                    '|',
                    buku.judul,
                    '|',
                    buku.kategori,
                    '|',
                    buku.status
                )

        # CARI BUKU

        elif perintah == 'CARI_BUKU':

            if len(cmd) < 2:

                print('Format salah')
                continue

            isbn = cmd[1]

            buku = bst.search(isbn)

            if buku:

                print('\n=== DATA BUKU ===')

                print('ISBN      :', buku.isbn)
                print('Judul     :', buku.judul)
                print('Pengarang :', buku.pengarang)
                print('Kategori  :', buku.kategori)
                print('Status    :', buku.status)

            else:

                print('Buku tidak ditemukan')

        # PINJAM
        
        elif perintah == 'PINJAM':

            if len(cmd) < 3:

                print('Format salah')
                continue

            nim = cmd[1]
            isbn = cmd[2]

            buku = bst.search(isbn)

            if buku is None:

                print('Buku tidak ditemukan')

            elif buku.status == STATUS['TERSEDIA']:

                bst.update_status(isbn, STATUS['DIPINJAM'])

                tx_counter += 1

                trx = Peminjaman(
                    tx_counter,
                    nim,
                    isbn,
                    time.time()
                )

                riwayat_global.push(trx)

                print('Peminjaman berhasil')

            else:

                print('Buku sedang dipinjam')

        # KEMBALIKAN

        elif perintah == 'KEMBALIKAN':

            if len(cmd) < 2:

                print('Format salah')
                continue

            isbn = cmd[1]

            buku = bst.search(isbn)

            if buku:

                bst.update_status(isbn, STATUS['TERSEDIA'])

                print('Pengembalian berhasil')

            else:

                print('Buku tidak ditemukan')

        # PESAN

        elif perintah == 'PESAN':

            if len(cmd) < 3:

                print('Format salah')
                continue

            nim = cmd[1]
            isbn = cmd[2]

            if isbn in antrian_pesan:

                antrian_pesan[isbn].enqueue(nim)

                print('Masuk antrian')

            else:

                print('ISBN tidak ditemukan')

        # ANTRIAN

        elif perintah == 'ANTRIAN':

            if len(cmd) < 2:

                print('Format salah')
                continue

            isbn = cmd[1]

            q = antrian_pesan.get(isbn)

            if q is None:

                print('ISBN tidak ditemukan')

            elif q.is_empty():

                print('Antrian kosong')

            else:

                cur = q.head

                print('\n=== ANTRIAN ===')

                while cur:

                    print(cur.data)

                    cur = cur.next

        # UNDO

        elif perintah == 'BATALKAN_TERAKHIR':

            trx = riwayat_global.pop()

            if trx is None:

                print('Tidak ada transaksi')

            else:

                bst.update_status(
                    trx.isbn,
                    STATUS['TERSEDIA']
                )

                print('Undo berhasil')

        # REKOMENDASI
    
        elif perintah == 'REKOMENDASI':

            if len(cmd) < 2:

                print('Format salah')
                continue

            isbn = cmd[1]

            hasil = graf_rek.rekomendasikan(isbn)

            print('\n=== REKOMENDASI ===')

            if len(hasil) == 0:

                print('Belum ada rekomendasi')

            else:

                for item in hasil:

                    print(item)

        # BANTUAN

        elif perintah == 'BANTUAN':

            print('\n=== DAFTAR PERINTAH ===')

            print('KATALOG')
            print('CARI_BUKU <isbn>')
            print('PINJAM <nim> <isbn>')
            print('KEMBALIKAN <isbn>')
            print('PESAN <nim> <isbn>')
            print('ANTRIAN <isbn>')
            print('BATALKAN_TERAKHIR')
            print('REKOMENDASI <isbn>')
            print('KELUAR')

        # KELUAR

        elif perintah == 'KELUAR':

            print('Program selesai')
            break

        else:

            print('Perintah tidak dikenal')


if __name__ == '__main__':

    main()