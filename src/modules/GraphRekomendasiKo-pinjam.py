class GraphRekBuku:
    """Graf tak-berarah berbobot: edge (A,B,w) = ko-pinjam frekuensi w."""
    def __init__(self):
        self.adj = {}   # isbn -> [(isbn, freq)]

    def add_copinjam(self, isbn_a, isbn_b):
        """Tambah atau naikkan bobot edge. Big-O: O(deg)."""
        # Inisialisasi adjacency list jika belum ada
        if isbn_a not in self.adj:
            self.adj[isbn_a] = []
        if isbn_b not in self.adj:
            self.adj[isbn_b] = []
        
        # Cari edge yang sudah ada untuk isbn_a -> isbn_b
        found_a = False
        for i, (tetangga, freq) in enumerate(self.adj[isbn_a]):
            if tetangga == isbn_b:
                self.adj[isbn_a][i] = (tetangga, freq + 1)
                found_a = True
                break
        
        if not found_a:
            self.adj[isbn_a].append((isbn_b, 1))
        
        # Cari edge yang sudah ada untuk isbn_b -> isbn_a (graf tak-berarah)
        found_b = False
        for i, (tetangga, freq) in enumerate(self.adj[isbn_b]):
            if tetangga == isbn_a:
                self.adj[isbn_b][i] = (tetangga, freq + 1)
                found_b = True
                break
        
        if not found_b:
            self.adj[isbn_b].append((isbn_a, 1))

    def rekomendasikan(self, isbn, max_hop=2):
        """BFS hingga max_hop. Big-O: O(V+E)."""
        if isbn not in self.adj:
            return []
        
        # Inisialisasi untuk BFS
        visited = {isbn}
        queue = [(isbn, 0)]  # (node, hop_level)
        rekomendasi = []  # [(isbn, freq, hop)]
        
        # BFS
        while queue:
            current, hop = queue.pop(0)
            
            # Jelajahi tetangga
            if current in self.adj:
                for tetangga, freq in self.adj[current]:
                    if tetangga not in visited:
                        visited.add(tetangga)
                        next_hop = hop + 1
                        
                        # Tambahkan ke rekomendasi jika dalam batas hop
                        if next_hop <=  max_hop:
                            rekomendasi.append((tetangga, freq, next_hop))
                            queue.append((tetangga, next_hop))
        
        # Urutkan berdasarkan hop (lebih dekat lebih baik), lalu frekuensi (lebih tinggi lebih baik)
        rekomendasi.sort(key=lambda x: (x[2], -x[1]))
        
        return rekomendasi