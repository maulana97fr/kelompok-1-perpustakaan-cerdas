import time
import random
import math

# ==============================================================================
# MODUL 1: QUEUE (Antrean Pemesanan Buku - FIFO berbasis Linked List)
# ==============================================================================
class QueueNode:
    def __init__(self, nim):
        self.nim = nim
        self.next = None

class BookingQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, nim):
        new_node = QueueNode(nim)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.head is None:
            return None
        temp = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return temp.nim

    def batal_pesan(self, nim):
        curr = self.head
        prev = None
        while curr is not None:
            if curr.nim == nim:
                if prev is None:
                    self.head = curr.next
                    if self.head is None:
                        self.tail = None
                else:
                    prev.next = curr.next
                    if curr.next is None:
                        self.tail = prev
                return True
            prev = curr
            curr = curr.next
        return False

    def tampilkan(self):
        curr = self.head
        res = []
        while curr is not None:
            res.append(curr.nim)
            curr = curr.next
        return res

    def is_empty(self):
        return self.head is None


# ==============================================================================
# MODUL 2: STACK (Log Global & Fungsi Undo - LIFO berbasis Linked List)
# ==============================================================================
class StackNode:
    def __init__(self, aksi, nim, isbn):
        self.aksi = aksi
        self.nim = nim
        self.isbn = isbn
        self.next = None

class TransactionStack:
    def __init__(self):
        self.top = None

    def push(self, aksi, nim, isbn):
        new_node = StackNode(aksi, nim, isbn)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp


# ==============================================================================
# MODUL 3: BINARY SEARCH TREE (Katalog Buku Berdasarkan Kunci ISBN)
# ==============================================================================
class BSTNode:
    def __init__(self, isbn, judul, kategori):
        self.isbn = isbn
        self.judul = judul
        self.kategori = kategori
        self.status = "TERSEDIA"
        self.peminjam = None
        self.antrean = BookingQueue()
        self.left = None
        self.right = None

class BookCatalog:
    def __init__(self):
        self.root = None

    def insert(self, isbn, judul, kategori):
        self.root = self._insert_recursive(self.root, isbn, judul, kategori)

    def _insert_recursive(self, root, isbn, judul, kategori):
        if root is None:
            return BSTNode(isbn, judul, kategori)
        if isbn < root.isbn:
            root.left = self._insert_recursive(root.left, isbn, judul, kategori)
        elif isbn > root.isbn:
            root.right = self._insert_recursive(root.right, isbn, judul, kategori)
        return root

    def search(self, isbn):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, root, isbn):
        if root is None or root.isbn == isbn:
            return root
        if isbn < root.isbn:
            return self._search_recursive(root.left, isbn)
        return self._search_recursive(root.right, isbn)

    def delete(self, isbn):
        self.root = self._delete_recursive(self.root, isbn)

    def _delete_recursive(self, root, isbn):
        if root is None:
            return root
        if isbn < root.isbn:
            root.left = self._delete_recursive(root.left, isbn)
        elif isbn > root.isbn:
            root.right = self._delete_recursive(root.right, isbn)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.isbn = temp.isbn
            root.judul = temp.judul
            root.kategori = temp.kategori
            root.status = temp.status
            root.peminjam = temp.peminjam
            root.antrean = temp.antrean
            root.right = self._delete_recursive(root.right, temp.isbn)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_all_books(self):
        books = []
        self._inorder_recursive(self.root, books)
        return books

    def _inorder_recursive(self, root, books):
        if root:
            self._inorder_recursive(root.left, books)
            books.append(root)
            self._inorder_recursive(root.right, books)


