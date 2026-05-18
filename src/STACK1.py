# =========================================================
# STACK RIWAYAT TRANSAKSI & UNDO
# Implementasi Linked List
# Big-O:
# push  -> O(1)
# pop   -> O(1)
# =========================================================


# =========================================================
# NODE
# =========================================================
class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


# =========================================================
# STACK
# =========================================================
class Stack:

    def __init__(self):

        self.top = None
        self.size = 0

    # =====================================================
    # PUSH
    # tambah transaksi ke atas stack
    # Big-O: O(1)
    # =====================================================
    def push(self, data):

        node_baru = Node(data)

        node_baru.next = self.top

        self.top = node_baru

        self.size += 1


    # =====================================================
    # POP
    # ambil transaksi paling atas
    # Big-O: O(1)
    # =====================================================
    def pop(self):

        if self.top is None:

            return None

        data = self.top.data

        self.top = self.top.next

        self.size -= 1

        return data


    # =====================================================
    # PEEK
    # melihat data teratas
    # =====================================================
    def peek(self):

        if self.top is None:

            return None

        return self.top.data


    # =====================================================
    # CEK KOSONG
    # =====================================================
    def is_empty(self):

        return self.top is None


# =========================================================
# DATABASE BUKU
# =========================================================
class DatabaseBuku:

    def __init__(self):

        self.buku = {

            "B001": {
                "judul": "Python Dasar",
                "stok": 5,
                "status": "TERSEDIA"
            },

            "B002": {
                "judul": "Struktur Data",
                "stok": 3,
                "status": "TERSEDIA"
            },

            "B003": {
                "judul": "Algoritma",
                "stok": 2,
                "status": "TERSEDIA"
            }
        }


    # =====================================================
    # TAMPILKAN BUKU
    # =====================================================
    def tampilkan_buku(self):

        print("\n===== DAFTAR BUKU =====")

        for kode, data in self.buku.items():

            print(
                f"{kode} | "
                f"{data['judul']} | "
                f"Stok: {data['stok']} | "
                f"Status: {data['status']}"
            )


    # =====================================================
    # PINJAM BUKU
    # =====================================================
    def pinjam_buku(self, kode):

        if kode not in self.buku:

            return False

        if self.buku[kode]["stok"] == 0:

            return False

        self.buku[kode]["stok"] -= 1

        self.buku[kode]["status"] = "DIPINJAM"

        return True


    # =====================================================
    # KEMBALIKAN BUKU
    # =====================================================
    def kembalikan_buku(self, kode):

        if kode not in self.buku:

            return False

        self.buku[kode]["stok"] += 1

        self.buku[kode]["status"] = "TERSEDIA"

        return True


# =========================================================
# SISTEM PERPUSTAKAAN
# =========================================================
class SistemPerpustakaan:

    def __init__(self):

        self.database = DatabaseBuku()

        self.riwayat = Stack()


    # =====================================================
    # PINJAM
    # =====================================================
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


    # =====================================================
    # KEMBALIKAN
    # =====================================================
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


    # =====================================================
    # BATALKAN TRANSAKSI TERAKHIR
    # =====================================================
    def batalkan_terakhir(self):

        transaksi = self.riwayat.pop()

        if transaksi is None:

            print("\nTidak ada transaksi")

            return


        # ================================================
        # JIKA TRANSAKSI PINJAM
        # ================================================
        if transaksi["jenis"] == "PINJAM":

            self.database.kembalikan_buku(
                transaksi["kode"]
            )

            print("\nUNDO BERHASIL")

            print(
                f"Peminjaman buku "
                f"{transaksi['kode']} dibatalkan"
            )


        # ================================================
        # JIKA TRANSAKSI KEMBALI
        # ================================================
        elif transaksi["jenis"] == "KEMBALI":

            self.database.pinjam_buku(
                transaksi["kode"]
            )

            print("\nUNDO BERHASIL")

            print(
                f"Pengembalian buku "
                f"{transaksi['kode']} dibatalkan"
            )


    # =====================================================
    # LIHAT RIWAYAT
    # =====================================================
    def lihat_riwayat(self):

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


# =========================================================
# MENU
# =========================================================
def main():

    sistem = SistemPerpustakaan()

    while True:

        print("\n==============================")
        print(" SISTEM PERPUSTAKAAN DIGITAL ")
        print("==============================")

        print("1. Lihat Buku")
        print("2. Pinjam Buku")
        print("3. Kembalikan Buku")
        print("4. BATALKAN_TERAKHIR")
        print("5. Lihat Riwayat")
        print("0. Keluar")

        pilihan = input("\nMasukkan pilihan: ")


        # =================================================
        # LIHAT BUKU
        # =================================================
        if pilihan == "1":

            sistem.database.tampilkan_buku()


        # =================================================
        # PINJAM
        # =================================================
        elif pilihan == "2":

            kode = input("Kode Buku : ").upper()

            nama = input("Nama      : ")

            sistem.pinjam(kode, nama)


        # =================================================
        # KEMBALIKAN
        # =================================================
        elif pilihan == "3":

            kode = input("Kode Buku : ").upper()

            nama = input("Nama      : ")

            sistem.kembalikan(kode, nama)


        # =================================================
        # UNDO
        # =================================================
        elif pilihan == "4":

            sistem.batalkan_terakhir()


        # =================================================
        # RIWAYAT
        # =================================================
        elif pilihan == "5":

            sistem.lihat_riwayat()


        # =================================================
        # KELUAR
        # =================================================
        elif pilihan == "0":

            print("\nProgram selesai")

            break


        else:

            print("\nPilihan tidak tersedia")


# =========================================================
# MENJALANKAN PROGRAM
# =========================================================
if __name__ == "__main__":

    main()