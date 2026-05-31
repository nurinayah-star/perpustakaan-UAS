from datetime import datetime, timedelta
import heapq
import random
import tkinter as tk
from tkinter import ttk, messagebox

# =============================================================================
# STRUKTUR DATA 1: BINARY SEARCH TREE (BST) UNTUK BUKU
# =============================================================================

class Buku:
    def __init__(self, kode, nama_buku, penulis, penerbit, tahun_terbit, jenis_buku, ketersediaan=1):
        self.kode         = kode
        self.nama_buku    = nama_buku
        self.penulis      = penulis
        self.penerbit     = penerbit
        self.tahun_terbit = tahun_terbit
        self.jenis_buku   = jenis_buku
        self.ketersediaan = ketersedii
        self.left  = None
        self.right = None

 
class BSTBuku:
    def __init__(self):
        self.root      = None
        self.buku_dict = {}

    def insert(self, buku):
        self.root = self._insert(self.root, buku)
        self.buku_dict[buku.kode] = buku

    def _insert(self, root, buku):
        if not root:
            return buku
        if buku.nama_buku.lower() < root.nama_buku.lower():
            root.left  = self._insert(root.left, buku)
        else:
            root.right = self._insert(root.right, buku)
        return root

    def search(self, nama_buku):
        return self._search(self.root, nama_buku)

    def _search(self, root, nama_buku):
        if not root or root.nama_buku.lower() == nama_buku.lower():
            return root
        if nama_buku.lower() < root.nama_buku.lower():
            return self._search(root.left, nama_buku)
        return self._search(root.right, nama_buku)

    def tampilkan_semua(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, root, hasil):
        if root:
            self._inorder(root.left, hasil)
            hasil.append(root)
            self._inorder(root.right, hasil)

    def tampilkan_berdasarkan_jenis(self, jenis):
        semua = self.tampilkan_semua()
        return [b for b in semua if b.jenis_buku.lower() == jenis.lower()]

    def dapatkan_semua_jenis(self):
        return sorted(list({b.jenis_buku for b in self.buku_dict.values()}))


# =============================================================================
# STRUKTUR DATA 2: HASH TABLE UNTUK MAHASISWA
# =============================================================================

class Mahasiswa:
    def __init__(self, nim, nama, prodi, angkatan):
        self.nim      = nim
        self.nama     = nama
        self.prodi    = prodi
        self.angkatan = angkatan


class HashTableMahasiswa:
    def __init__(self):
        self.table = {}

    def tambah_mahasiswa(self, mahasiswa):
        self.table[mahasiswa.nim] = mahasiswa

    def cari_mahasiswa(self, nim):
        return self.table.get(nim, None)

    def semua_mahasiswa(self):
        return list(self.table.values())


# =============================================================================
# STRUKTUR DATA 3: LINKED LIST UNTUK CATATAN PEMINJAMAN
# =============================================================================

class NodePeminjaman:
    def __init__(self, nim, kode_buku, tanggal_pinjam, maks_kembali):
        self.nim             = nim
        self.kode_buku       = kode_buku
        self.tanggal_pinjam  = tanggal_pinjam
        self.maks_kembali    = maks_kembali
        self.tanggal_kembali = None
        self.denda           = 0
        self.next            = None


class LinkedListPeminjaman:
    def __init__(self):
        self.head   = None
        self.tail   = None
        self.ukuran = 0

    def tambah_peminjaman(self, nim, kode_buku, tanggal_pinjam, maks_kembali):
        node_baru = NodePeminjaman(nim, kode_buku, tanggal_pinjam, maks_kembali)
        if not self.head:
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self.ukuran += 1

    def cari_peminjaman_aktif(self, nim, kode_buku):
        current = self.head
        while current:
            if (current.nim == nim and
                    current.kode_buku == kode_buku and
                    current.tanggal_kembali is None):
                return current
            current = current.next
        return None

    def semua_peminjaman(self):
        hasil   = []
        current = self.head
        while current:
            hasil.append(current)
            current = current.next
        return hasil

    def peminjaman_aktif_mahasiswa(self, nim):
        hasil   = []
        current = self.head
        while current:
            if current.nim == nim and current.tanggal_kembali is None:
                hasil.append(current)
            current = current.next
        return hasil

    def semua_peminjaman_selesai(self):
        hasil   = []
        current = self.head
        while current:
            if current.tanggal_kembali is not None:
                hasil.append(current)
            current = current.next
        return hasil

    def semua_peminjaman_dengan_denda(self):
        hasil   = []
        current = self.head
        while current:
            if current.denda > 0:
                hasil.append(current)
            current = current.next
        return hasil


# =============================================================================
# STRUKTUR DATA 4: HEAP UNTUK STATISTIK
# =============================================================================

class IndexPencarianCepat:
    def __init__(self):
        self.buku_counter      = {}
        self.mahasiswa_counter = {}
        self.total_denda       = {}

    def catat(self, nim, kode_buku):
        self.buku_counter[kode_buku]  = self.buku_counter.get(kode_buku, 0) + 1
        self.mahasiswa_counter[nim]   = self.mahasiswa_counter.get(nim, 0) + 1

    def catat_denda(self, nim, jumlah_denda):
        self.total_denda[nim] = self.total_denda.get(nim, 0) + jumlah_denda

    def top_buku(self, n=5):
        return heapq.nlargest(n, self.buku_counter.items(), key=lambda x: x[1])

    def top_mahasiswa(self, n=5):
        return heapq.nlargest(n, self.mahasiswa_counter.items(), key=lambda x: x[1])

    def top_debitur(self, n=5):
        return heapq.nlargest(n, self.total_denda.items(), key=lambda x: x[1])


# =============================================================================
# FUNGSI UTILITAS
# =============================================================================
DENDA_PER_HARI  = 1000
DURASI_PINJAM   = 7

def hitung_denda(tgl_maks_str, tgl_kembali_str):
    fmt           = "%Y-%m-%d"
    tgl_maks      = datetime.strptime(tgl_maks_str, fmt)
    tgl_kembali   = datetime.strptime(tgl_kembali_str, fmt)
    selisih       = (tgl_kembali - tgl_maks).days
    if selisih > 0:
        return selisih * DENDA_PER_HARI
    return 0

