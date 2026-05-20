class GraphRekomendasi:
    """Graf tak-berarah berbobot: edge (A,B,w) = ko-pinjam frekuensi w."""
    def __init__(self):
        self.adj = {}

    def add_copinjam(self, isbn_a, isbn_b):
        """Tambah atau naikkan bobot edge. Big-O: O(deg)."""
        # Hindari self-loop
        if isbn_a == isbn_b:
            return

        # Inisialisasi adjacency list jika belum ada
        if isbn_a not in self.adj:
            self.adj[isbn_a] = []

        if isbn_b not in self.adj:
            self.adj[isbn_b] = []

        # Update atau tambah edge untuk node a
        found = False
        for i, (isbn, bobot) in enumerate(self.adj[isbn_a]):
            if isbn == isbn_b:
                self.adj[isbn_a][i] = (isbn, bobot + 1)
                found = True
                break

        if not found:
            self.adj[isbn_a].append((isbn_b, 1))

        # Update atau tambah edge untuk node b (undirected graph)
        found = False
        for i, (isbn, bobot) in enumerate(self.adj[isbn_b]):
            if isbn == isbn_a:
                self.adj[isbn_b][i] = (isbn, bobot + 1)
                found = True
                break

        if not found:
            self.adj[isbn_b].append((isbn_a, 1))
        pass

    def rekomendasikan(self, isbn, max_hop=2):
        """BFS hingga max_hop. Big-O: O(V+E)."""
        if isbn not in self.adj:
            return []

        visited = set([isbn])
        queue = [(isbn, 0)]
        hasil = []

        while queue:
            current, level = queue.pop(0)

            # Batasi kedalaman pencarian
            if level >= max_hop:
                continue

            # Traverse semua tetangga
            for tetangga, bobot in self.adj[current]:
                if tetangga not in visited:
                    visited.add(tetangga)
                    hasil.append((tetangga, bobot))
                    queue.append((tetangga, level + 1))
        pass

        # Sort berdasarkan bobot (descending)
        hasil.sort(key=lambda x: x[1], reverse=True)
        return hasil
