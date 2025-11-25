# ==============================================================
# APLIKASI PREDIKSI FAKULTAS BERDASARKAN NILAI SISWA
# Menggunakan Python, Tkinter, dan SQLite
# ==============================================================
# Fitur:
# 1. Menyimpan data nilai siswa ke database SQLite
# 2. Menampilkan ID otomatis setiap data
# 3. Prediksi prodi berdasarkan nilai tertinggi
#    - Biologi  -> Kedokteran
#    - Fisika   -> Teknik
#    - Inggris  -> Bahasa
# 4. Update data berdasarkan ID
# 5. Delete data berdasarkan ID
# 6. Dilengkapi komentar penjelasan di setiap bagian
# ==============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ================== KONEKSI & SETUP DATABASE ==================
# Membuat / menghubungkan ke database SQLite
conn = sqlite3.connect('nilai_siswa.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi TEXT
)
''')
conn.commit()

# ================== FUNGSI PREDIKSI PRODI ==================
def prediksi_prodi(bio, fis, ing):
    """
    Fungsi ini menentukan prodi berdasarkan nilai tertinggi.
    Parameter:
    bio = nilai Biologi
    fis = nilai Fisika
    ing = nilai Inggris
    """
    nilai_tertinggi = max(bio, fis, ing)

    if nilai_tertinggi == bio:
        return "Kedokteran"
    elif nilai_tertinggi == fis:
        return "Teknik"
    else:
        return "Bahasa"

# ================== FUNGSI SUBMIT DATA ==================
def submit_data():
    """Menyimpan data siswa ke database"""
    nama = entry_nama.get()
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())

    hasil = prediksi_prodi(bio, fis, ing)

    cursor.execute("INSERT INTO siswa (nama, biologi, fisika, inggris, prediksi) VALUES (?,?,?,?,?)",
                   (nama, bio, fis, ing, hasil))
    conn.commit()

    tampilkan_data()
    messagebox.showinfo("Sukses", "Data berhasil disimpan")

# ================== FUNGSI UPDATE DATA ==================
def update_data():
    """Mengubah data berdasarkan ID"""
    id_data = entry_id.get()

    cursor.execute("""
        UPDATE siswa SET
        nama=?, biologi=?, fisika=?, inggris=?, prediksi=?
        WHERE id=?
    """, (
        entry_nama.get(),
        entry_bio.get(),
        entry_fis.get(),
        entry_ing.get(),
        prediksi_prodi(int(entry_bio.get()), int(entry_fis.get()), int(entry_ing.get())),
        id_data
    ))

    conn.commit()
    tampilkan_data()

# ================== FUNGSI DELETE DATA ==================
def delete_data():
    """Menghapus data berdasarkan ID"""
    id_data = entry_id.get()

    cursor.execute("DELETE FROM siswa WHERE id = ?", (id_data,))
    conn.commit()
    tampilkan_data()

# ================== MENAMPILKAN DATA KE TABEL ==================
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM siswa")
    for data in cursor.fetchall():
        tree.insert('', tk.END, values=data)

# ================== GUI TKINTER ==================
root = tk.Tk()
root.title("Prediksi Fakultas Berdasarkan Nilai Siswa")
root.geometry("850x500")

# ================== FORM INPUT ==================
tk.Label(root, text="ID Data").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

# Input Nama
tk.Label(root, text="Nama Siswa").grid(row=1, column=0)
entry_nama = tk.Entry(root)
entry_nama.grid(row=1, column=1)

# Input Nilai Biologi
tk.Label(root, text="Nilai Biologi").grid(row=2, column=0)
entry_bio = tk.Entry(root)
entry_bio.grid(row=2, column=1)

# Input Nilai Fisika
tk.Label(root, text="Nilai Fisika").grid(row=3, column=0)
entry_fis = tk.Entry(root)
entry_fis.grid(row=3, column=1)

# Input Nilai Inggris
tk.Label(root, text="Nilai Inggris").grid(row=4, column=0)
entry_ing = tk.Entry(root)
entry_ing.grid(row=4, column=1)

# ================== TOMBOL ==================
tk.Button(root, text="Submit Nilai", command=submit_data).grid(row=5, column=0)
tk.Button(root, text="Update Data", command=update_data).grid(row=5, column=1)
tk.Button(root, text="Delete Data", command=delete_data).grid(row=5, column=2)

# ================== TABEL DATA ==================
columns = ("ID", "Nama", "Biologi", "Fisika", "Inggris", "Prediksi")

tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.grid(row=6, column=0, columnspan=3, pady=20)

# Menampilkan data saat aplikasi dijalankan
tampilkan_data()

# Menjalankan aplikasi
root.mainloop()