# =============================================================================
# INISIALISASI SISTEM & GENERATE DATA DUMMY
# =============================================================================
bst_buku        = BSTBuku()
hash_mahasiswa  = HashTableMahasiswa()
ll_peminjaman   = LinkedListPeminjaman()
index_cepat     = IndexPencarianCepat()

# (Memasukkan 100 Buku dummy Anda)
list_buku = [
    ("B001", "Algoritma dan Pemrograman", "Rinaldi Munir", "Informatika", 2016, "Buku Referensi", 5),
    ("B002", "Struktur Data dan Algoritma", "Moh. Sjukani", "Mitra Wacana", 2015, "Buku Referensi", 3),
    ("B003", "Pemrograman Python", "Charles Severance", "Python.org", 2019, "Buku Referensi", 4),
    ("B004", "Jaringan Komputer", "Andrew Tanenbaum", "Pearson", 2010, "Buku Referensi", 2),
    ("B005", "Basis Data", "Ramez Elmasri", "Pearson", 2015, "Buku Referensi", 3),
    ("B006", "Kecerdasan Buatan", "Stuart Russell", "Pearson", 2020, "Buku Referensi", 2),
    ("B007", "Sistem Operasi", "Abraham Silberschatz", "Wiley", 2018, "Buku Referensi", 3),
    ("B008", "Matematika Diskrit", "Kenneth Rosen", "McGraw-Hill", 2012, "Buku Referensi", 2),
    ("B009", "Analisis Sistem Informasi", "Adi Nugroho", "Andi Offset", 2010, "Buku Referensi", 3),
    ("B010", "Pengantar Teknologi Informasi", "Bambang Wahyudi", "Andi Offset", 2008, "Buku Referensi", 4),
    ("B011", "Pemodelan UML", "Sugiarti", "Graha Ilmu", 2013, "Buku Referensi", 2),
    ("B012", "Rancangan Sistem Digital", "Muhammad Suyanto", "Andi Offset", 2014, "Buku Referensi", 3),
    ("B013", "Keamanan Jaringan Komputer", "William Stallings", "Pearson", 2017, "Buku Referensi", 2),
    ("B014", "Pemrograman Berorientasi Objek", "Deitel & Deitel", "Pearson", 2016, "Buku Referensi", 3),
    ("B015", "Machine Learning", "Tom Mitchell", "McGraw-Hill", 2018, "Buku Referensi", 2),
    ("B016", "Deep Learning", "Ian Goodfellow", "MIT Press", 2016, "Buku Referensi", 2),
    ("B017", "Rekayasa Perangkat Lunak", "Roger Pressman", "McGraw-Hill", 2014, "Buku Referensi", 3),
    ("B018", "Interaksi Manusia dan Komputer", "Dix, Finlay", "Pearson", 2011, "Buku Referensi", 2),
    ("B019", "Komputasi Awan", "Thomas Erl", "Prentice Hall", 2013, "Buku Referensi", 2),
    ("B020", "Pemrograman Web", "Jon Duckett", "Wiley", 2014, "Buku Referensi", 4),
    ("B021", "Algoritma Pemrograman C", "Budi Raharjo", "Informatika", 2012, "Buku Referensi", 3),
    ("B022", "Pemrograman Java", "Herbert Schildt", "McGraw-Hill", 2018, "Buku Referensi", 3),
    ("B023", "Pemrograman Mobile Android", "Nazruddin Safaat", "Informatika", 2015, "Buku Referensi", 2),
    ("B024", "Pengolahan Citra Digital", "Gonzalez & Woods", "Pearson", 2018, "Buku Referensi", 2),
    ("B025", "Kompiler dan Automata", "Aho, Lam, Sethi", "Pearson", 2006, "Buku Referensi", 2),
    ("B026", "Sistem Informasi Manajemen", "Kenneth Laudon", "Pearson", 2020, "Buku Referensi", 3),
    ("B027", "E-Commerce", "Gary Schneider", "Cengage", 2017, "Buku Referensi", 2),
    ("B028", "Data Mining", "Han & Kamber", "Morgan Kaufmann", 2012, "Buku Referensi", 2),
    ("B029", "Big Data Analytics", "Anil Maheshwari", "McGraw-Hill", 2015, "Buku Referensi", 2),
    ("B030", "Internet of Things", "Samuel Greengard", "MIT Press", 2015, "Buku Referensi", 2),
    ("B031", "Blockchain Teknologi", "Melanie Swan", "O'Reilly", 2015, "Buku Referensi", 2),
    ("B032", "Cyber Security", "Michael Rhodes", "Jones & Bartlett", 2016, "Buku Referensi", 2),
    ("B033", "Natural Language Processing", "Daniel Jurafsky", "Pearson", 2019, "Buku Referensi", 1),
    ("B034", "Computer Vision", "Simon Prince", "Cambridge UP", 2012, "Buku Referensi", 1),
    ("B035", "Robotika dan Kendali", "Bruno Siciliano", "Springer", 2010, "Buku Referensi", 2),
    ("B036", "Kalkulus", "James Stewart", "Cengage", 2016, "Buku Matematika", 4),
    ("B037", "Aljabar Linear", "Gilbert Strang", "Wellesley", 2016, "Buku Matematika", 3),
    ("B038", "Statistika Dasar", "Walpole", "Pearson", 2012, "Buku Matematika", 3),
    ("B039", "Probabilitas dan Statistik", "Jay Devore", "Cengage", 2015, "Buku Matematika", 2),
    ("B040", "Matematika Teknik", "Erwin Kreyszig", "Wiley", 2011, "Buku Matematika", 2),
    ("B041", "Habibie & Ainun", "B.J. Habibie", "THC Mandiri", 2010, "Buku Biografi", 4),
    ("B042", "Steve Jobs", "Walter Isaacson", "Simon & Schuster", 2011, "Buku Biografi", 3),
    ("B043", "Elon Musk", "Ashlee Vance", "Ecco Press", 2015, "Buku Biografi", 3),
    ("B044", "Soekarno: Penyambung Lidah", "Cindy Adams", "Gunung Agung", 2011, "Buku Biografi", 2),
    ("B045", "Biografi Tan Malaka", "Harry A. Poeze", "KITLV", 2009, "Buku Biografi", 2),
    ("B046", "Sapiens", "Yuval Noah Harari", "Harper", 2015, "Buku Non-Fiksi", 3),
    ("B047", "Homo Deus", "Yuval Noah Harari", "Harper", 2017, "Buku Non-Fiksi", 2),
    ("B048", "21 Lessons for the 21st Century", "Yuval Noah Harari", "Spiegel & Grau", 2018, "Buku Non-Fiksi", 2),
    ("B049", "Atomic Habits", "James Clear", "Avery", 2018, "Buku Non-Fiksi", 4),
    ("B050", "Thinking Fast and Slow", "Daniel Kahneman", "Farrar Straus", 2011, "Buku Non-Fiksi", 3),
    ("B051", "Laskar Pelangi", "Andrea Hirata", "Bentang Pustaka", 2005, "Buku Fiksi", 5),
    ("B052", "Bumi Manusia", "Pramoedya A. Toer", "Lentera Dipantara", 2005, "Buku Fiksi", 4),
    ("B053", "Tenggelamnya Kapal Van der Wijck", "Hamka", "Gema Insani", 2013, "Buku Fiksi", 3),
    ("B054", "Negeri 5 Menara", "Ahmad Fuadi", "Gramedia", 2009, "Buku Fiksi", 4),
    ("B055", "Perahu Kertas", "Dee Lestari", "Bentang Pustaka", 2009, "Buku Fiksi", 3),
    ("B056", "Sang Pemimpi", "Andrea Hirata", "Bentang Pustaka", 2006, "Buku Fiksi", 3),
    ("B057", "Edensor", "Andrea Hirata", "Bentang Pustaka", 2007, "Buku Fiksi", 2),
    ("B058", "Maryamah Karpov", "Andrea Hirata", "Bentang Pustaka", 2008, "Buku Fiksi", 2),
    ("B059", "Pulang", "Tere Liye", "Republika", 2015, "Buku Fiksi", 3),
    ("B060", "Bintang", "Tere Liye", "Gramedia", 2017, "Buku Fiksi", 3),
    ("B061", "Hujan", "Tere Liye", "Gramedia", 2016, "Buku Fiksi", 4),
    ("B062", "Rindu", "Tere Liye", "Republika", 2014, "Buku Fiksi", 3),
    ("B063", "Serial Harry Potter 1", "J.K. Rowling", "Gramedia", 2002, "Buku Fiksi", 4),
    ("B064", "The Alchemist", "Paulo Coelho", "Gramedia", 2005, "Buku Fiksi", 3),
    ("B065", "Sebuah Seni untuk Bersikap Bodo Amat", "Mark Manson", "Gramedia", 2018, "Buku Non-Fiksi", 5),
    ("B066", "Implementasi BST pada Python", "Ali Budiman", "ITH Press", 2023, "Tugas Akhir Mahasiswa", 1),
    ("B067", "Sistem Informasi Perpustakaan", "Siti Rahmawati", "ITH Press", 2022, "Tugas Akhir Mahasiswa", 1),
    ("B068", "Analisis Sentimen Media Sosial", "Budi Prakoso", "ITH Press", 2023, "Tugas Akhir Mahasiswa", 1),
    ("B069", "Pengenalan Wajah dengan CNN", "Dewi Lestari", "ITH Press", 2022, "Tugas Akhir Mahasiswa", 1),
    ("B070", "Sistem Rekomendasi Film", "Fajar Nugroho", "ITH Press", 2023, "Tugas Akhir Mahasiswa", 1),
    ("B071", "Optimasi Rute dengan Dijkstra", "Hendra Kusuma", "ITH Press", 2021, "Tugas Akhir Mahasiswa", 1),
    ("B072", "Klasifikasi Penyakit dengan ML", "Indah Permata", "ITH Press", 2023, "Tugas Akhir Mahasiswa", 1),
    ("B073", "Aplikasi Mobile Kesehatan", "Jaya Pratama", "ITH Press", 2022, "Tugas Akhir Mahasiswa", 1),
    ("B074", "Deteksi Hoaks Berbasis NLP", "Kevin Halim", "ITH Press", 2023, "Tugas Akhir Mahasiswa", 1),
    ("B075", "Smart Home dengan IoT", "Lina Marlina", "ITH Press", 2022, "Tugas Akhir Mahasiswa", 1),
    ("B076", "Manajemen Proyek IT", "Harold Kerzner", "Wiley", 2017, "Buku Manajemen", 3),
    ("B077", "Kewirausahaan Digital", "Rhenald Kasali", "Gramedia", 2018, "Buku Manajemen", 3),
    ("B078", "Lean Startup", "Eric Ries", "Crown Business", 2011, "Buku Manajemen", 2),
    ("B079", "Good to Great", "Jim Collins", "Harper Business", 2001, "Buku Manajemen", 2),
    ("B080", "Zero to One", "Peter Thiel", "Crown Business", 2014, "Buku Manajemen", 2),
    ("B081", "Bahasa Indonesia untuk Perguruan Tinggi", "Asep Supriadi", "Graha Ilmu", 2014, "Buku Bahasa", 4),
    ("B082", "English for Academic Purposes", "Martin Hewings", "Cambridge UP", 2012, "Buku Bahasa", 3),
    ("B083", "Teknik Menulis Ilmiah", "Nurul Chomaria", "Tiga Serangkai", 2015, "Buku Bahasa", 3),
    ("B084", "Public Speaking Efektif", "Dale Carnegie", "Gramedia", 2010, "Buku Bahasa", 2),
    ("B085", "Seni Berargumen", "Anthony Weston", "Georgetown UP", 2011, "Buku Bahasa", 2),
    ("B086", "Sosiologi Teknologi", "Judy Wajcman", "Open UP", 2004, "Buku Sosial", 2),
    ("B087", "Etika Profesi IT", "Onno W. Purbo", "Andi Offset", 2012, "Buku Sosial", 3),
    ("B088", "Filsafat Ilmu", "Jujun S. Suriasumantri", "Pustaka Sinar", 2009, "Buku Sosial", 2),
    ("B089", "Psikologi Sosial", "David Myers", "McGraw-Hill", 2013, "Buku Sosial", 2),
    ("B090", "Pendidikan Karakter", "Thomas Lickona", "Kreasi Wacana", 2013, "Buku Sosial", 2),
    ("B091", "Elektronika Dasar", "Thomas Floyd", "Pearson", 2012, "Buku Teknik", 3),
    ("B092", "Sistem Kendali Otomatis", "Katsuhiko Ogata", "Pearson", 2010, "Buku Teknik", 2),
    ("B093", "Mikrokontroler Arduino", "Djuandi", "Tobuku", 2011, "Buku Teknik", 3),
    ("B094", "Raspberry Pi Projects", "Simon Monk", "McGraw-Hill", 2014, "Buku Teknik", 2),
    ("B095", "Fisika Komputasi", "Nicholas Giordano", "Pearson", 2006, "Buku Teknik", 2),
    ("B096", "La Tahzan", "Aidh Al-Qarni", "Qisthi Press", 2004, "Buku Motivasi", 5),
    ("B097", "Riyadhus Shalihin", "Imam An-Nawawi", "Gema Insani", 2013, "Buku Agama", 4),
    ("B098", "The Power of Habit", "Charles Duhigg", "Random House", 2012, "Buku Motivasi", 3),
    ("B099", "Mindset: The New Psychology", "Carol Dweck", "Random House", 2006, "Buku Motivasi", 3),
    ("B100", "Rich Dad Poor Dad", "Robert Kiyosaki", "Plata Publishing", 2011, "Buku Motivasi", 4),
]

