import csv
import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

#зчитування та вивід даних
def read_print():
    with open('clients.csv', 'r', encoding ='utf-8') as file:
        r = csv.reader(file)
        orders = list(r)

    orderss = pd.DataFrame(orders[1:], columns = orders[0])
    orderss['Сума замовлення'] = pd.to_numeric(orderss['Сума замовлення'])
    orders_info = orderss.to_string(index = False)
    messagebox.showinfo('Список замовлень', orders_info)
    return orderss

#  додавання замовлення
def add_order(orderss):
    name = simpledialog.askstring("Введіть ім\'я клієнта ", "Ім\'я:")
    if name is None:
        return orderss
    
    number_order = simpledialog.askstring("Введіть номер замовлення", "номер замовлення:")
    if number_order is None:
        return orderss
    
    date_order = simpledialog.askinteger("Введіть дату замовлення", "Дата замовлення(у форматі: рік-місяць-число):")
    if date_order is None:
        return orderss
    
    price = simpledialog.askfloat("Введіть суму замовлення ", "Сума замовлення:")
    if price is None:
        return orderss
    
    status = simpledialog.askfloat("Введіть статус замовлення ", "Статус замовлення(ви можете ввести лише один з них: В процесі або Виконано):")
    if status is None:
        return orderss

    
    pr = {'Ім\'я клієнта': name, 'Номер замовлення': number_order, 'Дата замовлення': date_order, 'Сума замовлення': price, 'Статус' : status}
    orderss.loc[len(orderss)] = pr
    
   
    with open('clients.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=pr.keys())
        writer.writerow(pr)

    messagebox.showinfo("вдалося", "додано!")
    return orderss

# видалити замовлення за номером
def delete(orderss):
    del_number_order = simpledialog.askstring('Вкажіть номер зпмовлення', "Номер зпмовлення:")
    if del_number_order is None:
        return orderss
    
    if del_number_order in orderss['Номер замовлення'].values:
        orderss = orderss[orderss['Номер замовлення'] != del_number_order]
        orderss.to_csv('clients.csv', index=False, encoding='utf-8')
        messagebox.showinfo("вдалося", "видалено!")
    else:
        messagebox.showwarning("Не знайдено", "Замовлення не знайдено!")
    
    return orderss
#діаграма 
def diagram_for_categories(orderss):
    gr_by_status = orderss.groupby('Статус')
    quants = gr_by_status['Статус']
    

    fig, ax = plt.subplots()
    ax.set_title('Статуси')
    ax.pie(quants, autopct= '%1.1f%%' )
    plt.show()
    


root = tk.Tk()
root.geometry('600x600')

def load_and_display():
    global orderss
    orderss = read_print()

buttom1 = tk.Button(text ='Зчитати та вивести дані', command = read_print)
buttom1.pack()

buttom2 = tk.Buttom(text = 'Додати замовлення', command =lambda: add_order(orderss))
buttom2.pack()

buttom3 = tk.Buttom(text = 'Видалити замовлення за номером', command=lambda: delete(orderss))
buttom3.pack()

buttom4 = tk.Buttom(text = 'Видалити замовлення за номером', command=lambda: diagram_for_categories(orderss))
buttom4.pack()

root.mainloop()