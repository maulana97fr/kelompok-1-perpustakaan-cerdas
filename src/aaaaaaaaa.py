# ============================================================
#   STACK RIWAYAT TRANSAKSI & UNDO
#   Implementasi berbasis Linked List
#   Big-O: push O(1), pop O(1)
# ============================================================


# ── 1. NODE
class Node:
    def __init__(self, transaksi):
        self.transaksi = transaksi
        self.next      = None


# ── 2. STACK berbasis Linked List
class StackTransaksi:
    def __init__(self):
        self.top   = None
        self._size = 0

    def push(self, transaksi: dict):        # O(1)
        node      = Node(transaksi)
        node.next = self.top
        self.top  = node
        self._size += 1

    def pop(self):                          # O(1)
        if self.is_empty():
            return None
        data     = self.top.transaksi
        self.top = self.top.next
        self._size -= 1
        return data

    def peek(self):                         # O(1)
        if self.is_empty():
            return None
        return self.top.transaksi

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size


# ── 3. DATABASE BUKU
class DatabaseBuku:
    def __init__(self):
        self.buku = {
            "B001": {"judul": "Python Dasar",             "stok": 5, "status": "tersedia"},
            "B002": {"judul": "Struktur Data",             "stok": 3, "status": "tersedia"},
            "B003": {"judul": "Algoritma & Pemrograman",   "stok": 2, "status": "tersedia"},
        }

    def tampilkan(self):
        garis = "-" * 55
        print("\n" + garis)
        print(f"  {'ID':<6} {'Judul':<30} {'Stok':<6} {'Status'}")
        print(garis)
        for id_b, info in self.buku.items():
            print(f"  {id_b:<6} {info['judul']:<30} {info['stok']:<6} {info['status']}")
        print(garis)

    def pinjam(self, id_buku):
        if id_buku not in self.buku:
            return False, "Buku tidak ditemukan"
        b = self.buku[id_buku]
        if b["stok"] == 0:
            return False, "Stok habis"
        b["stok"] -= 1
        if b["stok"] == 0:
            b["status"] = "habis"
        return True, "OK"

    def kembalikan(self, id_buku):
        if id_buku not in self.buku:
            return False, "Buku tidak ditemukan"
        b = self.buku[id_buku]
        b["stok"]  += 1
        b["status"] = "tersedia"
        return True, "OK"

    def get_judul(self, id_buku):
        return self.buku.get(id_buku, {}).get("judul", "?")


# ── 4. SISTEM PERPUSTAKAAN
class SistemPerpustakaan:
    def __init__(self):
        self.db_buku    = DatabaseBuku()
        self.stack_log  = StackTransaksi()
        self.id_counter = 1

    def _buat_id(self):
        tid = f"TRX{self.id_counter:04d}"
        self.id_counter += 1
        return tid

    def pinjam_buku(self, id_buku, nama_peminjam):
        ok, pesan = self.db_buku.pinjam(id_buku)
        if not ok:
            print(f"  [GAGAL] {pesan}")
            return
        transaksi = {
            "id"      : self._buat_id(),
            "tipe"    : "PINJAM",
            "id_buku" : id_buku,
            "judul"   : self.db_buku.get_judul(id_buku),
            "peminjam": nama_peminjam,
        }
        self.stack_log.push(transaksi)
        print(f"  [OK] {transaksi['id']} — {nama_peminjam} meminjam '{transaksi['judul']}'")

    def kembalikan_buku(self, id_buku, nama_peminjam):
        ok, pesan = self.db_buku.kembalikan(id_buku)
        if not ok:
            print(f"  [GAGAL] {pesan}")
            return
        transaksi = {
            "id"      : self._buat_id(),
            "tipe"    : "KEMBALI",
            "id_buku" : id_buku,
            "judul"   : self.db_buku.get_judul(id_buku),
            "peminjam": nama_peminjam,
        }
        self.stack_log.push(transaksi)
        print(f"  [OK] {transaksi['id']} — {nama_peminjam} mengembalikan '{transaksi['judul']}'")

    def batalkan_terakhir(self):
        if self.stack_log.is_empty():
            print("  [INFO] Tidak ada transaksi yang bisa dibatalkan.")
            return
        trx = self.stack_log.pop()
        print(f"\n  Membatalkan {trx['id']} ({trx['tipe']}) — '{trx['judul']}' oleh {trx['peminjam']}")
        if trx["tipe"] == "PINJAM":
            self.db_buku.kembalikan(trx["id_buku"])
            print(f"  Stok '{trx['judul']}' dikembalikan (+1).")
        elif trx["tipe"] == "KEMBALI":
            self.db_buku.pinjam(trx["id_buku"])
            print(f"  Stok '{trx['judul']}' dikurangi (-1).")
        print(f"  [OK] Transaksi {trx['id']} berhasil dibatalkan.\n")

    def lihat_riwayat(self):
        if self.stack_log.is_empty():
            print("  Belum ada riwayat transaksi.")
            return
        garis = "-" * 50
        print("\n" + garis)
        print("  RIWAYAT TRANSAKSI (terbaru di atas)")
        print(garis)
        node = self.stack_log.top
        urut = 1
        while node:
            t = node.transaksi
            print(f"  {urut}. [{t['tipe']:<7}] {t['id']} | {t['judul'][:25]:<25} | {t['peminjam']}")
            node = node.next
            urut += 1
        print(garis)
        print(f"  Total: {self.stack_log.size()} transaksi\n")

    def lihat_teratas(self):
        trx = self.stack_log.peek()
        if trx is None:
            print("  Stack kosong.")
        else:
            print(f"  Teratas → {trx['id']} | {trx['tipe']} | '{trx['judul']}' | {trx['peminjam']}")


# ── 5. MENU UTAMA
def menu():
    sistem = SistemPerpustakaan()
    while True:
        print("\n" + "=" * 50)
        print("   SISTEM PERPUSTAKAAN — STACK TRANSAKSI")
        print("=" * 50)
        print("  1. Pinjam Buku")
        print("  2. Kembalikan Buku")
        print("  3. BATALKAN TRANSAKSI TERAKHIR (Undo)")
        print("  4. Lihat Riwayat Transaksi")
        print("  5. Lihat Transaksi Teratas (Peek)")
        print("  6. Lihat Daftar Buku & Stok")
        print("  0. Keluar")
        print("-" * 50)

        pilihan = input("  Pilih menu: ").strip()

        if pilihan == "1":
            sistem.db_buku.tampilkan()
            id_b = input("  ID Buku      : ").strip().upper()
            nama = input("  Nama Peminjam: ").strip()
            sistem.pinjam_buku(id_b, nama)
        elif pilihan == "2":
            id_b = input("  ID Buku      : ").strip().upper()
            nama = input("  Nama Peminjam: ").strip()
            sistem.kembalikan_buku(id_b, nama)
        elif pilihan == "3":
            sistem.batalkan_terakhir()
        elif pilihan == "4":
            sistem.lihat_riwayat()
        elif pilihan == "5":
            sistem.lihat_teratas()
        elif pilihan == "6":
            sistem.db_buku.tampilkan()
        elif pilihan == "0":
            print("\n  Sampai jumpa!\n")
            break
        else:
            print("  Pilihan tidak valid.")


if __name__ == "__main__":
    menu()