# ==============================================================================
# MODUL 4: GRAPH & BFS (Sistem Rekomendasi Pintar Ko-Pinjam)
# ==============================================================================
class GraphRekomendasi:
    def __init__(self):
        self.adj_list = {}
        self.weights = {}

    def add_book(self, isbn):
        if isbn not in self.adj_list:
            self.adj_list[isbn] = []

    def add_edge(self, isbn1, isbn2):
        self.add_book(isbn1)
        self.add_book(isbn2)
        
        pair = tuple(sorted([isbn1, isbn2]))
        if isbn2 not in self.adj_list[isbn1]:
            self.adj_list[isbn1].append(isbn2)
        if isbn1 not in self.adj_list[isbn2]:
            self.adj_list[isbn2].append(isbn1)
            
        self.weights[pair] = self.weights.get(pair, 0) + 1

    def bfs_rekomendasi(self, start_isbn, max_hop=2, threshold=1):
        if start_isbn not in self.adj_list:
            return []
        
        visited = {start_isbn}
        queue = [(start_isbn, 0)]
        head = 0
        rekomendasi = []

        while head < len(queue):
            curr_isbn, hop = queue[head]
            head += 1

            if hop >= max_hop:
                continue

            for neighbor in self.adj_list.get(curr_isbn, []):
                if neighbor not in visited:
                    pair = tuple(sorted([curr_isbn, neighbor]))
                    weight = self.weights.get(pair, 0)
                    
                    if weight >= threshold:
                        visited.add(neighbor)
                        queue.append((neighbor, hop + 1))
                        rekomendasi.append((neighbor, weight))
                        
        return rekomendasi


