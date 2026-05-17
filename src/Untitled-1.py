import numpy as np
import time
import random

from dataclasses import dataclass
from typing import Optional

np.random.seed (13)
random.seed(13)

KATEGORI = [
    'Fiksi',
    'Sains',
    'Teknik',
    'Sejarah',
    'Seni'
]

STATUS = {
    'TERSEDIA' : 0,
    'DIPINJAM' : 1,
    'DIPESAN' : 2
}

# DATA CLASS BUKU

@dataclass
class Buku:

    isbn: str
    judul: str
    pengarang: str
    kategori: str

    status: int = STATUS['TERSEDIA']

    stok: int = 1


# DATA CLASS PEMINJAMAN

@dataclass
class Peminjaman: 

    transaksi_id: int

    anggota_id: str

    isbn: str

    tgl_pinjam: float

    durasi_hari: int = 14


# NODE LINKED LIST

class Node:

    def __init__(self, data):

        self.data = data

        self.next = None


# STACK
# UNTUK UNDO TRANSAKSI
# PUSH / POP = O(1)

class Stack: 

    def __init__(self):

        self.top = None

        self.size = 0


    # PUSH

    def push(self, data):

        node_baru = Node(data)

        node_baru.next = self.top

        self.top = node_baru

        self.size += 1


    # POP

    def pop(self):

        if self.top is None :

            return None
        
        data = self.top.data
        
        self.top = self.top.next
        
        self.size -= 1

        return data
    

    # PEEK
    
    def peek(self):

        if self.top is None:

            return None
        
        return self.top.data
    
    def is_empty(self):

        return self.top is None
    

# QUEUE
# UNTUK ANTRIAN PEMESANAN
# ENQUEUE / DEQUEUE = O(1)
    
class Queue:

    def __init__(self):

        self.front = None

        self.rear = None

        self.size = 0


    # ENQUEUE

    def enqueue(self, data):

        node_baru = Node(data)

        if self.rear is None:

            self.front = node_baru

            self.rear = node_baru

        else:

            self.rear.next = node_baru

            self.rear = node_baru

        self.size += 1

    # DEQUEUE

    def dequeue (self):

        if self.front is None:

            return None
        
        data = self.front.data

        self.front = self.front.next

        if self.front is None:

            self.rear = None

        self.size -= 1

        return data
    
    def is_empty(self):

        return self.front is None
    
# DATABASE BUKU

class DatabaseBuku:

    def __init__(self):

        self.buku = {}

        self.generate_koleksi()


    # GENERATE 80 KOLEKSI BUKU

    def generate_koleksi(self):

        kata = [

            'Algoritma',
            'jaringan',
            'Python',
            'Data',
            'Digital',
            'Sistem',
            'Kontrol',
            'Sinyal',
            'Elektronika',
            'Fisika'
        ]

        for i in range(1, 81):

            isbn = f'ISBN-{i:04d}'
            
            buku = Buku (

                isbn = isbn,

                judul = f'{random.choice(kata)} vol.{i}',

                pengarang = f'Penulis-{random.randint(1,20)}',

                kategori = random.choice(KATEGORI),

                stok = random.randint(1,5)
            )

            self.buku[isbn] = buku

    # TAMPILKAN BUKU

    def tampilkan_buku(self):

        print("\n==== DAFTAR BUKU ====")

        for isbn, buku in self.buku.items():

            print(

              f"{isbn} | "  

              f"{buku.judul} | "

              f"{buku.kategori} | "

              f"Stok: {buku.stok}"
            )

    #PINJAM BUKU

    def pinjam_buku(self, isbn):

        if isbn not in self.buku:

            return False
        
        buku = self.buku[isbn]

        if buku.stok == 0:

            return False
        
        buku.stok -= 1

        buku.status = STATUS['DIPINJAM']

        return True
    

    # KEMBALIKAN BUKU

    def kembalikan_buku(self, isbn):
        if isbn not in self.buku:

            return False
        
        buku = self.buku[isbn]

        buku.stok += 1

        buku.status = STATUS['TERSEDIA']

        return True