for data in list_buku:
    bst_buku.insert(Buku(*data))

# (Memasukkan 100 Mahasiswa dummy Anda)
nama_depan = ["Ahmad", "Budi", "Citra", "Dian", "Eko", "Fitri", "Gunawan", "Hani", "Irfan", "Joko", "Kartini", "Lukman", "Maya", "Nanda", "Omar", "Putri", "Reza", "Sari", "Toni", "Umar", "Vera", "Wahyu", "Xena", "Yudi", "Zara", "Andi", "Bagas", "Chika", "Dafa", "Elsa", "Farhan", "Gita", "Hendra", "Ika", "Johan", "Krisna", "Laras", "Miko", "Nina", "Oscar"]
nama_belakang = ["Fauzi", "Santoso", "Dewi", "Pertiwi", "Prasetyo", "Handayani", "Saputra", "Rahayu", "Maulana", "Widodo", "Sari", "Hakim", "Lestari", "Wijaya", "Hidayat", "Ayu", "Kusuma", "Pratama", "Putra", "Halim", "Puspita", "Setiawan", "Ananda", "Ramadan", "Maharani"]

list_mahasiswa = []
for i in range(100):
    nim      = f"241011{i+1:03d}"
    nama     = f"{random.choice(nama_depan)} {random.choice(nama_belakang)}"
    prodi    = random.choice(["Ilmu Komputer", "Sistem Informasi", "Teknik Informatika"])
    angkatan = random.choice([2022, 2023, 2024])
    list_mahasiswa.append((nim, nama, prodi, angkatan))

