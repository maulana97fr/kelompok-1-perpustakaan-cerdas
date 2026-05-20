# modul4_graph.py
# Deskripsi: Graf tidak berarah berbobot untuk mencatat pola ko-pinjam buku dengan BFS

class GraphRekomendasi:
    def __init__(self):
        self.adj = {}

    def add_edge(self, a, b):
        if a == b:
            return
        if a not in self.adj:
            self.adj[a] = []
        if b not in self.adj:
            self.adj[b] = []

        found = False
        for i, (isbn, bobot) in enumerate(self.adj[a]):
            if isbn == b:
                self.adj[a][i] = (isbn, bobot + 1)
                found = True
                break
        if not found:
            self.adj[a].append((b, 1))

        found = False
        for i, (isbn, bobot) in enumerate(self.adj[b]):
            if isbn == a:
                self.adj[b][i] = (isbn, bobot + 1)
                found = True
                break
        if not found:
            self.adj[b].append((a, 1))

    def bfs_rekomendasi(self, start, max_hop=2):
        if start not in self.adj:
            return []
        visited = set([start])
        queue = [(start, 0)]
        hasil = []
        while queue:
            current, level = queue.pop(0)
            if level >= max_hop:
                continue
            for tetangga, bobot in self.adj[current]:
                if tetangga not in visited:
                    visited.add(tetangga)
                    hasil.append((tetangga, bobot))
                    queue.append((tetangga, level + 1))
        hasil.sort(key=lambda x: x[1], reverse=True)
        return hasil