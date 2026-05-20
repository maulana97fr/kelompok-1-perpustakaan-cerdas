# main.py
# Deskripsi: Integrasi Utama CLI dan Inisialisasi Otomatis 300 Event Sistem

import numpy as np
import random
import time
from dataclasses import dataclass, field

# Import komponen dari modul-modul modular terpisah
from src.modules.modul1_queue import Queue
from src.modules.modul2_stack import Stack
from src.modules.modul3_bst import BSTKatalog, Buku
from src.modules.modul4_graph import GraphRekomendasi
from src.modules.modul5_sorting import shell_sort, merge_sort, bandingkan_runtime_spesifikasi
# =========================================================
# CONFIG PERPUSTAKAAN (SESUAI PARAMETER TOPIK 6)
# =========================================================
np.random.seed(13)
random.seed(13)

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']
STATUS = {'TERSEDIA': 0, 'DIPINJAM': 1, 'DIPESAN': 2}
STATUS_TEXT = {0: 'TERSEDIA', 1: 'DIPINJAM', 2: 'DIPESAN'}

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
            Buku(f'ISBN-{i:04d}', f'{random.choice(kata)} Vol.{i}', f'Penulis-{random.randint(1,20)}', random.choice(KATEGORI))
        )
    return hasil

def main():
    bst = BSTKatalog()
    stack_undo = Stack()
    graph = GraphRekomendasi()
    antrian = {}
    transaksi = []
    histori_pinjam = []

    # Anggota 60 orang berformat NIM
    anggota = [f'24{str(i).zfill(8)}' for i in range(1, 61)]

    for b in generate_koleksi(80):
        bst.insert(b)
        antrian[b.isbn] = Queue()

    # -----------------------------------------------------
    # AUTOMATION GENERATOR: WAJIB MINIMAL 300 EVENT CAMPURAN
    # -----------------------------------------------------
    print("Memuat rancangan parameter sistem...")
    print("Mengeksekusi simulasi 300 event campuran secara otomatis...")
    for _ in range(300):
        act = random.choice(['PINJAM', 'PESAN'])
        nim_rand = random.choice(anggota)
        isbn_rand = f'ISBN-{random.randint(1, 80):04d}'
        buku_rand = bst.search(isbn_rand)
        
        if buku_rand:
            if act == 'PINJAM' and buku_rand.status == STATUS['TERSEDIA']:
                buku_rand.status = STATUS['DIPINJAM']
                buku_rand.frek_pinjam += 1
                durasi = random.choice([7, 10, 14, 21, 30])
                transaksi.append(Peminjaman(len(transaksi)+1, nim_rand, isbn_rand, durasi_hari=durasi))
                histori_pinjam.append(isbn_rand)
                if len(histori_pinjam) >= 2:
                    graph.add_edge(histori_pinjam[-1], histori_pinjam[-2])
            elif act == 'PESAN':
                antrian[isbn_rand].enqueue(nim_rand)
    print("Inisialisasi 300 event selesai dimasukkan ke sistem.")

    print('\nSMART LIBRARY SYSTEM CLI')
    print('Ketik BANTUAN untuk melihat menu perintah')

    while True:
        try:
            cmd = input('\n>> ').strip().split()
        except (KeyboardInterrupt, EOFError):
            break

        if len(cmd) == 0: continue
        perintah = cmd[0].upper()

        if perintah == 'BANTUAN':
            print('\n=== PERINTAH CLI PERPUSTAKAAN ===')
            print('CARI_BUKU <isbn> | PINJAM <nim> <isbn> | KEMBALIKAN <isbn>')
            print('PESAN <nim> <isbn> | BATALKAN_PESAN <nim> <isbn> | ANTRIAN <isbn>')
            print('DELETE <isbn> | KATALOG | REKOMENDASI <isbn> | LAPORAN_BULAN')
            print('BATALKAN_TERAKHIR | KELUAR')

        elif perintah == 'CARI_BUKU':
            if len(cmd) < 2: print('Format salah'); continue
            isbn = cmd[1].upper()
            buku = bst.search(isbn)
            if buku:
                print(f'\n=== DATA BUKU ===\nISBN: {buku.isbn}\nJudul: {buku.judul}\nPengarang: {buku.pengarang}\nKategori: {buku.kategori}\nStatus: {STATUS_TEXT[buku.status]}')
                print('Big-O search BST = O(log n)')
            else:
                print('Buku tidak ditemukan')

        elif perintah == 'PINJAM':
            if len(cmd) < 3: print('Format salah'); continue
            nim, isbn = cmd[1], cmd[2].upper()
            buku = bst.search(isbn)
            if buku and buku.status == STATUS['TERSEDIA']:
                buku.status = STATUS['DIPINJAM']
                buku.frek_pinjam += 1
                durasi = random.choice([7, 14, 21, 30])
                transaksi.append(Peminjaman(len(transaksi)+1, nim, isbn, durasi_hari=durasi))
                stack_undo.push(('PINJAM', isbn))
                histori_pinjam.append(isbn)
                if len(histori_pinjam) >= 2: graph.add_edge(histori_pinjam[-1], histori_pinjam[-2])
                print('Peminjaman sukses.')
                print('Big-O BST Search = O(log n)')
            else:
                print('Buku tidak tersedia/tidak ditemukan')

        elif perintah == 'KEMBALIKAN':
            if len(cmd) < 2: print('Format salah'); continue
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
            if len(cmd) < 3: print('Format salah'); continue
            nim, isbn = cmd[1], cmd[2].upper()
            if isbn in antrian:
                antrian[isbn].enqueue(nim)
                stack_undo.push(('PESAN', nim, isbn))
                print('Masuk antrian pemesanan')
                print('Big-O Queue enqueue = O(1)')
            else:
                print('ISBN salah')

        elif perintah == 'BATALKAN_PESAN':
            if len(cmd) < 3: print('Format salah'); continue
            nim, isbn = cmd[1], cmd[2].upper()
            if isbn in antrian and antrian[isbn].batal_pesan(nim):
                print('Pesanan dibatalkan')
            else:
                print('Data tidak ditemukan')

        elif perintah == 'ANTRIAN':
            if len(cmd) < 2: print('Format salah'); continue
            isbn = cmd[1].upper()
            if isbn in antrian:
                data = antrian[isbn].tampil()
                print(f'\n=== ANTRIAN {isbn} ===')
                if not data: print('Kosong')
                for i, item in enumerate(data, start=1): print(i, item)
                print('Big-O Queue traversal = O(n)')

        elif perintah == 'DELETE':
            if len(cmd) < 2: print('Format salah'); continue
            isbn = cmd[1].upper()
            if bst.delete(isbn):
                print('Buku sukses dihapus dari katalog BST.'); print('Big-O delete BST = O(log n)')
            else:
                print('Buku tidak ditemukan')

        elif perintah == 'KATALOG':
            print('\n=== KATALOG BUKU ===')
            for b in bst.inorder():
                print(f"{b.isbn} | {b.judul[:20].ljust(20)} | {b.kategori} | {STATUS_TEXT[b.status]}")
            print('Big-O inorder BST = O(n)')

        elif perintah == 'REKOMENDASI':
            if len(cmd) < 2:
