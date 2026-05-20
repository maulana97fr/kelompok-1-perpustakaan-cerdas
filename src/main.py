# src/main.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from src.modules.modul3_bst import BSTKatalog

# Aturan data sesuai panduan (Seed 13)
random.seed(13)
KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']

class Buku:
    def __init__(self, isbn, judul, pengarang, kategori, status=0):
        self.isbn = isbn          # Kunci/Key Pengurutan BST
        self.judul = judul
        self.pengarang = pengarang
        self.kategori = kategori
        self.status = status      # 0=TERSEDIA, 1=DIPINJAM, 2=DIPESAN

def generate_koleksi(n=80):
    """Fungsi otomatis dari dosen untuk membuat 80 buku acak"""
    kata = ['Algoritma', 'Jaringan', 'Python', 'Data', 'Digital',
            'Sistem', 'Kontrol', 'Sinyal', 'Elektronika', 'Fisika']
    return [Buku(f'ISBN-{i:04d}', f'{random.choice(kata)} Vol.{i}',
                 f'Penulis-{random.randint(1,20)}', random.choice(KATEGORI))
            for i in range(1, n+1)]

def main():
    bst = BSTKatalog()
    
    # Otomatis memasukkan 80 data buku awal ke dalam BST
    for buku in generate_koleksi(80):
        bst.insert(buku)

    print("====================================================")
    print("  SMART LIBRARY SYSTEM - MODUL KATALOG (BST) ACTIVE ")
    print("====================================================")
    print("Ketik 'BANTUAN' untuk melihat daftar perintah.")

    while True:
        perintah = input("\nPerpustakaan> ").strip().split()
        if not perintah:
            continue
        
        cmd = perintah[0].upper()

        if cmd == "BANTUAN":
            print("\nDaftar Perintah Katalog (BST):")
            print("  KATALOG           : Menampilkan semua buku urut ISBN (In-order)")
            print("  CARI <isbn>       : Mencari info buku berdasarkan ISBN")
            print("  STATUS <isbn> <0/1/2> : Mengubah status buku (0:Tersedia, 1:Pinjam, 2:Pesan)")
            print("  KELUAR            : Menutup aplikasi")

        elif cmd == "KATALOG":
            print("\n==========================================================")
            print("         DAFTAR KATALOG BUKU (IN-ORDER TRAVERSAL BST)     ")
            print("==========================================================")
            semua_buku = bst.inorder()
            for bku in semua_buku:
                status_str = "TERSEDIA" if bku.status == 0 else ("DIPINJAM" if bku.status == 1 else "DIPESAN")
                print(f"[{bku.isbn}] {bku.judul} | Penulis: {bku.pengarang} | Status: {status_str}")
            print(f"Total: {len(semua_buku)} Buku berhasil diurutkan.")

        elif cmd == "CARI":
            if len(perintah) < 2:
                print("[!] Gunakan format: CARI <isbn> (Contoh: CARI ISBN-0005)")
                continue
            isbn_cari = perintah[1]
            buku_ketemu = bst.search(isbn_cari)
            if buku_ketemu:
                status_str = "TERSEDIA" if buku_ketemu.status == 0 else ("DIPINJAM" if buku_ketemu.status == 1 else "DIPESAN")
                print(f"\n[✔] Buku Ditemukan (Kompleksitas: O(log n))")
                print(f"  -> Judul    : {buku_ketemu.judul}")
                print(f"  -> Pengarang: {buku_ketemu.pengarang}")
                print(f"  -> Kategori : {buku_ketemu.kategori}")
                print(f"  -> Status   : {status_str}")
            else:
                print(f"[X] Buku dengan {isbn_cari} tidak ditemukan di katalog.")

        elif cmd == "STATUS":
            if len(perintah) < 3:
                print("[!] Gunakan format: STATUS <isbn> <0/1/2>")
                continue
            isbn_update = perintah[1]
            try:
                status_baru = int(perintah[2])
                if bst.update_status(isbn_update, status_baru):
                    print(f"[✔] Status {isbn_update} berhasil diperbarui!")
                else:
                    print("[X] Gagal update. ISBN tidak ditemukan atau kode status salah.")
            except ValueError:
                print("[!] Kode status harus berupa angka (0, 1, atau 2).")

        elif cmd == "KELUAR":
            print("\nSistem ditutup. Kerja bagus hari ini, Maul!")
            break
        else:
            print("[!] Perintah tidak dikenal. Ketik 'BANTUAN' untuk melihat daftar perintah.")

if __name__ == "__main__":
    main()