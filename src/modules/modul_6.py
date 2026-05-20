# main.py
# Deskripsi: Integrasi sistem CLI Utama dan pengisian 300 data event simulasi operasional

import numpy as np
import random
import time
from dataclasses import dataclass, field

# Mengimpor modul-modul yang telah dipisahkan
from modul1_queue import Queue
from modul2_stack import Stack
from modul3_bst import BSTKatalog, Buku
from modul4_graph import GraphRekomendasi
from modul5_sorting import shell_sort, merge_sort

# =========================================================
# CONFIG & PARAMETER SISTEM (SESUAI GAMBAR BARU)
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
            Buku(
                f'ISBN-{i:04d}',
                f'{random.choice(kata)} Vol.{i}',
                f'Penulis-{random.randint(1,20)}',
                random.choice(KATEGORI)
            )
        )
    return hasil

def main():
    bst = BSTKatalog()
    stack_undo = Stack()
    graph = GraphRekomendasi()
    antrian = {}
    transaksi = []
    histori_pinjam = []

    # Format NIM untuk 60 anggota perpustakaan sesuai parameter tugas
    anggota = [f'24{str(i).zfill(8)}' for i in range(1, 61)]

    for buku in generate_koleksi(80):
        bst.insert(buku)
        antrian[buku.isbn] = Queue()

    # -----------------------------------------------------
    # OTOMATISASI PARAMETER SISTEM: GENERATE MINIMUM 300 EVENT CAMPURAN
    # -----------------------------------------------------
    print("Mempersiapkan parameter sistem...")
    print("Mengeksekusi otomatis 300 event campuran (Pinjam/Pesan) untuk inisialisasi...")
    for _ in range(300):
        action = random.choice(['PINJAM', 'PESAN'])
        nim_dummy = random.choice(anggota)
        isbn_dummy = f'ISBN-{random.randint(1, 80):04d}'
        buku_dummy = bst.search(isbn_dummy)
        
        if buku_dummy:
            if action == 'PINJAM' and buku_dummy.status == STATUS['TERSEDIA']:
                buku_dummy.status = STATUS['DIPINJAM']
                buku_dummy.frek_pinjam += 1
                # Memberikan variasi durasi acak agar sorting laporan berfungsi dengan baik
                durasi_acak = random.choice([7, 10, 14, 21, 30])
                trx = Peminjaman(len(transaksi)+1, nim_dummy, isbn_dummy, durasi_hari=durasi_acak)
                transaksi.append(trx)
                histori_pinjam.append(isbn_dummy)
                if len(histori_pinjam) >= 2:
                    graph.add_edge(histori_pinjam[-1], histori_pinjam[-2])
            elif action == 'PESAN':
                antrian[isbn_dummy].enqueue(nim_dummy)
    print("Inisialisasi 300 event berhasil dimasukkan ke sistem.")

    print('\nSMART LIBRARY MANAGEMENT & RECOMMENDATION SYSTEM')
    print('Ketik BANTUAN untuk melihat opsi perintah CLI')

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
            print('\n=== DAFTAR PERINTAH OPERASI CLI ===')
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
                print('Format salah')
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
                print('Format salah')
                continue
            nim = cmd[1]
            isbn = cmd[2].upper()
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
                print(f'Peminjaman berhasil. Durasi: {durasi_acak} hari.')
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
            nim = cmd[1]
            isbn = cmd[2].upper()
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
            nim = cmd[1]
            isbn = cmd[2].upper()
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
                print('Belum ada rekomendasi')
            else:
                for rec, skor in hasil[:5]:
                    buku = bst.search(rec)
                    if buku:
                        print(rec, '|', buku.judul, '| skor =', skor)
            print('Big-O BFS = O(V+E)')

        elif perintah == 'LAPORAN_BULAN':
            print('\n=== LAPORAN BULANAN ===')
            if len(transaksi) == 0:
                print("Tidak ada transaksi.")
                continue
            shell_data = shell_sort(transaksi.copy())
            merge_data = merge_sort(bst.inorder())
            
            print('\nTop transaksi durasi (Shell Sort):')
            for trx in shell_data[:5]:
                print(f"NIM: {trx.nim} | ISBN: {trx.isbn} | Durasi: {trx.durasi_hari} hari")

            print('\nTop buku populer (Merge Sort):')
            for b in merge_data[:5]:
                print(f"ISBN: {b.isbn} | {b.judul[:20].ljust(20)} | Frekuensi: {b.frek_pinjam}")
            print('\nBig-O Shell Sort = O(n^1.5)')
            print('Big-O Merge Sort = O(n log n)')

        elif perintah == 'BATALKAN_TERAKHIR':
            aksi = stack_undo.pop()
            if aksi is None:
                print('Stack kosong')
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
                print('Undo berhasil:', aksi)
                print('Big-O Stack pop = O(1)')

        elif perintah == 'KELUAR':
            print('Program selesai')
            break
        else:
            print('Perintah tidak dikenal')

if __name__ == '__main__':
    main()