# SISTEM PERPUSTAKAAN

class SistemPerpustakaan:

    def __init__(self):

        self.database = DatabaseBuku()

        self.riwayat = Stack()

        self.antrian = {}

        self.transaksi_id = 1

        # QUEUE UNTUK SETIAP BUKU
        for isbn in self.database.buku:

            self.antrian[isbn] = Queue()


    # PINJAM
    def pinjam(self, nim, isbn):

        berhasil = self.database.pinjam_buku(isbn)

        if berhasil:

            transaksi = {

                "jenis": "PINJAM",

                "nim": nim,

                "isbn": isbn
            }

            self.riwayat.push(transaksi)

            print("\nPeminjaman berhasil")

        else:

            print("\nBuku sedang habis")

            jawab = input("Masuk antrian? (y/n): ")

            if jawab.lower() == "y":

                self.antrian[isbn].enqueue(nim)

                print("Berhasil masuk antrian")


    # KEMBALIKAN
    def kembalikan(self, nim, isbn):

        berhasil = self.database.kembalikan_buku(isbn)

        if berhasil:

            transaksi = {

                "jenis": "KEMBALI",

                "nim": nim,

                "isbn": isbn
            }

            self.riwayat.push(transaksi)

            print("\nPengembalian berhasil")

            # CEK ANTRIAN
            if not self.antrian[isbn].is_empty():

                berikutnya = self.antrian[isbn].dequeue()

                print(
                    f"{berikutnya} mendapat giliran meminjam {isbn}"
                )

        else:

            print("\nPengembalian gagal")


    # UNDO
    def batalkan_terakhir(self):

        transaksi = self.riwayat.pop()

        if transaksi is None:

            print("\nTidak ada transaksi")

            return

        if transaksi["jenis"] == "PINJAM":

            self.database.kembalikan_buku(
                transaksi["isbn"]
            )

            print("\nUNDO peminjaman berhasil")

        elif transaksi["jenis"] == "KEMBALI":

            self.database.pinjam_buku(
                transaksi["isbn"]
            )

            print("\nUNDO pengembalian berhasil")


    # RIWAYAT
    def lihat_riwayat(self):

        if self.riwayat.is_empty():

            print("\nRiwayat kosong")

            return

        print("\n==== RIWAYAT TRANSAKSI ====")

        bantu = self.riwayat.top

        while bantu:

            data = bantu.data

            print(

                f"{data['jenis']} | "

                f"{data['nim']} | "

                f"{data['isbn']}"
            )

            bantu = bantu.next


# MAIN PROGRAM

def main():

    sistem = SistemPerpustakaan()

    while True:

        print("\n===================================")
        print(" SMART LIBRARY MANAGEMENT SYSTEM ")
        print("===================================")

        print("1. Lihat Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. BATALKAN_TERAKHIR")
        print("5. Lihat Riwayat")
        print("0. Keluar")

        pilihan = input("\nMasukkan pilihan: ")

        # LIHAT BUKU 

        if pilihan == "1":
            sistem.database.tampilkan_buku()


        # PINJAM 

        elif pilihan == "2":

            nim = input("NIM  : ")

            isbn = input("ISBN  : ").upper()

            sistem.pinjam(nim, isbn)


        # KEMBALIKAN 

        elif pilihan == "3":

            nim = input("NIM  : ")

            isbn = input("ISBN  : ").upper()

            sistem.kembalikan(nim, isbn)

        # UNDO

        elif pilihan == "4":

            sistem.batalkan_terakhir()


        # RIWAYAT

        elif pilihan == "5":

            sistem.lihat_riwayat()


        # KELUAR

        elif pilihan == "0":

            print("\nProgram selesai")

            break


        else:

            print("\nPilihan tidak tersedia")


# RUN PROGRAM

if __name__== "__main__":

    main()








