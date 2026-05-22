import time
import random

# =========================================================
# 1. SHELL SORT (Kategori: In-place Comparison Sort)
# Kompleksitas Waktu: Worst-case O(n log^2 n) atau O(n^2) tergantung gap
# =========================================================
def shell_sort(arr):
    """
    Mengurutkan list array berupa tuple/objek (buku, frekuensi) secara descending
    menggunakan metode interval gap (Knuth atau Shell sequence).
    """
    n = len(arr)
    gap = n // 2

    # Lakukan loop selama interval gap lebih besar dari 0
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            # Bandingkan nilai frekuensi peminjaman (indeks [1] atau properti frek_pinjam)
            # Jika menggunakan objek Buku, ganti temp[1] menjadi temp.frek_pinjam
            while j >= gap and (arr[j - gap].frek_pinjam if hasattr(arr[j - gap], 'frek_pinjam') else arr[j - gap][1]) < (temp.frek_pinjam if hasattr(temp, 'frek_pinjam') else temp[1]):
                arr[j] = arr[j - gap]
                j -= gap
                
            arr[j] = temp
        gap //= 2


# =========================================================
# 2. MERGE SORT (Kategori: Divide and Conquer)
# Kompleksitas Waktu: Worst-case O(n log n)
# =========================================================
def merge_sort(arr):
    """
    Mengurutkan list secara rekursif dengan membagi array menjadi dua sub-array
    hingga berukuran 1, kemudian menggabungkannya kembali secara terurut (descending).
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Rekursif membelah bagian kiri dan kanan
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Proses Merge (Penggabungan) kedua sub-array secara descending
        while i < len(left_half) and j < len(right_half):
            # Ambil nilai pembanding frekuensi
            val_left = left_half[i].frek_pinjam if hasattr(left_half[i], 'frek_pinjam') else left_half[i][1]
            val_right = right_half[j].frek_pinjam if hasattr(right_half[j], 'frek_pinjam') else right_half[j][1]

            if val_left >= val_right:  # >= untuk descending
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Salin sisa elemen dari left_half jika ada
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Salin sisa elemen dari right_half jika ada
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


# =========================================================
# 3. EVALUATOR RUNTIME (LAPORAN_BULAN)
# Membandingkan kecepatan asimtotik aslinya di terminal
# =========================================================
def bandingkan_runtime_spesifikasi(transaksi, bst_katalog):
    """
    Mengumpulkan data frekuensi dari seluruh buku yang ada di katalog BST,
    lakukan pengujian duplikat list untuk mengukur perbandingan running time 
    dalam milidetik (ms) untuk ukuran N = 20, 80, dan 300 sesuai spesifikasi tugas.
    """
    print("\n=== EVALUASI PERFORMA RUNTIME RUNNING SORTING ===")
    
    # Ambil seluruh buku dari BST (menggunakan inorder traversal)
    semua_buku = bst_katalog.inorder() if hasattr(bst_katalog, 'inorder') else []
    
    # Kasus simulasi perbandingan performa untuk N berbeda
    for size in [20, 80, 300]:
        # Jika buku di sistem kurang dari target size, kita generate sampel acak tiruan
        if len(semua_buku) < size:
            class DummyBuku:
                def __init__(self, f): self.frek_pinjam = f
            test_data_1 = [DummyBuku(random.randint(0, 100)) for _ in range(size)]
        else:
            test_data_1 = list(semua_buku[:size])
            
        test_data_2 = list(test_data_1)

        # 1. Ukur Waktu Eksekusi Shell Sort
        start_shell = time.perf_counter()
        shell_sort(test_data_1)
        end_shell = time.perf_counter()
        t_shell = (end_shell - start_shell) * 1000  # Ubah ke milidetik (ms)

        # 2. Ukur Waktu Eksekusi Merge Sort
        start_merge = time.perf_counter()
        merge_sort(test_data_2)
        end_merge = time.perf_counter()
        t_merge = (end_merge - start_merge) * 1000  # Ubah ke milidetik (ms)

        print(f"Ukuran Data N = {size:<3} | Shell Sort: {t_shell:.4f} ms | Merge Sort: {t_merge:.4f} ms")
        
    print("=" * 55)
