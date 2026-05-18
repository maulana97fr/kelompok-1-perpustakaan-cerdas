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
        for i, (neighbor, freq) in enumerate(self.adj[isbn_a]):
            if neighbor == isbn_b:
                self.adj[isbn_a][i] = (neighbor, freq + 1)
                found_a = True
                break
        
        if not found_a:
            self.adj[isbn_a].append((isbn_b, 1))
        
        # Cari edge yang sudah ada untuk isbn_b -> isbn_a (graf tak-berarah)
        found_b = False
        for i, (neighbor, freq) in enumerate(self.adj[isbn_b]):
            if neighbor == isbn_a:
                self.adj[isbn_b][i] = (neighbor, freq + 1)
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
                for neighbor, freq in self.adj[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_hop = hop + 1
                        
                        # Tambahkan ke rekomendasi jika dalam batas hop
                        if next_hop <=  max_hop:
                            rekomendasi.append((neighbor, freq, next_hop))
                            queue.append((neighbor, next_hop))
        
        # Urutkan berdasarkan hop (lebih dekat lebih baik), lalu frekuensi (lebih tinggi lebih baik)
        rekomendasi.sort(key=lambda x: (x[2], -x[1]))
        
        return rekomendasi
    
    if __name__ == "__main__":
    graf = GraphRekBuku()
    
    # Tambah data ko-pinjam
    graf.add_copinjam("ISBN001", "ISBN002")
    graf.add_copinjam("ISBN001", "ISBN002")  # Frekuensi naik
    graf.add_copinjam("ISBN001", "ISBN003")
    graf.add_copinjam("ISBN002", "ISBN004")
    graf.add_copinjam("ISBN003", "ISBN005")
    graf.add_copinjam("ISBN004", "ISBN006")
    
    # Rekomendasikan dari ISBN001 dengan max_hop=2
    hasil = graf.rekomendasikan("ISBN001", max_hop=2)
    
    print("Rekomendasi dari ISBN001:")
    for isbn, freq, hop in hasil:
        print(f"  {isbn}: frekuensi={freq}, hop={hop}")
    
    print(f"\nTotal node dijelajahi: {len(hasil) + 1}")  # +1 untuk node sumber