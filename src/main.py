import numpy as np
import random

# JANGAN DIUBAH agar hasil eksperimen dapat direproduksi (Syarat Topik 6)
np.random.seed(13)
random.seed(13)

def main():
    print("========================================")
    print("   SMART LIBRARY MANAGEMENT SYSTEM     ")
    print("========================================")
    print("Ketik 'BANTUAN' untuk melihat perintah.")
    
    while True:
        # Menunggu input perintah dari user
        pilihan = input("\n[Menu Utama] Masukkan Perintah: ").strip().upper()
        
        if pilihan == "KELUAR":
            print("Sistem dimatikan. Sampai jumpa!")
            break
        elif pilihan == "BANTUAN":
            print("\nDaftar Perintah:")
            print("1. CARI_BUKU   : Mencari buku berdasarkan ISBN (BST)")
            print("2. PINJAM      : Menambah antrian peminjaman (Queue)")
            print("3. KEMBALIKAN  : Mengembalikan buku")
            print("4. REKOMENDASI : Melihat rekomendasi buku (Graph)")
            print("5. UNDO        : Membatalkan transaksi terakhir (Stack)")
            print("6. KELUAR      : Menutup aplikasi")
        else:
            print(f"Perintah '{pilihan}' belum tersedia atau sedang dikembangkan.")

if __name__ == "__main__":
    main()