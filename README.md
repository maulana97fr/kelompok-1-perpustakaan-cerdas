# Kelompok-1 Smart Library Management &amp; Recommendation System
# MATA KULIAH
- **ALGORITMA DAN STRUKTUR DATA**
- **S1 TEKNIK ELEKTRO**
- **UNIVERSITAS NEGERI YOGYAKARTA**
# DESKRIPSI PROJECT
Project ini merupakan pembahasan mengenai pengembangan sistem perpustakaan pintar dengan memanfaatkan berbagai konsep pada mata kuliah ini. Sistem ini dibuat untuk membantu pengelolaan buku, proses peminjaman, pengembalian, antrian pemesanan, hingga pemberian rekomendasi buku secara otomatis.
# Struktur Data
- 1. Binary Search Tree (BST)

BST digunakan untuk menyimpan data katalog buku berdasarkan ISBN. Struktur ini mempermudah proses pencarian, penambahan, dan pengurutan data buku secara lebih cepat dibanding pencarian linear.

Operasi utama:

Insert buku
Search buku
Traversal inorder

Kompleksitas:

Average-case: O(log n)
Worst-case: O(n) 
- 2. Queue

Queue digunakan untuk mengatur antrian pemesanan buku dengan metode FIFO (First In First Out), sehingga pengguna yang memesan lebih dulu akan dilayani terlebih dahulu.

Operasi utama:

Enqueue
Dequeue

Kompleksitas:

O(1)
- 3. Stack

Stack digunakan untuk menyimpan riwayat transaksi dan mendukung fitur undo transaksi menggunakan metode LIFO (Last In First Out).

Operasi utama:

Push
Pop
Peek

Kompleksitas:

O(1)
- 4. Graph

Graph digunakan pada fitur rekomendasi buku untuk menggambarkan hubungan antar buku berdasarkan riwayat peminjaman pengguna.

Algoritma yang digunakan:

Breadth First Search (BFS)

Kompleksitas:

O(V + E)
- 5. Linked List

Linked List digunakan sebagai dasar implementasi Queue dan Stack untuk mempermudah pengelolaan node data secara dinamis.

Keunggulan:

Tidak perlu ukuran tetap
Mudah menambah dan menghapus data

### Pembagian Tugas Kelompok
- **Maulana Fatihah Rizki_25051030075**: Implementasi BST (Katalog Buku) & Fondasi Data Structures (Linked List).
- **Nasya Afina Suharta_25051030068**: Implementasi Sorting (Laporan Bulanan) & Analisis Performa (Runtime).
- **Faisal Abdullah Hamood Hazaea_25051030061**: Implementasi Stack (Riwayat Transaksi & Undo).
- **Fairuz Addzikri Hakim_25051030063**: Implementasi Queue (Antrian Pemesanan).
- **Erlangga Supranoto Anggota_25051030041**: Implementasi Graph (Sistem Rekomendasi Ko-pinjam).

#
