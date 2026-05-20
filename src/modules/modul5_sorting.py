import random
import time

def shell_sort(arr):
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

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
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

def bandingkan_runtime_spesifikasi(transaksi, bst_katalog):
    print("\n=== EVALUASI PERFORMA RUNTIME RUNNING SORTING ===")
    all_books = bst_katalog.inorder()
    for size in [20, 80, 300]:
        test_data1 = []
        for j in range(size):
            buku_ref = all_books[j % len(all_books)]
            val = buku_ref.frek_pinjam if size == 300 else random.randint(1, 50)
            test_data1.append((buku_ref.isbn, val))
        
        test_data2 = list(test_data1)
        
        t0 = time.perf_counter()
        shell_sort(test_data1)
        t_shell = (time.perf_counter() - t0) * 1000
        
        t0 = time.perf_counter()
        merge_sort(test_data2)
        t_merge = (time.perf_counter() - t0) * 1000
        
        print(f"Ukuran Data N = {size:<3} | Shell Sort: {t_shell:.4f} ms | Merge Sort: {t_merge:.4f} ms")
    print("=" * 60)