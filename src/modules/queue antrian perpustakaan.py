# =========================================================
# QUEUE LINKED LIST
# =========================================================
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # =====================================================
    # ENQUEUE
    # Menambahkan data ke belakang antrian
    # Big-O = O(1)
    # =====================================================
    def enqueue(self, data):
        new_node = Node(data)

        # Jika queue kosong
        if self.tail is None:
            self.head = new_node
            self.tail = new_node

        # Jika queue sudah ada isi
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    # =====================================================
    # DEQUEUE
    # Mengambil data paling depan
    # Big-O = O(1)
    # =====================================================
    def dequeue(self):
        # Jika queue kosong
        if self.head is None:
            return None

        # Ambil data paling depan
        data = self.head.data

        # Geser head ke node berikutnya
        self.head = self.head.next

        # Jika queue menjadi kosong
        if self.head is None:
            self.tail = None

        self.size -= 1

        return data

    # =====================================================
    # BATAL PESAN
    # Menghapus data tertentu dari queue
    # Big-O = O(n)
    # =====================================================
    def batal_pesan(self, nim):
        prev = None
        cur = self.head

        while cur:

            # Jika data ditemukan
            if cur.data == nim:

                # Jika data di head
                if prev is None:
                    self.head = cur.next

                # Jika data di tengah / belakang
                else:
                    prev.next = cur.next

                # Jika data di tail
                if cur == self.tail:
                    self.tail = prev

                self.size -= 1

                return True

            prev = cur
            cur = cur.next

        return False

    # =====================================================
    # TAMPILKAN ANTRIAN
    # Big-O = O(n)
    # =====================================================
    def tampil(self):
        hasil = []
        cur = self.head

        while cur:
            hasil.append(cur.data)
            cur = cur.next

        return hasil

    # =====================================================
    # CEK APAKAH QUEUE KOSONG
    # =====================================================
    def is_empty(self):
        return self.size == 0

    # =====================================================
    # MELIHAT DATA PALING DEPAN
    # =====================================================
    def peek(self):
        if self.head is None:
            return None

        return self.head.data

    # =====================================================
    # JUMLAH ANTRIAN
    # =====================================================
    def jumlah_antrian(self):
        return self.size