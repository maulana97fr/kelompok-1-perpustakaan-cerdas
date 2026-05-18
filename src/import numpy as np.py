import numpy as np
import random

# =====================================================
# SMART LIBRARY MANAGEMENT SYSTEM
# =====================================================

# AGAR RANDOM SELALU SAMA
np.random.seed(13)
random.seed(13)

# =====================================================
# DATA SISTEM
# =====================================================

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']

STATUS_TERSEDIA = 0
STATUS_DIPINJAM = 1

# =====================================================
# CLASS BUKU
# =====================================================

class Buku:

    def __init__(self, isbn, judul, kategori):

        self.isbn = isbn
        self.judul = judul
        self.kategori = kategori
        self.status = STATUS_TERSEDIA


# =====================================================
# NODE LINKED LIST
# =====================================================

class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


# =====================================================
# QUEUE LINKED LIST
# =====================================================

class Queue:

    def __init__(self):

        self.head = None
        self.tail = None

    # enqueue O(1)
    def enqueue(self, data):

        new_node = Node(data)

        if self.tail is None:

            self.head = new_node
            self.tail = new_node

        else:

            self.tail.next = new_node
            self.tail = new_node

    # dequeue O(1)
    def dequeue(self):

        if self.head is None:
            return None

        data = self.head.data

        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return data

    def is_empty(self):

        return self.head is None

    def tampilkan(self):

        current = self.head

        if current is None:

            print("Antrian kosong")
            return

        while current:

            print("-", current.data)

            current = current.next


# =====================================================
# GENERATE DATA BUKU
# =====================================================

def generate_buku():

    kata = [
        'Algoritma',
        'Jaringan',
        'Python',
        'Data',
        'Digital',
        'Sistem',
        'Kontrol',
        'Sinyal',
        'Elektronika',
        'Fisika'
    ]

    koleksi = []

    for i in range(1, 81):

        isbn = f"ISBN-{i:04d}"

        judul = f"{random.choice(kata)} Vol.{i}"

        kategori = random.choice(KATEGORI)

        buku = Buku(isbn, judul, kategori)

        koleksi.append(buku)

    return koleksi


# =====================================================
# MAIN PROGRAM
# =====================================================

def main():

    # Generate 80 buku
    koleksi = generate_buku()

    # Queue untuk setiap ISBN
    antrian = {}

    for buku in koleksi:

        antrian[buku.isbn] = Queue()

    # =================================================
    # HEADER
    # =================================================

    print("========================================")
    print(" SMART LIBRARY MANAGEMENT SYSTEM ")
    print("========================================")

    # =================================================
    # LOOP PROGRAM
    # =================================================

    while True:

        print("\n===== MENU =====")
        print("1. KATALOG")
        print("2. PINJAM")
        print("3. PESAN")
        print("4. KEMBALIKAN")
        print("5. ANTRIAN_BUKU")
        print("6. KELUAR")

        pilihan = input("Masukkan pilihan: ")

        # =================================================
        # KATALOG
        # =================================================

        if pilihan == "1":

            print("\n===== DAFTAR BUKU =====")

            for buku in koleksi:

                if buku.status == STATUS_TERSEDIA:
                    status = "TERSEDIA"
                else:
                    status = "DIPINJAM"

                print(
                    buku.isbn,
                    "|",
                    buku.judul,
                    "|",
                    buku.kategori,
                    "|",
                    status
                )

        # =================================================
        # PINJAM
        # =================================================

        elif pilihan == "2":

            isbn = input("Masukkan ISBN: ")
            nim = input("Masukkan NIM: ")

            ditemukan = False

            for buku in koleksi:

                if buku.isbn == isbn:

                    ditemukan = True

                    if buku.status == STATUS_TERSEDIA:

                        buku.status = STATUS_DIPINJAM

                        print(
                            f"Buku {isbn} berhasil dipinjam oleh {nim}"
                        )

                    else:

                        print(
                            "Buku sedang dipinjam."
                        )

                        print(
                            "Gunakan menu PESAN."
                        )

                    break

            if not ditemukan:

                print("ISBN tidak ditemukan")

        # =================================================
        # PESAN
        # =================================================

        elif pilihan == "3":

            isbn = input("Masukkan ISBN: ")
            nim = input("Masukkan NIM: ")

            if isbn in antrian:

                antrian[isbn].enqueue(nim)

                print(
                    f"{nim} masuk antrian buku {isbn}"
                )

            else:

                print("ISBN tidak ditemukan")

        # =================================================
        # KEMBALIKAN
        # =================================================

        elif pilihan == "4":

            isbn = input("Masukkan ISBN: ")

            ditemukan = False

            for buku in koleksi:

                if buku.isbn == isbn:

                    ditemukan = True

                    buku.status = STATUS_TERSEDIA

                    print("Buku berhasil dikembalikan")

                    # PRIORITAS ANTRIAN
                    if not antrian[isbn].is_empty():

                        next_user = antrian[isbn].dequeue()

                        buku.status = STATUS_DIPINJAM

                        print(
                            f"Buku otomatis dipinjam oleh {next_user}"
                        )

                    break

            if not ditemukan:

                print("ISBN tidak ditemukan")

        # =================================================
        # LIHAT ANTRIAN
        # =================================================

        elif pilihan == "5":

            isbn = input("Masukkan ISBN: ")

            if isbn in antrian:

                print(f"\nAntrian Buku {isbn}")

                antrian[isbn].tampilkan()

            else:

                print("ISBN tidak ditemukan")

        # =================================================
        # KELUAR
        # =================================================

        elif pilihan == "6":

            print("Program selesai")
            break

        # =================================================
        # INPUT SALAH
        # =================================================

        else:

            print("Pilihan tidak tersedia")


# =====================================================
# JALANKAN PROGRAM
# =====================================================

if __name__ == "__main__":

    main()