import tkinter as tk
from tkinter import messagebox
import sqlite3


def veri_tabani_olustur():
    connection = sqlite3.connect("kullanici_veritabani.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kullanici_adi TEXT NOT NULL UNIQUE,
                        sifre TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE)''')
    connection.commit()
    connection.close()


def kaydet(entryKullanici, entrySifre, entrySifre2, entryMail, kayitSayfasi):
    kullanici_adi = entryKullanici.get()
    sifre = entrySifre.get()
    sifre2 = entrySifre2.get()
    mail = entryMail.get()

   
    if not kullanici_adi or not sifre or not sifre2 or not mail:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
        return

    if sifre != sifre2:
        messagebox.showerror("Hata", "Şifreler uyuşmuyor!")
        return

    try:
       
        connection = sqlite3.connect("kullanici_veritabani.db")
        cursor = connection.cursor()

     
        cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre, email) VALUES (?, ?, ?)",
                       (kullanici_adi, sifre, mail))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Kayıt başarılı!")

       
        entryKullanici.delete(0, tk.END)
        entrySifre.delete(0, tk.END)
        entrySifre2.delete(0, tk.END)
        entryMail.delete(0, tk.END)

        kayitSayfasi.destroy() 
        giris_sayfasi()  

    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror("Hata", "Kullanıcı adı veya e-posta zaten kayıtlı!")
        else:
            messagebox.showerror("Hata", "Bir hata oluştu, tekrar deneyin.")


def ana_pencere():
    import tkinter as tk
    import customtkinter as ctk
    import sqlite3
    from tkinter import ttk, messagebox

  
    db = sqlite3.connect("proje_yonetimi.db")
    cursor = db.cursor()

  
    cursor.execute('''CREATE TABLE IF NOT EXISTS projeler (
        proje_adi TEXT,
        sorumlu_kisi TEXT,
        toplantı_tarihi TEXT,
        deadline TEXT,
        detaylar TEXT
    )''')
    db.commit()

    
    def fetch_data():
        query = "SELECT proje_adi, sorumlu_kisi, toplantı_tarihi, deadline, detaylar FROM projeler"
        cursor.execute(query)
        return cursor.fetchall()

    def tablo_verileri_gir():
        for item in tree.get_children():
            tree.delete(item)

        for row in fetch_data():
            tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

    def kayit_ekleme_sayfasi():
        def kayit_ekle():
            proje_adi = entry_proje_adi.get()
            sorumlu_kisi = entry_sorumlu_kisi.get()
            toplantı_tarihi = entry_toplantı_tarihi.get()
            deadline = entry_deadline.get()
            detaylar = entry_detaylar.get()

            if proje_adi and sorumlu_kisi and toplantı_tarihi and deadline:
                cursor.execute(
                    "INSERT INTO projeler (proje_adi, sorumlu_kisi, toplantı_tarihi, deadline, detaylar) VALUES (?, ?, ?, ?, ?)",
                    (proje_adi, sorumlu_kisi, toplantı_tarihi, deadline, detaylar)
                )
                db.commit()
                tablo_verileri_gir()
                entry_proje_adi.delete(0, tk.END)
                entry_sorumlu_kisi.delete(0, tk.END)
                entry_toplantı_tarihi.delete(0, tk.END)
                entry_deadline.delete(0, tk.END)
                entry_detaylar.delete(0, tk.END)
            else:
                messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

        try:
            add_window = ctk.CTkToplevel(root)
            add_window.title("Yeni Kayıt Ekle")
            add_window.geometry("500x400")

            root.after(100, lambda: add_window.lift())
            root.after(100, lambda: add_window.focus_force())

            
            ctk.CTkLabel(add_window, text="Proje Adı:").grid(row=0, column=0, padx=20, pady=10, sticky="w")
            entry_proje_adi = ctk.CTkEntry(add_window)
            entry_proje_adi.grid(row=0, column=1, padx=20, pady=10, sticky="w")

            
            ctk.CTkLabel(add_window, text="Sorumlu Kişi:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
            entry_sorumlu_kisi = ctk.CTkEntry(add_window)
            entry_sorumlu_kisi.grid(row=1, column=1, padx=20, pady=10, sticky="w")

            
            ctk.CTkLabel(add_window, text="Toplantı Tarihi:").grid(row=2, column=0, padx=20, pady=10, sticky="w")
            entry_toplantı_tarihi = ctk.CTkEntry(add_window)
            entry_toplantı_tarihi.grid(row=2, column=1, padx=20, pady=10, sticky="w")

            
            ctk.CTkLabel(add_window, text="Deadline:").grid(row=3, column=0, padx=20, pady=10, sticky="w")
            entry_deadline = ctk.CTkEntry(add_window)
            entry_deadline.grid(row=3, column=1, padx=20, pady=10, sticky="w")

            
            ctk.CTkLabel(add_window, text="Proje Detayları:").grid(row=4, column=0, padx=20, pady=10, sticky="w")
            entry_detaylar = ctk.CTkEntry(add_window)
            entry_detaylar.grid(row=4, column=1, padx=20, pady=10, sticky="w")

            
            add_button = ctk.CTkButton(add_window, text="Ekle", command=kayit_ekle)
            add_button.grid(row=5, column=0, columnspan=2, pady=20)
        except Exception as e:
            print(f"Hata oluştu: {e}")
            messagebox.showerror("Hata", f"Pencere açılırken bir hata oluştu: {e}")

    
    def detay_sayfasi(proje_adi):
        cursor.execute("SELECT sorumlu_kisi, detaylar FROM projeler WHERE proje_adi = ?", (proje_adi,))
        proje = cursor.fetchone()

        detail_window = ctk.CTkToplevel(root)
        detail_window.title("Proje Detayları")
        detail_window.geometry("400x200")

        ctk.CTkLabel(detail_window, text="Sorumlu Kişi:", font=("Arial", 12, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(detail_window, text=proje[0], font=("Arial", 10)).grid(row=0, column=1, sticky="W")

        ctk.CTkLabel(detail_window, text="Proje Detayları:", font=("Arial", 12, "bold")).grid(row=1, column=0)
        ctk.CTkLabel(detail_window, text=proje[1], font=("Arial", 10)).grid(row=1, column=1)


    root = ctk.CTk()
    root.title("Proje Yönetim Tablosu")
    root.geometry("900x600")


    columns = ("Proje Adı", "Sorumlu Kişi", "Toplantı Tarihi", "Deadline")

    frame = ctk.CTkFrame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    tree.heading("Proje Adı", text="Proje Adı")
    tree.heading("Sorumlu Kişi", text="Sorumlu Kişi")
    tree.heading("Toplantı Tarihi", text="Toplantı Tarihi")
    tree.heading("Deadline", text="Deadline")

    tree.column("Proje Adı", width=200, anchor="center")
    tree.column("Sorumlu Kişi", width=150, anchor="center")
    tree.column("Toplantı Tarihi", width=150, anchor="center")
    tree.column("Deadline", width=150, anchor="center")

    
    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

   
    tablo_verileri_gir()

    
    def tablo_veri_tiklama(event):
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, "values")
            proje_adi = item_values[0]
            detay_sayfasi(proje_adi)

    tree.bind("<Double-1>", tablo_veri_tiklama)

   
    add_window_button = ctk.CTkButton(root, text="Yeni Kayıt Ekle", command=kayit_ekleme_sayfasi)
    add_window_button.pack(pady=20)

    root.mainloop()

  
    cursor.close()
    db.close()



def giris_sayfasi():
    def giris():
        kullanici_adi = entryKullanici.get().strip()
        sifre = entrySifre.get().strip()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve şifreyi doldurun!")
            return

        try:
            
            connection = sqlite3.connect("kullanici_veritabani.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
            user = cursor.fetchone()
            connection.close()

            if user:
                messagebox.showinfo("Başarılı Giriş", "Başarılı giriş yaptınız!")
                girisSayfasi.destroy()
                ana_pencere()
            else:
                messagebox.showerror("Hatalı Giriş", "Kullanıcı adı veya şifre hatalı!")

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

    def kayit_sayfasi_ac():
        girisSayfasi.destroy()  
        kayit_sayfasi() 

    girisSayfasi = tk.Tk()
    girisSayfasi.title("Giriş Yap")
    girisSayfasi.geometry("500x300")
    girisSayfasi.configure(bg='pink')

    frame = tk.Frame(girisSayfasi, bg='pink')

 
    labelBaslik = tk.Label(frame, text="Giriş Yap", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelBaslik.grid(row=0, column=1, columnspan=1, pady=20)

    labelKullanici = tk.Label(frame, text="Kullanıcı Adı", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelKullanici.grid(row=2, column=0)

    labelSifre = tk.Label(frame, text="Şifre", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelSifre.grid(row=3, column=0)

    entryKullanici = tk.Entry(frame)
    entryKullanici.grid(row=2, column=1)

    entrySifre = tk.Entry(frame, show="*")
    entrySifre.grid(row=3, column=1)

    girisButonu = tk.Button(frame, text="Giriş", bg="pink", command=giris)
    girisButonu.grid(row=4, column=0, columnspan=2, pady=20)

    kayitButonu = tk.Button(frame, text="Kayıt Ol", bg="lightblue", command=kayit_sayfasi_ac)
    kayitButonu.grid(row=5, column=0, columnspan=2, pady=10)

    frame.pack()
    girisSayfasi.mainloop()


def kayit_sayfasi():
    kayitSayfasi = tk.Tk()
    kayitSayfasi.title("Kayıt Ol")
    kayitSayfasi.geometry("500x300")
    kayitSayfasi.configure(bg='pink')

    frame = tk.Frame(bg='pink')

    labelBaslik = tk.Label(frame, text="Kayıt Ol", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='white')
    labelBaslik.grid(row=0, column=1, columnspan=1, pady=20)
    labelKullanici = tk.Label(frame, text="Kullanıcı Adı", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelKullanici.grid(row=2, column=0, sticky="E")
    labelSifre = tk.Label(frame, text="Şifre Giriniz", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelSifre.grid(row=3, column=0, sticky="E")
    labelSifre2 = tk.Label(frame, text="Şifreyi Tekrar Giriniz", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelSifre2.grid(row=4, column=0, sticky="E")
    labelMail = tk.Label(frame, text="Mail Adresi Giriniz", font=("liberation sans narrow bold", 10, "normal"), bg='pink', fg='black')
    labelMail.grid(row=5, column=0, sticky="E")

    entryKullanici = tk.Entry(frame)
    entryKullanici.grid(row=2, column=1)
    entrySifre = tk.Entry(frame, show="*")
    entrySifre.grid(row=3, column=1)
    entrySifre2 = tk.Entry(frame, show="*")
    entrySifre2.grid(row=4, column=1)
    entryMail = tk.Entry(frame)
    entryMail.grid(row=5, column=1)

    kayitButonu = tk.Button(frame, text="Kayıt Ol", bg="lightblue", command=lambda: kaydet(entryKullanici, entrySifre, entrySifre2, entryMail, kayitSayfasi))
    kayitButonu.grid(row=6, column=1, columnspan=2, pady=20)

    frame.pack()

    kayitSayfasi.mainloop()


veri_tabani_olustur()


giris_sayfasi()
