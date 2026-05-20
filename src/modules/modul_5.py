# modul5_sorting.py
# Deskripsi: Shell Sort (durasi descending) dan Merge Sort (frekuensi peminjaman populer)

def shell_sort(data):
    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            while j >= gap and data[j-gap].durasi_hari < temp.durasi_hari:
                data[j] = data[j-gap]
                j -= gap
            data[j] = temp
        gap //= 2
    return data

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    hasil = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i].frek_pinjam > right[j].frek_pinjam:
            hasil.append(left[i])
            i += 1
        else:
            hasil.append(right[j])
            j += 1
    hasil.extend(left[i:])
    hasil.extend(right[j:])
    return hasil
