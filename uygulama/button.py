from tkinter import*

root=Tk()
root.geometry("400x400")
root.title("buton kullanımı")
def metinDegis():
    anaEkran["text"]="butona basıldı"
    anaEkran["bg"]="darkblue"
    anaEkran["fg"]="pink"
def metinTemizle():
    anaEkran["text"]="hello tkinter"
    anaEkran["bg"]="red"
    anaEkran["fg"]="white"




anaEkran = Label(root,text="hello tkinter",font=("arial",14),bg="red")
anaEkran.grid(row=0,column=0)
buton1 = Button(root,text="click",command=metinDegis)
buton1.grid(row=1,column=0)
buton2 = Button(root,text="clar",command=metinTemizle)
buton2.grid(row=2,column=0)


root.mainloop()