seen_nim = set()
for data in list_mahasiswa:
    if data[0] not in seen_nim:
        seen_nim.add(data[0])
        hash_mahasiswa.tambah_mahasiswa(Mahasiswa(*data))

# (Memasukkan 50 Peminjaman Selesai & 20 Aktif dummy Anda)
kode_buku_list = [b.kode for b in bst_buku.tampilkan_semua()]
nim_list       = [m.nim for m in hash_mahasiswa.semua_mahasiswa()]
random.seed(42)

peminjaman_selesai = []
used_pairs = set()
count = 0
while count < 50:
    nim       = random.choice(nim_list)
    kode_buku = random.choice(kode_buku_list)
    pair      = (nim, kode_buku, count)
    if pair in used_pairs: continue
    used_pairs.add(pair)
    hari_acak      = random.randint(0, 90)
    tgl_pinjam_obj = datetime(2025, 1, 1) + timedelta(days=hari_acak)
    tgl_pinjam     = tgl_pinjam_obj.strftime("%Y-%m-%d")
    tgl_maks_obj   = tgl_pinjam_obj + timedelta(days=DURASI_PINJAM)
    tgl_maks       = tgl_maks_obj.strftime("%Y-%m-%d")
    if count < 40:
        hari_kembali    = random.randint(1, DURASI_PINJAM)
        tgl_kembali_obj = tgl_pinjam_obj + timedelta(days=hari_kembali)
    else:
        hari_terlambat  = random.randint(1, 14)
        tgl_kembali_obj = tgl_maks_obj + timedelta(days=hari_terlambat)
    tgl_kembali = tgl_kembali_obj.strftime("%Y-%m-%d")
    peminjaman_selesai.append((nim, kode_buku, tgl_pinjam, tgl_maks, tgl_kembali))
    count += 1

peminjaman_aktif = []
count_aktif = 0
while count_aktif < 20:
    nim       = random.choice(nim_list)
    kode_buku = random.choice(kode_buku_list)
    hari_acak      = random.randint(100, 130)
    tgl_pinjam_obj = datetime(2025, 1, 1) + timedelta(days=hari_acak)
    tgl_pinjam     = tgl_pinjam_obj.strftime("%Y-%m-%d")
    tgl_maks_obj   = tgl_pinjam_obj + timedelta(days=DURASI_PINJAM)
    tgl_maks       = tgl_maks_obj.strftime("%Y-%m-%d")
    peminjaman_aktif.append((nim, kode_buku, tgl_pinjam, tgl_maks))
    count_aktif += 1

for nim, kode_buku, tgl_pinjam, tgl_maks, tgl_kembali in peminjaman_selesai:
    ll_peminjaman.tambah_peminjaman(nim, kode_buku, tgl_pinjam, tgl_maks)
    index_cepat.catat(nim, kode_buku)
    node = ll_peminjaman.tail
    node.tanggal_kembali = tgl_kembali
    denda = hitung_denda(tgl_maks, tgl_kembali) if tgl_kembali else 0
    node.denda = denda
    if denda > 0: index_cepat.catat_denda(nim, denda)

for nim, kode_buku, tgl_pinjam, tgl_maks in peminjaman_aktif:
    ll_peminjaman.tambah_peminjaman(nim, kode_buku, tgl_pinjam, tgl_maks)
    index_cepat.catat(nim, kode_buku)
    buku_obj = bst_buku.buku_dict.get(kode_buku)
    if buku_obj and buku_obj.ketersediaan > 0:
        buku_obj.ketersediaan -= 1


# ===============GUIIIII==============================================================

class PerpustakaanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Layanan Perpustakaan ITH")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5") # Background abu-abu terang modern
        
        # --- KONFIGURASI TEMA DAN STYLE (MEMPERCANTIK GUI) ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Style untuk Notebook (Tab)
        style.configure("TNotebook", background="#f0f2f5", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[20, 10], background="#e4e6eb", foreground="#4b4f56")
        style.map("TNotebook.Tab", background=[("selected", "#1877f2")], foreground=[("selected", "white")])
        
        # Style untuk Frame dan LabelFrame
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabelframe", background="#ffffff", borderwidth=2, bordercolor="#dadddf")
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#1c1e21")
        
        # Style untuk Label & Entry
        style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10), foreground="#1c1e21")
        
        # Style untuk Button (Tombol)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#1877f2", foreground="white", padding=8)
        style.map("Primary.TButton", background=[("active", "#166fe5")])
        
        style.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"), background="#e4e6eb", foreground="#4b4f56", padding=8)
        style.map("Secondary.TButton", background=[("active", "#dadddf")])
        
        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background="#fa383e", foreground="white", padding=8)
        style.map("Danger.TButton", background=[("active", "#e32c32")])
        
        # Style untuk Treeview (Tabel)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="#ffffff", fieldbackground="#ffffff", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f0f2f5", foreground="#1c1e21", borderwidth=1)
        style.map("Treeview", background=[("selected", "#e7f3ff")], foreground=[("selected", "#1877f2")])

        # Judul Aplikasi Header
        header_frame = tk.Frame(root, bg="#8A2BE2", height=60)
        header_frame.pack(fill="x", side="top")
        header_label = tk.Label(header_frame, text="SISTEM LAYANAN PERPUSTAKAAN ITH", font=("Segoe UI", 16, "bold"), bg="#8A2BE2", fg="white")
        header_label.pack(pady=15)

        # Membuat Panel Tab Kontrol
        self.tabControl = ttk.Notebook(root)
        
        self.tab_buku = ttk.Frame(self.tabControl)
        self.tab_mhs = ttk.Frame(self.tabControl)
        self.tab_transaksi = ttk.Frame(self.tabControl)
        self.tab_denda = ttk.Frame(self.tabControl)
        self.tab_statistik = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_buku, text=' 📚 Manajemen Buku ')
        self.tabControl.add(self.tab_mhs, text=' 🎓 Manajemen Mahasiswa ')
        self.tabControl.add(self.tab_transaksi, text=' 🔄 Transaksi Peminjaman ')
        self.tabControl.add(self.tab_denda, text=' 💰 Layanan Denda ')
        self.tabControl.add(self.tab_statistik, text=' 📊 Statistik & Laporan ')
        
        self.tabControl.pack(expand=1, fill="both", padx=20, pady=20)
        
        self.init_tab_buku()
        self.init_tab_mhs()
        self.init_tab_transaksi()
        self.init_tab_denda()
        self.init_tab_statistik()

    # --- KELOMPOK TAB BUKU ---
    def init_tab_buku(self):
        # Frame Form
        form_frame = ttk.LabelFrame(self.tab_buku, text=" Registrasi Buku Baru ", padding=20)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        fields = [("Kode Buku:", "b_kode"), ("Nama Buku:", "b_nama"), ("Penulis:", "b_penulis"),
                  ("Penerbit:", "b_penerbit"), ("Tahun Terbit:", "b_tahun"), ("Jenis Buku:", "b_jenis"), 
                  ("Ketersediaan:", "b_stok")]
        
        self.b_entries = {}
        for i, (label_text, var_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=8)
            entry = ttk.Entry(form_frame, width=28, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, pady=8, padx=10)
            self.b_entries[var_name] = entry
            
        ttk.Button(form_frame, text="Simpan Data Buku", style="Primary.TButton", command=self.gui_tambah_buku).grid(row=len(fields), column=0, columnspan=2, pady=20, sticky="ew")
        
        # Frame Display (Tabel)
        display_frame = ttk.Frame(self.tab_buku, padding=10)
        display_frame.pack(side="right", expand=True, fill="both")
        
        search_frame = ttk.Frame(display_frame)
        search_frame.pack(fill="x", pady=10)
        
        ttk.Label(search_frame, text="Cari Judul Buku:").pack(side="left", padx=5)
        self.ent_cari_buku = ttk.Entry(search_frame, width=30, font=("Segoe UI", 10))
        self.ent_cari_buku.pack(side="left", padx=5)
        ttk.Button(search_frame, text="🔍 Cari", style="Primary.TButton", command=self.gui_cari_buku).pack(side="left", padx=5)
        ttk.Button(search_frame, text="🔄 Reset", style="Secondary.TButton", command=self.load_semua_buku).pack(side="left", padx=5)
        
        ttk.Label(search_frame, text="Filter Jenis:").pack(side="left", padx=(25, 5))
        self.cb_jenis = ttk.Combobox(search_frame, state="readonly", width=20, font=("Segoe UI", 10))
        self.cb_jenis.pack(side="left", padx=5)
        self.cb_jenis.bind("<<ComboboxSelected>>", self.gui_filter_jenis_buku)
        
        # Mempercantik Treeview dengan Scrollbar
        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(expand=True, fill="both")
        
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")
        
        self.tree_buku = ttk.Treeview(tree_frame, columns=("kode", "judul", "penulis", "penerbit", "tahun", "jenis", "stok"), show='headings', yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree_buku.yview)
        
        cols = [("kode", "Kode", 70), ("judul", "Judul Buku", 200), ("penulis", "Penulis", 150), 
                ("penerbit", "Penerbit", 120), ("tahun", "Tahun", 60), ("jenis", "Jenis", 120), ("stok", "Stok", 60)]
        for id_col, teks, lebar in cols:
            self.tree_buku.heading(id_col, text=teks)
            self.tree_buku.column(id_col, width=lebar, anchor="center" if id_col in ["kode", "tahun", "stok"] else "w")
            
        self.tree_buku.pack(expand=True, fill="both")
        self.load_semua_buku()

    def load_semua_buku(self):
        for item in self.tree_buku.get_children(): self.tree_buku.delete(item)
        for b in bst_buku.tampilkan_semua():
            self.tree_buku.insert("", "end", values=(b.kode, b.nama_buku, b.penulis, b.penerbit, b.tahun_terbit, b.jenis_buku, b.ketersediaan))
        self.cb_jenis['values'] = bst_buku.dapatkan_semua_jenis()

    def gui_tambah_buku(self):
        try:
            kode = self.b_entries["b_kode"].get().strip()
            nama = self.b_entries["b_nama"].get().strip()
            penulis = self.b_entries["b_penulis"].get().strip()
            penerbit = self.b_entries["b_penerbit"].get().strip()
            tahun = int(self.b_entries["b_tahun"].get().strip())
            jenis = self.b_entries["b_jenis"].get().strip()
            stok = int(self.b_entries["b_stok"].get().strip())
            
            if kode in bst_buku.buku_dict:
                messagebox.showerror("Error", "Kode Buku sudah terdaftar!")
                return
            if not kode or not nama:
                messagebox.showwarning("Peringatan", "Kode dan Nama buku wajib diisi!")
                return
                
            bst_buku.insert(Buku(kode, nama, penulis, penerbit, tahun, jenis, stok))
            messagebox.showinfo("Sukses", f"Buku '{nama}' berhasil ditambahkan!")
            self.load_semua_buku()
            for entry in self.b_entries.values(): entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Tahun dan Stok harus berupa angka!")

    def gui_cari_buku(self):
        query = self.ent_cari_buku.get().strip()
        hasil = bst_buku.search(query)
        for item in self.tree_buku.get_children(): self.tree_buku.delete(item)
        if hasil:
            self.tree_buku.insert("", "end", values=(hasil.kode, hasil.nama_buku, hasil.penulis, hasil.penerbit, hasil.tahun_terbit, hasil.jenis_buku, hasil.ketersediaan))
        else:
            messagebox.showinfo("Hasil", "Buku tidak ditemukan.")

    def gui_filter_jenis_buku(self, event):
        jenis = self.cb_jenis.get()
        hasil = bst_buku.tampilkan_berdasarkan_jenis(jenis)
        for item in self.tree_buku.get_children(): self.tree_buku.delete(item)
        for b in hasil:
            self.tree_buku.insert("", "end", values=(b.kode, b.nama_buku, b.penulis, b.penerbit, b.tahun_terbit, b.jenis_buku, b.ketersediaan))

    # --- KELOMPOK TAB MAHASISWA ---
    def init_tab_mhs(self):
        form_frame = ttk.LabelFrame(self.tab_mhs, text=" Registrasi Mahasiswa ", padding=20)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        fields = [("NIM:", "m_nim"), ("Nama Lengkap:", "m_nama"), ("Program Studi:", "m_prodi"), ("Angkatan:", "m_angkatan")]
        self.m_entries = {}
        for i, (label_text, var_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=10)
            entry = ttk.Entry(form_frame, width=28, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.m_entries[var_name] = entry
            
        ttk.Button(form_frame, text="Daftarkan Mahasiswa", style="Primary.TButton", command=self.gui_tambah_mhs).grid(row=len(fields), column=0, columnspan=2, pady=25, sticky="ew")
        
        display_frame = ttk.Frame(self.tab_mhs, padding=10)
        display_frame.pack(side="right", expand=True, fill="both")
        
        search_frame = ttk.Frame(display_frame)
        search_frame.pack(fill="x", pady=10)
        ttk.Label(search_frame, text="Cari NIM:").pack(side="left", padx=5)
        self.ent_cari_mhs = ttk.Entry(search_frame, width=25, font=("Segoe UI", 10))
        self.ent_cari_mhs.pack(side="left", padx=5)
        ttk.Button(search_frame, text="🔍 Cari", style="Primary.TButton", command=self.gui_cari_mhs).pack(side="left", padx=5)
        ttk.Button(search_frame, text="🔄 Tampilkan Semua", style="Secondary.TButton", command=self.load_semua_mhs).pack(side="left", padx=5)
        
        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(expand=True, fill="both")
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")
        
        self.tree_mhs = ttk.Treeview(tree_frame, columns=("nim", "nama", "prodi", "angkatan"), show='headings', yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree_mhs.yview)
        
        cols = [("nim", "NIM", 120), ("nama", "Nama Lengkap", 250), ("prodi", "Program Studi", 200), ("angkatan", "Angkatan", 100)]
        for id_col, teks, lebar in cols:
            self.tree_mhs.heading(id_col, text=teks)
            self.tree_mhs.column(id_col, width=lebar, anchor="center" if id_col in ["nim", "angkatan"] else "w")
            
        self.tree_mhs.pack(expand=True, fill="both")
        self.load_semua_mhs()

    def load_semua_mhs(self):
        for item in self.tree_mhs.get_children(): self.tree_mhs.delete(item)
        for m in hash_mahasiswa.semua_mahasiswa():
            self.tree_mhs.insert("", "end", values=(m.nim, m.nama, m.prodi, m.angkatan))

    def gui_tambah_mhs(self):
        try:
            nim = self.m_entries["m_nim"].get().strip()
            nama = self.m_entries["m_nama"].get().strip()
            prodi = self.m_entries["m_prodi"].get().strip()
            angkatan = int(self.m_entries["m_angkatan"].get().strip())
            
            if hash_mahasiswa.cari_mahasiswa(nim):
                messagebox.showerror("Error", "NIM sudah terdaftar!")
                return
            if not nim or not nama:
                return
                
            hash_mahasiswa.tambah_mahasiswa(Mahasiswa(nim, nama, prodi, angkatan))
            messagebox.showinfo("Sukses", f"Mahasiswa '{nama}' sukses disimpan!")
            self.load_semua_mhs()
            for entry in self.m_entries.values(): entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Tahun angkatan harus berupa angka!")

    def gui_cari_mhs(self):
        nim = self.ent_cari_mhs.get().strip()
        m = hash_mahasiswa.cari_mahasiswa(nim)
        for item in self.tree_mhs.get_children(): self.tree_mhs.delete(item)
        if m:
            self.tree_mhs.insert("", "end", values=(m.nim, m.nama, m.prodi, m.angkatan))
        else:
            messagebox.showinfo("Kosong", "Mahasiswa tidak ditemukan.")

    # --- KELOMPOK TAB TRANSAKSI ---
    def init_tab_transaksi(self):
        forms_container = ttk.Frame(self.tab_transaksi, padding=10)
        forms_container.pack(side="left", fill="y", padx=10)
        
        # Peminjaman
        f_pinjam = ttk.LabelFrame(forms_container, text=" Form Peminjaman Buku ", padding=20)
        f_pinjam.pack(fill="x", pady=(0, 20))
        ttk.Label(f_pinjam, text="NIM Peminjam:").grid(row=0, column=0, sticky="w", pady=8)
        self.tx_p_nim = ttk.Entry(f_pinjam, width=20, font=("Segoe UI", 10))
        self.tx_p_nim.grid(row=0, column=1, pady=8, padx=10)
        ttk.Label(f_pinjam, text="Kode Buku:").grid(row=1, column=0, sticky="w", pady=8)
        self.tx_p_kode = ttk.Entry(f_pinjam, width=20, font=("Segoe UI", 10))
        self.tx_p_kode.grid(row=1, column=1, pady=8, padx=10)
        ttk.Button(f_pinjam, text="Proses Pinjam", style="Primary.TButton", command=self.gui_pinjam_buku).grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        # Pengembalian
        f_kembali = ttk.LabelFrame(forms_container, text=" Form Pengembalian Buku ", padding=20)
        f_kembali.pack(fill="x")
        ttk.Label(f_kembali, text="NIM Pengembali:").grid(row=0, column=0, sticky="w", pady=8)
        self.tx_k_nim = ttk.Entry(f_kembali, width=20, font=("Segoe UI", 10))
        self.tx_k_nim.grid(row=0, column=1, pady=8, padx=10)
        ttk.Label(f_kembali, text="Kode Buku:").grid(row=1, column=0, sticky="w", pady=8)
        self.tx_k_kode = ttk.Entry(f_kembali, width=20, font=("Segoe UI", 10))
        self.tx_k_kode.grid(row=1, column=1, pady=8, padx=10)
        ttk.Button(f_kembali, text="Proses Kembali", style="Danger.TButton", command=self.gui_kembali_buku).grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        # Log Transaksi
        view_container = ttk.Frame(self.tab_transaksi, padding=10)
        view_container.pack(side="right", expand=True, fill="both")
        
        btn_action_frame = ttk.Frame(view_container)
        btn_action_frame.pack(fill="x", pady=10)
        ttk.Button(btn_action_frame, text="🔄 Segarkan Semua Riwayat", style="Secondary.TButton", command=self.load_semua_peminjaman).pack(side="left", padx=5)
        ttk.Label(btn_action_frame, text=" |  Cari NIM (Aktif):").pack(side="left", padx=10)
        self.ent_filter_log_nim = ttk.Entry(btn_action_frame, width=20, font=("Segoe UI", 10))
        self.ent_filter_log_nim.pack(side="left", padx=5)
        ttk.Button(btn_action_frame, text="Cek Peminjaman Aktif", style="Primary.TButton", command=self.gui_log_aktif_mhs).pack(side="left", padx=5)

        tree_frame = ttk.Frame(view_container)
        tree_frame.pack(expand=True, fill="both")
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")
        
        self.tree_log = ttk.Treeview(tree_frame, columns=("nim", "kode", "tgl_p", "tgl_m", "tgl_k", "denda"), show='headings', yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree_log.yview)
        
        cols = [("nim", "NIM", 100), ("kode", "Kode Buku", 90), ("tgl_p", "Tgl Pinjam", 110),
                ("tgl_m", "Batas Maks", 110), ("tgl_k", "Status / Kembali", 120), ("denda", "Denda", 100)]
        for id_col, teks, lebar in cols:
            self.tree_log.heading(id_col, text=teks)
            self.tree_log.column(id_col, width=lebar, anchor="center")
            
        self.tree_log.pack(expand=True, fill="both")
        self.load_semua_peminjaman()

    def load_semua_peminjaman(self):
        for item in self.tree_log.get_children(): self.tree_log.delete(item)
        for node in ll_peminjaman.semua_peminjaman():
            tk_str = node.tanggal_kembali if node.tanggal_kembali else "🔴 BELUM KEMBALI"
            self.tree_log.insert("", "end", values=(node.nim, node.kode_buku, node.tanggal_pinjam, node.maks_kembali, tk_str, f"Rp {node.denda}"))

    def gui_pinjam_buku(self):
        nim = self.tx_p_nim.get().strip()
        kode = self.tx_p_kode.get().strip()
        
        mhs = hash_mahasiswa.cari_mahasiswa(nim)
        buku = bst_buku.buku_dict.get(kode)
        
        if not mhs:
            messagebox.showerror("Gagal", "Mahasiswa tidak terdaftar.")
            return
        if not buku:
            messagebox.showerror("Gagal", "Buku tidak ditemukan.")
            return
        if buku.ketersediaan <= 0:
            messagebox.showwarning("Kosong", "Stok buku habis!")
            return
            
        tgl_skg = datetime.now().strftime("%Y-%m-%d")
        tgl_maks = (datetime.now() + timedelta(days=DURASI_PINJAM)).strftime("%Y-%m-%d")
        
        ll_peminjaman.tambah_peminjaman(nim, kode, tgl_skg, tgl_maks)
        index_cepat.catat(nim, kode)
        buku.ketersediaan -= 1
        
        messagebox.showinfo("Sukses", f"Berhasil mencatat peminjaman buku '{buku.nama_buku}'")
        self.load_semua_peminjaman()
        self.tx_p_nim.delete(0, tk.END)
        self.tx_p_kode.delete(0, tk.END)

    def gui_kembali_buku(self):
        nim = self.tx_k_nim.get().strip()
        kode = self.tx_k_kode.get().strip()
        
        node = ll_peminjaman.cari_peminjaman_aktif(nim, kode)
        if not node:
            messagebox.showerror("Gagal", "Data peminjaman aktif tidak ditemukan di sistem!")
            return
            
        tgl_skg = datetime.now().strftime("%Y-%m-%d")
        node.tanggal_kembali = tgl_skg
        denda = hitung_denda(node.maks_kembali, tgl_skg)
        node.denda = denda
        
        if denda > 0:
            index_cepat.catat_denda(nim, denda)
            messagebox.showwarning("Terlambat", f"Buku dikembalikan. Anda Terkena Denda: Rp {denda}")
        else:
            messagebox.showinfo("Sukses", "Buku dikembalikan Tepat Waktu!")
            
        buku = bst_buku.buku_dict.get(kode)
        if buku: buku.ketersediaan += 1
        
        self.load_semua_peminjaman()
        self.tx_k_nim.delete(0, tk.END)
        self.tx_k_kode.delete(0, tk.END)

    def gui_log_aktif_mhs(self):
        nim = self.ent_filter_log_nim.get().strip()
        for item in self.tree_log.get_children(): self.tree_log.delete(item)
        for node in ll_peminjaman.peminjaman_aktif_mahasiswa(nim):
            self.tree_log.insert("", "end", values=(node.nim, node.kode_buku, node.tanggal_pinjam, node.maks_kembali, "🔴 BELUM KEMBALI", f"Rp {node.denda}"))

    # --- KELOMPOK TAB DENDA ---
    def init_tab_denda(self):
        display_frame = ttk.Frame(self.tab_denda, padding=20)
        display_frame.pack(expand=True, fill="both")
        
        ctrl_frame = ttk.Frame(display_frame)
        ctrl_frame.pack(fill="x", pady=(0, 15))
        ttk.Button(ctrl_frame, text="🔄 Tampilkan Daftar Pelanggaran", style="Secondary.TButton", command=self.load_peminjaman_denda).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="💰 Rangkuman Total Denda", style="Primary.TButton", command=self.gui_summary_denda).pack(side="left", padx=5)
        
        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(expand=True, fill="both")
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")
        
        self.tree_denda = ttk.Treeview(tree_frame, columns=("nim", "kode", "maks", "kembali", "nominal"), show='headings', yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree_denda.yview)
        
        cols = [("nim", "NIM Mahasiswa", 150), ("kode", "Kode Buku", 120), ("maks", "Batas Waktu", 150), ("kembali", "Dikembalikan Pada", 150), ("nominal", "Denda Terhutang", 150)]
        for id_col, teks, lebar in cols:
            self.tree_denda.heading(id_col, text=teks)
            self.tree_denda.column(id_col, width=lebar, anchor="center")
            
        self.tree_denda.pack(expand=True, fill="both")
        self.load_peminjaman_denda()

    def load_peminjaman_denda(self):
        for item in self.tree_denda.get_children(): self.tree_denda.delete(item)
        for node in ll_peminjaman.semua_peminjaman_dengan_denda():
            self.tree_denda.insert("", "end", values=(node.nim, node.kode_buku, node.maks_kembali, node.tanggal_kembali, f"Rp {node.denda}"))

    def gui_summary_denda(self):
        semua_pelanggar = ll_peminjaman.semua_peminjaman_dengan_denda()
        total_dana = sum(node.denda for node in semua_pelanggar)
        kasus = len(semua_pelanggar)
        messagebox.showinfo("Rangkuman Finansial", f"Total Kasus Keterlambatan : {kasus} Kasus\nAkumulasi Total Denda    : Rp {total_dana}")

    # --- KELOMPOK TAB STATISTIK ---
    def init_tab_statistik(self):
        main_frame = ttk.Frame(self.tab_statistik, padding=20)
        main_frame.pack(expand=True, fill="both")
        
        ttk.Button(main_frame, text="🔄 Perbarui Data Statistik", style="Primary.TButton", command=self.load_statistik_heap).pack(pady=(0, 20))
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True, fill="both")
        
        # Frame Buku Terpopuler
        frame_buku = ttk.LabelFrame(content_frame, text=" 🌟 Top 5 Buku Terpopuler ", padding=15)
        frame_buku.pack(side="left", expand=True, fill="both", padx=10)
        self.txt_buku = tk.Text(frame_buku, width=30, height=15, font=("Consolas", 11), bg="#f8f9fa", fg="#212529", borderwidth=0)
        self.txt_buku.pack(expand=True, fill="both")

        # Frame Mahasiswa Aktif
        frame_mhs = ttk.LabelFrame(content_frame, text=" 🏆 Top 5 Mahasiswa Teraktif ", padding=15)
        frame_mhs.pack(side="left", expand=True, fill="both", padx=10)
        self.txt_mhs = tk.Text(frame_mhs, width=30, height=15, font=("Consolas", 11), bg="#f8f9fa", fg="#212529", borderwidth=0)
        self.txt_mhs.pack(expand=True, fill="both")

        # Frame Debitur
        frame_deb = ttk.LabelFrame(content_frame, text=" 💸 Top 5 Debitur (Denda) ", padding=15)
        frame_deb.pack(side="left", expand=True, fill="both", padx=10)
        self.txt_deb = tk.Text(frame_deb, width=30, height=15, font=("Consolas", 11), bg="#fdf2f2", fg="#c92a2a", borderwidth=0)
        self.txt_deb.pack(expand=True, fill="both")
        
        self.load_statistik_heap()

    def load_statistik_heap(self):
        self.txt_buku.delete('1.0', tk.END)
        for rank, (kode, jumlah) in enumerate(index_cepat.top_buku(5), 1):
            bk = bst_buku.buku_dict.get(kode)
            judul = bk.nama_buku[:20] + ".." if bk and len(bk.nama_buku) > 20 else (bk.nama_buku if bk else kode)
            self.txt_buku.insert(tk.END, f"{rank}. {judul}\n   ({jumlah}x Dipinjam)\n\n")
            
        self.txt_mhs.delete('1.0', tk.END)
        for rank, (nim, jumlah) in enumerate(index_cepat.top_mahasiswa(5), 1):
            m = hash_mahasiswa.cari_mahasiswa(nim)
            nama = m.nama[:20] + ".." if m and len(m.nama) > 20 else (m.nama if m else nim)
            self.txt_mhs.insert(tk.END, f"{rank}. {nama}\n   ({jumlah}x Transaksi)\n\n")
            
        self.txt_deb.delete('1.0', tk.END)
        for rank, (nim, total) in enumerate(index_cepat.top_debitur(5), 1):
            m = hash_mahasiswa.cari_mahasiswa(nim)
            nama = m.nama[:20] + ".." if m and len(m.nama) > 20 else (m.nama if m else nim)
            self.txt_deb.insert(tk.END, f"{rank}. {nama}\n   (Rp {total})\n\n")

if __name__ == "__main__":
    app_root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")  # Menggunakan tema GUI yang lebih bersih dan modern
    app = PerpustakaanGUI(app_root)
    app_root.mainloop()
