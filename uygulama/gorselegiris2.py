from tkinter import*


pen = Tk()
pen.geometry("400x400")
pen.title("takım")


takimAdi= Label(pen,text="Takim Adı",font=("arial",14), fg="black")
takimAdi.grid(row=0,column=0)
takimRengi1= Label(pen,text="1. Takım Rengi",font=("arial",14), fg="black")
takimRengi1.grid(row=0,column=1)
takimRengi2=Label(pen,text="2. Takım REngi",font=("arial",14),fg="black")
takimRengi2.grid(row=0,column=2)

gsAdi=Label(pen,text="galatasaray",font=("arial",14),fg="black")
gsAdi.grid(row=1,column=0)
gsrenk1=Label(pen,text="      ",font=("arial",14),bg="red")
gsrenk1.grid(row=1,column=1)
gsrenk2=Label(pen,text="      ",font=("arial",14),bg="yellow")
gsrenk2.grid(row=1,column=2)

fbAdi=Label(text="fenerbahce",font=("arial",14),fg="black")
fbAdi.grid(row=2,column=0)
fbrenk1=Label(text="      ",font=("arial",14),bg="yellow")
fbrenk1.grid(row=2,column=1,padx=10)
fbRenk2=Label(text="      " , font=("arial",14),bg="blue")
fbRenk2.grid(row=2,column=2,padx=10)










pen.mainloop()