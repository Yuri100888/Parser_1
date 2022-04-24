from tkinter import *
import sale as func

window = Tk()
window.title("Акции интернет-магазина '7745.by' ")
<<<<<<< HEAD
window.geometry('700x330')


def hi(url):
    print(url[0])
    print(url[1])

categories = LabelFrame(text='Выберите категорию', width=50)
=======
window.geometry('')


categories = LabelFrame(text='Выберите категорию', width=50, padx=5, pady=5)
>>>>>>> 975389e (отредактрирован размер окна,удалена временная функция)
categories.pack()
button_all_categoories = Button(categories, text='Все категории', width=30, height=7, command=lambda i=func.get_sale(): func.all_sale_categori(i) )
button_all_categoories.grid(row=0, rowspan=4, column=1)

for i in func.get_sale():
    Button(categories, text=str(i[0]), width=30, command=lambda i=(str(i[1]),str(i[4]), str(i[0])): func.sale_category(i)).grid(row=i[3], column=i[2], padx=5, pady=3)

window.mainloop()