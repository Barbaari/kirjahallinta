import sqlite3
import tkinter as tk
from tkinter import messagebox

# Luo tietokanta ja taulu, jos niitä ei ole vielä
def luo_tietokanta():
    conn = sqlite3.connect("kirjat.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Lisää kirja tietokantaan
def lisaa_kirja_gui(title, author, year, genre):
    if not title or not author or not year or not genre:
        messagebox.showerror("Virhe", "Kaikki kentät ovat pakollisia!")
        return

    if not year.isdigit():
        messagebox.showerror("Virhe", "Julkaisuvuoden tulee olla numero!")
        return

    try:
        conn = sqlite3.connect("kirjat.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Books (title, author, year, genre) VALUES (?, ?, ?, ?)",
                       (title, author, int(year), genre))
        conn.commit()
        conn.close()
        messagebox.showinfo("Onnistui", "Kirja lisätty onnistuneesti!")
    except sqlite3.Error as e:
        messagebox.showerror("Virhe", f"Tietokantavirhe: {e}")

# Näytä kaikki kirjat
def nayta_kirjat_gui():
    try:
        conn = sqlite3.connect("kirjat.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        conn.close()

        if books:
            result = "\n".join([f"{book[0]}. {book[1]} — {book[2]} ({book[3]}, {book[4]})" for book in books])
        else:
            result = "Ei kirjoja tietokannassa."

        messagebox.showinfo("Kirjat", result)
    except sqlite3.Error as e:
        messagebox.showerror("Virhe", f"Tietokantavirhe: {e}")

# Päivitetty poista kirja -toiminto vetolaatikolla
def paivita_vetolaatikko(option_menu, var):
    """Päivittää vetolaatikon kirjalistan."""
    try:
        conn = sqlite3.connect("kirjat.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM Books")
        books = cursor.fetchall()
        conn.close()

        if books:
            # Päivitä vetolaatikon vaihtoehdot
            menu = option_menu["menu"]
            menu.delete(0, "end")  # Tyhjennä vanhat vaihtoehdot
            for book in books:
                menu.add_command(label=f"{book[0]}: {book[1]}", command=lambda value=book[0]: var.set(value))
            var.set(f"{books[0][0]}: {books[0][1]}")  # Aseta oletusvalinta
        else:
            var.set("Ei kirjoja")
            menu = option_menu["menu"]
            menu.delete(0, "end")
    except sqlite3.Error as e:
        messagebox.showerror("Virhe", f"Tietokantavirhe: {e}")

def poista_kirja_gui_vetolaatikko(book_id):
    """Poistaa kirjan valitun ID:n perusteella."""
    if not book_id.isdigit():
        messagebox.showerror("Virhe", "ID:n tulee olla numero!")
        return

    try:
        conn = sqlite3.connect("kirjat.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Onnistui", "Kirja poistettu!")
        else:
            messagebox.showerror("Virhe", "Kirjaa ei löytynyt annetulla ID:llä.")
    except sqlite3.Error as e:
        messagebox.showerror("Virhe", f"Tietokantavirhe: {e}")

# Luo pääikkuna
def main():
    luo_tietokanta()

    root = tk.Tk()
    root.title("Kirjahallinta")

    # Otsikko
    tk.Label(root, text="Kirjahallinta", font=("Arial", 16)).pack(pady=10)

    # Syötekentät
    tk.Label(root, text="Kirjan nimi:").pack()
    title_entry = tk.Entry(root)
    title_entry.pack()

    tk.Label(root, text="Kirjoittaja:").pack()
    author_entry = tk.Entry(root)
    author_entry.pack()

    tk.Label(root, text="Julkaisuvuosi:").pack()
    year_entry = tk.Entry(root)
    year_entry.pack()

    tk.Label(root, text="Genre:").pack()
    genre_entry = tk.Entry(root)
    genre_entry.pack()

    # Lisää kirja -painike
    tk.Button(root, text="Lisää kirja", command=lambda: lisaa_kirja_gui(
        title_entry.get(),
        author_entry.get(),
        year_entry.get(),
        genre_entry.get()
    )).pack(pady=10)

    # Näytä kirjat -painike
    tk.Button(root, text="Näytä kaikki kirjat", command=nayta_kirjat_gui).pack(pady=10)

    # Poista kirja -osio vetolaatikolla
    tk.Label(root, text="Poista kirja ID:n perusteella:").pack()
    selected_book = tk.StringVar(root)
    selected_book.set("Ei kirjoja")  # Oletusvalinta
    option_menu = tk.OptionMenu(root, selected_book, [])
    option_menu.pack()

    # Päivitä vetolaatikko
    tk.Button(root, text="Päivitä lista", command=lambda: paivita_vetolaatikko(option_menu, selected_book)).pack(pady=5)

    # Poista kirja -painike
    tk.Button(root, text="Poista kirja", command=lambda: poista_kirja_gui_vetolaatikko(selected_book.get().split(":")[0])).pack(pady=10)

    # Sulje-painike
    tk.Button(root, text="Sulje", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()