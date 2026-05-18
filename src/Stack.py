# ============================================
# STACK RIWAYAT TRANSAKSI PERPUSTAKAAN
# ============================================

# --------------------------------------------
# CLASS NODE
# --------------------------------------------
class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


# --------------------------------------------
# CLASS STACK
# --------------------------------------------
class Stack:

    def __init__(self):

        self.top = None


    # PUSH
    def push(self, data):

        node_baru = Node(data)

        node_baru.next = self.top

        self.top = node_baru

        print("Transaksi berhasil ditambahkan")


    # POP / UNDO
    def pop(self):

        if self.top is None:

            print("Stack kosong")
            return None

        data = self.top.data

        self.top = self.top.next

        return data


    # PEEK
    def peek(self):

        if self.top is None:

            return None

        return self.top.data


    # TAMPILKAN STACK
    def tampilkan(self):

        if self.top is None:

            print("Riwayat transaksi kosong")
            return

        sekarang = self.top

        print("\n===== RIWAYAT TRANSAKSI =====")

        while sekarang:

            print("-", sekarang.data)

            sekarang = sekarang.next


# ============================================
# PROGRAM UTAMA
# ============================================

def main():

    riwayat = Stack()

    while True:

        print("\n===== MENU STACK =====")
        print("1. TAMBAH TRANSAKSI")
        print("2. UNDO TRANSAKSI")
        print("3. LIHAT RIWAYAT")
        print("4. TRANSAKSI TERAKHIR")
        print("5. KELUAR")

        pilihan = input("Masukkan pilihan: ")


        # ====================================
        # TAMBAH TRANSAKSI
        # ====================================
        if pilihan == "1":

            transaksi = input("Masukkan transaksi: ")

            riwayat.push(transaksi)


        # ====================================
        # UNDO TRANSAKSI
        # ====================================
        elif pilihan == "2":

            hasil = riwayat.pop()

            if hasil:

                print("Undo transaksi:", hasil)


        # ====================================
        # LIHAT RIWAYAT
        # ====================================
        elif pilihan == "3":

            riwayat.tampilkan()


        # ====================================
        # TRANSAKSI TERAKHIR
        # ====================================
        elif pilihan == "4":

            terakhir = riwayat.peek()

            if terakhir:

                print("Transaksi terakhir:", terakhir)

            else:

                print("Belum ada transaksi")


        # ====================================
        # KELUAR
        # ====================================
        elif pilihan == "5":

            print("Program selesai")
            break


        # ====================================
        # INPUT SALAH
        # ====================================
        else:

            print("Pilihan tidak tersedia")


# ============================================
# MENJALANKAN PROGRAM
# ============================================

if __name__ == "__main__":

    main()