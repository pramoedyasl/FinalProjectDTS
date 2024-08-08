import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Membuat atau menghubungkan ke database SQLite
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Membuat tabel untuk menyimpan data penjualan
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    date TEXT NOT NULL
)
''')
conn.commit()

# Fungsi untuk menambah data penjualan ke database
def add_sales():
    product_name = entry_product.get()
    amount = entry_amount.get()
    date = entry_date.get()
    
    if product_name and amount and date:
        cursor.execute('''
        INSERT INTO sales (product_name, amount, date)
        VALUES (?, ?, ?)
        ''', (product_name, amount, date))
        conn.commit()
        messagebox.showinfo("Success", "Data has been added!")
    else:
        messagebox.showwarning("Warning", "Please fill all fields")

# Fungsi untuk menampilkan grafik penjualan
def show_graph():
    cursor.execute('SELECT product_name, SUM(amount) FROM sales GROUP BY product_name')
    data = cursor.fetchall()
    
    if data:
        products = [row[0] for row in data]
        amounts = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(products, amounts, color='blue')
        ax.set_title('Sales Data')
        ax.set_xlabel('Product')
        ax.set_ylabel('Amount Sold')

        for widget in frame_graph.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.get_tk_widget().pack()
        canvas.draw()
    else:
        messagebox.showwarning("Warning", "No data to display")

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title('Sales Data Analysis')
root.geometry('800x600')

# Frame untuk memasukkan data penjualan
frame_input = tk.Frame(root)
frame_input.pack(pady=20)

tk.Label(frame_input, text="Product Name:").grid(row=0, column=0, padx=10, pady=5)
entry_product = tk.Entry(frame_input)
entry_product.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Amount:").grid(row=1, column=0, padx=10, pady=5)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_input, text="Add Sales Data", command=add_sales).grid(row=3, column=0, columnspan=2, pady=10)

# Frame untuk menampilkan grafik
frame_graph = tk.Frame(root)
frame_graph.pack(pady=20)

tk.Button(root, text="Show Sales Graph", command=show_graph).pack(pady=10)

root.mainloop()

# Menutup koneksi ke database saat aplikasi ditutup
conn.close()
