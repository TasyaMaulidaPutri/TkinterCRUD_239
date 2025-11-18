import sqlite3                 # digunakan untuk membuat dan mengelola database SQLite
import tkinter as tk           # modul GUI utama Tkinter
import tkinter.messagebox as msg   # untuk menampilkan pop-up alert, error, info
from tkinter import ttk        # ttk digunakan untuk widget modern seperti Treeview


# ======================================================
#                 FUNGSI DATABASE
# ======================================================

def koneksi():
    # Membuat koneksi ke database SQLite bernama nilai.db
    # Jika file belum ada, SQLite otomatis membuat file baru
    return sqlite3.connect("nilai.db")


def create_table():
    # Membuat tabel nilai_siswa jika tabel belum pernah dibuat
    # Tabel berisi nama siswa, nilai biologi, fisika, inggris, dan prediksi fakultas
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()


def insert_nilai(nama, bio, fis, ing, fakultas):
    # Menyimpan satu data siswa ke tabel nilai_siswa
    # Data yang disimpan termasuk hasil prediksi fakultas
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, fakultas))
    con.commit()
    con.close()


def read_nilai():
    # Membaca seluruh data siswa dari database
    # Data akan ditampilkan di Treeview (tabel GUI)
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows


# Membuat tabel ketika program pertama kali dijalankan
create_table()


# ======================================================
#                CLASS GUI APLIKASI
# ======================================================

class NilaiGUI(tk.Tk):
    def __init__(self):
        # Mengatur window utama Tkinter
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai Siswa")
        self.geometry("650x450")

        # Frame untuk menampung input
        frm = tk.Frame(self, padx=12, pady=12)
        frm.pack(fill="x")

        # Form input nama siswa
        tk.Label(frm, text="Nama Siswa").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frm)
        self.ent_nama.grid(row=0, column=1, pady=5)

        # Form input nilai biologi
        tk.Label(frm, text="Nilai Biologi").grid(row=1, column=0, sticky="w")
        self.ent_bio = tk.Entry(frm)
        self.ent_bio.grid(row=1, column=1, pady=5)

        # Form input nilai fisika
        tk.Label(frm, text="Nilai Fisika").grid(row=2, column=0, sticky="w")
        self.ent_fis = tk.Entry(frm)
        self.ent_fis.grid(row=2, column=1, pady=5)

        # Form input nilai inggris
        tk.Label(frm, text="Nilai Inggris").grid(row=3, column=0, sticky="w")
        self.ent_ing = tk.Entry(frm)
        self.ent_ing.grid(row=3, column=1, pady=5)

        # Tombol submit untuk menyimpan nilai siswa
        tk.Button(
            frm, text="Submit Nilai", width=15,
            command=self.submit
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # Tombol refresh untuk memperbarui tabel
        tk.Button(
            frm, text="Refresh", width=15,
            command=self.load_data
        ).grid(row=5, column=0, columnspan=2)

        # ======================================================
        #               TREEVIEW UNTUK TAMPIL DATA
        # ======================================================

        # Mendefinisikan kolom tabel
        cols = ("id", "nama", "bio", "fis", "ing", "prediksi")

        # Membuat komponen Treeview
        self.tree = ttk.Treeview(self, columns=cols, show="headings")

        # Mengatur nama kolom
        for col in cols:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True, padx=12, pady=12)

        # Memuat data awal
        self.load_data()


    # ======================================================
    #             LOGIKA PREDIKSI FAKULTAS
    # ======================================================

    def prediksi_fakultas(self, bio, fis, ing):
        # Menentukan fakultas berdasarkan nilai tertinggi
        # Aturan:
        # - Tertinggi Biologi → Kedokteran
        # - Tertinggi Fisika → Teknik
        # - Tertinggi Inggris → Bahasa
        nilai = {"Biologi": bio, "Fisika": fis, "Inggris": ing}

        # Mencari mata pelajaran dengan nilai paling tinggi
        tertinggi = max(nilai, key=nilai.get)

        if tertinggi == "Biologi":
            return "Kedokteran"
        elif tertinggi == "Fisika":
            return "Teknik"
        else:
            return "Bahasa"


    # ======================================================
    #                 TOMBOL SUBMIT
    # ======================================================

    def submit(self):
        # Mengambil input dari form
        try:
            nama = self.ent_nama.get()
            bio = int(self.ent_bio.get())
            fis = int(self.ent_fis.get())
            ing = int(self.ent_ing.get())
        except:
            # Error jika input bukan angka
            msg.showerror("Error", "Semua nilai harus berupa angka!")
            return

        # Menentukan prediksi fakultas
        prediksi = self.prediksi_fakultas(bio, fis, ing)

        # Menyimpan data ke database
        insert_nilai(nama, bio, fis, ing, prediksi)

        # Notifikasi berhasil
        msg.showinfo("Berhasil", f"Prediksi Fakultas: {prediksi}")

        # Refresh tabel
        self.load_data()

        # Mengosongkan input
        self.ent_nama.delete(0, tk.END)
        self.ent_bio.delete(0, tk.END)
        self.ent_fis.delete(0, tk.END)
        self.ent_ing.delete(0, tk.END)


    # ======================================================
    #                 LOAD DATA TABLE
    # ======================================================

    def load_data(self):
        # Menghapus seluruh isi tabel sebelum mengisi ulang
        for r in self.tree.get_children():
            self.tree.delete(r)

        # Membaca semua data dari database
        rows = read_nilai()

        # Menampilkan data satu per satu
        for r in rows:
            self.tree.insert("", tk.END, values=r)



# ======================================================
#                     JALANKAN APLIKASI
# ======================================================

if __name__ == "__main__":
    app = NilaiGUI()
    app.mainloop()