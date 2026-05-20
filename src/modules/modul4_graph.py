from src.data_structures.graph import Graph

class Graph:
    def __init__(self):
        # Menggunakan dictionary untuk Adjacency List
        # Key: Judul Buku / ISBN, Value: List dari buku-buku yang terhubung (tetangga)
        self.adj_list = {}

    def add_vertex(self, buku):
        if buku not in self.adj_list:
            self.adj_list[buku] = []
            return True
        return False

    def add_edge(self, buku1, buku2):
        # Menghubungkan dua buku secara bolak-balik (Undirected Graph)
        if buku1 in self.adj_list and buku2 in self.adj_list:
            if buku2 not in self.adj_list[buku1]:
                self.adj_list[buku1].append(buku2)
            if buku1 not in self.adj_list[buku2]:
                self.adj_list[buku2].append(buku1)
            return True
        return False

    def get_recommendations(self, buku):
        # Mengambil semua tetangga yang terhubung langsung dengan buku tersebut
        return self.adj_list.get(buku, [])

    def display_graph(self):
        for vertex in self.adj_list:
            print(f"{vertex} -> {', '.join(self.adj_list[vertex])}")