# ==============================================================================
# MODUL 5: ALGORITMA PENGURUTAN (Shell Sort vs Merge Sort untuk Evaluasi)
# ==============================================================================
def shell_sort_durasi(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap][1] < temp[1]:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def merge_sort_populer(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_populer(arr[:mid])
    right = merge_sort_populer(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] >= right[j][1]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res


# ==============================================================================
# MODUL 6: CLI ORCHESTRATOR & FUNGSI UTAMA
# ==============================================================================
def generate_koleksi(catalog, graph):
    kategori_list = ["Teknik", "Sains", "Fiksi", "Sejarah", "Seni"]
    judul_sampel = [
        "Algoritma Vol.1", "Python Cepat", "Jaringan Dasar", "Sains Modern", 
        "Fisika Kuantum", "Kisah Dunia", "Seni Rupa Klasik", "Struktur Data"
    ]
    
    for i in range(1, 81):
        isbn = f"ISBN-{i:04d}"
        judul = f"{random.choice(judul_sampel)} Edisi-{i}"
        kategori = random.choice(kategori_list)
        catalog.insert(isbn, judul, kategori)
        graph.add_book(isbn)

    for _ in range(120):
        id1 = random.randint(1, 80)
        id2 = random.randint(1, 80)
        if id1 != id2:
            graph.add_edge(f"ISBN-{id1:04d}", f"ISBN-{id2:04d}")

def main():
    catalog = BookCatalog()
    tx_stack = TransactionStack()
    graph = GraphRekomendasi()
    
    generate_koleksi(catalog, graph)
    
    print("=" * 60)
    print("        SISTEM PERPUSTAKAAN CERDAS TERINTEGRASI CLI        ")
    print("=" * 60)
    print("Ketik 'BANTUAN' untuk melihat daftar perintah fungsional.\n")

    while True:
        try:
            cmd_input = input(">> ").strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if not cmd_input:
            continue
            
        tokens = cmd_input.split()
        perintah = tokens[0].upper()
        args = tokens[1:]

        if perintah == "KELUAR":
            print("Sesi program dihentikan. Terima kasih!")
            break

        elif perintah == "BANTUAN":
            print("\nDaftar Perintah:")
            print("- KATALOG                       : Menampilkan seluruh koleksi buku")
            print("- CARI_BUKU <isbn>              : Mencari detail informasi buku")
            print("- PINJAM <nim> <isbn>           : Meminjam buku dari perpustakaan")
            print("- KEMBALIKAN <isbn>             : Mengembalikan buku ke rak")
            print("- PESAN <nim> <isbn>            : Booking buku jika sedang dipinjam")
            print("- ANTRIAN <isbn>                : Melihat daftar antrean booking")
            print("- BATALKAN_PESAN <nim> <isbn>   : Keluar dari antrean booking buku")
            print("- REKOMENDASI <isbn>            : Rekomendasi buku terdekat (BFS)")
            print("- LAPORAN_BULAN                 : Cetak statistik & simulasi Big-O")
            print("- BATALKAN_TERAKHIR             : Batalkan aksi transaksi terakhir (Undo)")
            print("- DELETE <isbn>                 : Menghapus buku dari katalog utama")
            print("- KELUAR                        : Keluar dari sistem")

        elif perintah == "KATALOG":
            buku_list = catalog.get_all_books()
            print(f"\n=== KATALOG INVENTARIS BUKU ({len(buku_list)} Judul) ===")
            for b in buku_list:
                print(f"{b.isbn} | {b.judul:<28} | {b.kategori:<8} | {b.status}")
            print(f"-> Analisis Kompleksitas Inorder BST = O(n)")

        elif perintah == "CARI_BUKU":
            if len(args) < 1:
                print("Eror: Gunakan format CARI_BUKU <isbn>")
                continue
            b = catalog.search(args[0])
            if b:
                print(f"\n=== DETAIL DATA BUKU ===")
                print(f"ISBN     : {b.isbn}\nJudul    : {b.judul}\nKategori : {b.kategori}\nStatus   : {b.status}")
                if b.peminjam:
                    print(f"Peminjam : NIM {b.peminjam}")
                print(f"-> Analisis Kompleksitas Search BST = O(log n)")
            else:
                print("Eror: Buku tidak ditemukan di katalog.")

        elif perintah == "PINJAM":
            if len(args) < 2:
                print("Eror: Gunakan format PINJAM <nim> <isbn>")
                continue
            nim, isbn = args[0], args[1]
            b = catalog.search(isbn)
            if b:
                if b.status == "TERSEDIA":
                    b.status = "DIPINJAM"
                    b.peminjam = nim
                    tx_stack.push("PINJAM", nim, isbn)
                    print(f"Sukses! Buku {isbn} berhasil dipinjam oleh NIM {nim}.")
                else:
                    print(f"Gagal: Buku sedang dipinjam NIM {b.peminjam}. Silakan gunakan perintah 'PESAN'.")
            else:
                print("Eror: Buku tidak terdaftar.")

        elif perintah == "KEMBALIKAN":
            if len(args) < 1:
                print("Eror: Gunakan format KEMBALIKAN <isbn>")
                continue
            isbn = args[0]
            b = catalog.search(isbn)
            if b:
                if b.status == "DIPINJAM":
                    nim_lama = b.peminjam
                    tx_stack.push("KEMBALIKAN", nim_lama, isbn)
                    
                    if not b.antrean.is_empty():
                        nim_baru = b.antrean.dequeue()
                        b.peminjam = nim_baru
                        print(f"Sukses! Buku {isbn} dikembalikan. Otomatis dipinjam oleh pengantre pertama: NIM {nim_baru}.")
                    else:
                        b.status = "TERSEDIA"
                        b.peminjam = None
                        print(f"Sukses! Buku {isbn} kini kembali tersedia di rak perpustakaan.")
                else:
                    print("Gagal: Buku sudah berada di rak perpustakaan.")
            else:
                print("Eror: Buku tidak ditemukan.")

        elif perintah == "PESAN":
            if len(args) < 2:
                print("Eror: Gunakan format PESAN <nim> <isbn>")
                continue
            nim, isbn = args[0], args[1]
            b = catalog.search(isbn)
            if b:
                if b.status == "DIPINJAM":
                    b.antrean.enqueue(nim)
                    tx_stack.push("PESAN", nim, isbn)
                    print(f"Sukses! NIM {nim} berhasil masuk antrean booking untuk buku {isbn}.")
                else:
                    print("Gagal: Buku ini tersedia di rak, silakan langsung lakukan transaksi 'PINJAM'.")
            else:
                print("Eror: Buku tidak ditemukan.")

        elif perintah == "ANTRIAN":
            if len(args) < 1:
                print("Eror: Gunakan format ANTRIAN <isbn>")
                continue
            b = catalog.search(args[0])
            if b:
                list_antrean = b.antrean.tampilkan()
                print(f"\n=== DAFTAR ANTREAN BOOKING BUKU {b.isbn} ===")
                if list_antrean:
                    for idx, nim in enumerate(list_antrean, 1):
                        print(f"{idx}. NIM {nim}")
                else:
                    print("(Antrean kosong)")
                print("-> Analisis Kompleksitas Antrean = O(n)")
            else:
                print("Eror: Buku tidak ditemukan.")

        elif perintah == "BATALKAN_PESAN":
            if len(args) < 2:
                print("Eror: Gunakan format BATALKAN_PESAN <nim> <isbn>")
                continue
            nim, isbn = args[0], args[1]
            b = catalog.search(isbn)
            if b and b.antrean.batal_pesan(nim):
                print(f"Sukses! Pembatalan booking untuk NIM {nim} pada buku {isbn} berhasil diproses.")
            else:
                print("Gagal: NIM tidak terdata di dalam antrean buku tersebut.")

        elif perintah == "REKOMENDASI":
            if len(args) < 1:
                print("Eror: Gunakan format REKOMENDASI <isbn>")
                continue
            isbn = args[0]
            print(f"\n=== SISTEM REKOMENDASI PINTAR (BFS Hop <= 2) ===")
            list_rec = graph.bfs_rekomendasi(isbn, max_hop=2, threshold=1)
            if list_rec:
                for idx, (rec_isbn, w) in enumerate(list_rec, 1):
                    b = catalog.search(rec_isbn)
                    judul = b.judul if b else "Judul Tidak Diketahui"
                    print(f"{idx}. {rec_isbn} - {judul} (Skor Frekuensi: {w})")
            else:
                print("Belum ada pola rekomendasi yang cocok untuk buku ini.")
            print("-> Analisis Kompleksitas Graf BFS = O(V + E)")

        elif perintah == "BATALKAN_TERAKHIR":
            last_tx = tx_stack.pop()
            if last_tx:
                b = catalog.search(last_tx.isbn)
                if b:
                    if last_tx.aksi == "PINJAM":
                        b.status = "TERSEDIA"
                        b.peminjam = None
                    elif last_tx.aksi == "KEMBALIKAN":
                        b.status = "DIPINJAM"
                        b.peminjam = last_tx.nim
                    elif last_tx.aksi == "PESAN":
                        b.antrean.batal_pesan(last_tx.nim)
                    print(f"Undo Sukses! Transaksi terakhir ({last_tx.aksi} oleh NIM {last_tx.nim}) telah dibatalkan.")
                else:
                    print("Eror: Dokumen objek transaksi sudah terhapus.")
            else:
                print("Log transaksi kosong. Tidak ada aksi yang bisa dibatalkan.")

        elif perintah == "DELETE":
            if len(args) < 1:
                print("Eror: Gunakan format DELETE <isbn>")
                continue
            isbn = args[0]
            if catalog.search(isbn):
                catalog.delete(isbn)
                print(f"Sukses! Buku dengan kode {isbn} berhasil dihapus dari katalog utama.")
            else:
                print("Gagal: Buku tidak ditemukan.")

        elif perintah == "LAPORAN_BULAN":
            print("\n=== EVALUASI PERFORMA RUNTIME RUNNING SORTING ===")
            for size in [20, 80, 300]:
                test_data1 = [(f"Buku-{j}", random.uniform(0.01, 1.5)) for j in range(size)]
                test_data2 = list(test_data1)
                
                t0 = time.perf_counter()
                shell_sort_durasi(test_data1)
                t_shell = (time.perf_counter() - t0) * 1000
                
                t0 = time.perf_counter()
                merge_sort_populer(test_data2)
                t_merge = (time.perf_counter() - t0) * 1000
                
                print(f"Ukuran Data N = {size:<3} | Shell Sort: {t_shell:.4f} ms | Merge Sort: {t_merge:.4f} ms")
            print("=" * 60)

        else:
            print("Perintah salah! Ketik 'BANTUAN' untuk melihat panduan operasi.")

if __name__ == "__main__":
    main()