from tkinter import *
import sale as func
import buttons_func as bf

window = Tk()
window.title("Акции интернет-магазина '7745.by' ")

window.geometry('700x330')

window.geometry('')

categories = LabelFrame(text='Выберите категорию', width=50, padx=5, pady=5)

categories.pack()
button_all_categoories = Button(categories, text='Все категории\n(не рекомендуется нажимать\nиз-за времени ожидания)',
                                width=30, height=3, bg='red', activebackground='green',
                                command=lambda: bf.all_sale_categori())
button_all_categoories.grid(row=0, rowspan=2, column=1)

for i in func.get_sale():
    Button(categories, text=str(i[0]), width=30, activebackground='green',
           command=lambda i=(str(i[0]), str(i[1]), str(i[4])): bf.sale_category(i)).grid(row=i[3], column=i[2], padx=5,
                                                                                         pady=3)

window.mainloop()
