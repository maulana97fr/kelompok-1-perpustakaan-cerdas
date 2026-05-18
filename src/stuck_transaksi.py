# ============================================================
# SISTEM PERPUSTAKAAN
# STACK RIWAYAT TRANSAKSI & UNDO
# ============================================================

# =========================
# NODE
# =========================
class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


# =========================
# STACK LINKED LIST
# =========================
class Stack:

    def __init__(self):

        self.top = None
        self.size = 0

    # tambah data ke stack
    def push(self, data):

        node_baru = Node(data)

        node_baru.next = self.top

        self.top = node_baru

        self.size += 1

    # ambil data teratas
    def pop(self):

        if self.top is None:

            return None

        data = self.top.data

        self.top = self.top.next

        self.size -= 1

        return data

    # melihat data teratas
    def peek(self):

        if self.top is None:

            return None

        return self.top.data

    # cek stack kosong
    def is_empty(self):

        return self.top is None


# =========================
# DATABASE BUKU
# =========================
class DatabaseBuku:

    def __init__(self):

        self.buku = {

            "B001": {
                "judul": "Python Dasar",
                "stok": 5
            },

            "B002": {
                "judul": "Struktur Data",
                "stok": 3
            },

            "B003": {
                "judul": "Algoritma Pemrograman",
                "stok": 2
            }
        }

    # tampilkan buku
    def tampilkan_buku(self):

        print("\n===== DAFTAR BUKU =====")

        for kode, data in self.buku.items():

            print(
                f"{kode} | {data['judul']} | Stok: {data['stok']}"
            )

    # pinjam buku
    def pinjam_buku(self, kode):

        if kode not in self.buku:

            return False

        if self.buku[kode]["stok"] == 0:

            return False

        self.buku[kode]["stok"] -= 1

        return True

    # kembalikan buku
    def kembalikan_buku(self, kode):

        if kode not in self.buku:

            return False

        self.buku[kode]["stok"] += 1

        return True


# =========================
# SISTEM PERPUSTAKAAN
# =========================
class SistemPerpustakaan:

    def __init__(self):

        self.database = DatabaseBuku()

        self.riwayat = Stack()

    # =====================
    # PINJAM BUKU
    # =====================
    def pinjam(self, kode, nama):

        berhasil = self.database.pinjam_buku(kode)

        if berhasil:

            transaksi = {

                "jenis": "PINJAM",
                "kode": kode,
                "nama": nama
            }

            self.riwayat.push(transaksi)

            print(
                f"\nBuku {kode} berhasil dipinjam oleh {nama}"
            )

        else:

            print("\nPeminjaman gagal")

    # =====================
    # KEMBALIKAN BUKU
    # =====================
    def kembalikan(self, kode, nama):

        berhasil = self.database.kembalikan_buku(kode)

        if berhasil:

            transaksi = {

                "jenis": "KEMBALI",
                "kode": kode,
                "nama": nama
            }

            self.riwayat.push(transaksi)

            print(
                f"\nBuku {kode} berhasil dikembalikan"
            )

        else:

            print("\nPengembalian gagal")

    # =====================
    # UNDO TRANSAKSI
    # =====================
    def batalkan_terakhir(self):

        transaksi = self.riwayat.pop()

        if transaksi is None:

            print("\nTidak ada transaksi")

            return

        # jika transaksi pinjam
        if transaksi["jenis"] == "PINJAM":

            self.database.kembalikan_buku(
                transaksi["kode"]
            )

            print(
                f"\nUndo berhasil"
            )

            print(
                f"Peminjaman buku {transaksi['kode']} dibatalkan"
            )

        # jika transaksi kembali
        elif transaksi["jenis"] == "KEMBALI":

            self.database.pinjam_buku(
                transaksi["kode"]
            )

            print(
                f"\nUndo berhasil"
            )

            print(
                f"Pengembalian buku {transaksi['kode']} dibatalkan"
            )

    # =====================
    # TAMPILKAN RIWAYAT
    # =====================
    def tampilkan_riwayat(self):

        if self.riwayat.is_empty():

            print("\nRiwayat kosong")

            return

        print("\n===== RIWAYAT TRANSAKSI =====")

        bantu = self.riwayat.top

        while bantu:

            data = bantu.data

            print(
                f"{data['jenis']} | "
                f"{data['kode']} | "
                f"{data['nama']}"
            )

            bantu = bantu.next


# =========================
# MENU PROGRAM
# =========================
def main():

    sistem = SistemPerpustakaan()

    while True:

        print("\n==============================")
        print(" SISTEM PERPUSTAKAAN DIGITAL ")
        print("==============================")

        print("1. Lihat Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. Undo Transaksi")
        print("5. Lihat Riwayat")
        print("0. Keluar")

        pilihan = input("\nMasukkan pilihan: ")

        # =====================
        # LIHAT BUKU
        # =====================
        if pilihan == "1":

            sistem.database.tampilkan_buku()

        # =====================
        # PINJAM
        # =====================
        elif pilihan == "2":

            kode = input("Kode Buku : ").upper()

            nama = input("Nama      : ")

            sistem.pinjam(kode, nama)

        # =====================
        # KEMBALIKAN
        # =====================
        elif pilihan == "3":

            kode = input("Kode Buku : ").upper()

            nama = input("Nama      : ")

            sistem.kembalikan(kode, nama)

        # =====================
        # UNDO
        # =====================
        elif pilihan == "4":

            sistem.batalkan_terakhir()

        # =====================
        # RIWAYAT
        # =====================
        elif pilihan == "5":

            sistem.tampilkan_riwayat()

        # =====================
        # KELUAR
        # =====================
        elif pilihan == "0":

            print("\nProgram selesai")

            break

        else:

            print("\nPilihan tidak tersedia")


# =========================
# MENJALANKAN PROGRAM
# =========================
if __name__ == "__main__":

    main()