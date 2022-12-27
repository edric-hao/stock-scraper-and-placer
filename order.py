import tkinter as tk
from datetime import datetime
import os
import csv
from datetime import timedelta
from config import get

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=300, relief='raised')
root.geometry('400x325')
root.resizable(0,0)
canvas.pack()

status = tk.StringVar()
status.set('')
message = tk.Label(root, textvariable=status)
message.pack(fill='x')

def main_menu():
    Button1 = tk.Button(canvas, text='Login', command=lambda: [canvas.delete('all'), login()])
    Button2 = tk.Button(canvas, text='Sign Up', command=lambda: [canvas.delete('all'), sign_up()])
    canvas.create_window(200, 100, window=Button1)
    canvas.create_window(200, 140, window=Button2)

def sign_up():
    label1 = tk.Label(canvas, text='Please enter your First Metro account name and password')
    label1.config(font=('helvetica', 10))
    canvas.create_window(200, 50, window=label1)
    label2 = tk.Label(canvas, text='Username:')
    label2.config(font=('helvetica', 10))
    canvas.create_window(100, 100, window=label2)
    label3 = tk.Label(canvas, text='Password:')
    label3.config(font=('helvetica', 10))
    canvas.create_window(100, 150, window=label3)
    entry1 = tk.Entry(canvas)
    canvas.create_window(250, 100, window=entry1)
    entry2 = tk.Entry(canvas)
    canvas.create_window(250, 150, window=entry2)
    Button1 = tk.Button(canvas, text='Back', command=lambda: [canvas.delete('all'), main_menu()])
    canvas.create_window(125, 200, window=Button1)
    Button2 = tk.Button(canvas, text='Enter', command=lambda: [canvas.delete('all'), new_account(entry1.get(), entry2.get())])
    canvas.create_window(275, 200, window=Button2)

def new_account(username, password):
    with open('config.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([username, password])
    main_menu()

def login():
    label1 = tk.Label(canvas, text='First Metro Order Placer')
    label1.config(font=('helvetica', 15))
    canvas.create_window(200, 50, window=label1)
    label2 = tk.Label(canvas, text='Username')
    label2.config(font=('helvetica', 10))
    canvas.create_window(125, 125, window=label2)
    entry1 = tk.Entry(canvas)
    canvas.create_window(225, 125, window=entry1)
    label3 = tk.Label(canvas, text='Password')
    label3.config(font=('helvetica', 10))
    canvas.create_window(125, 175, window=label3)
    entry2 = tk.Entry(canvas)
    canvas.create_window(225, 175, window=entry2)
    Button1 = tk.Button(canvas, text='Back', command=lambda: [canvas.delete('all'), main_menu()])
    canvas.create_window(125, 225, window=Button1)
    Button2 = tk.Button(canvas, text='Enter', command=lambda: checker(entry1.get(),entry2.get()))
    canvas.create_window(275, 225, window=Button2)

def checker(username,password):
    print(username)
    print(password)
    canvas.delete('all')
    correct = False
    with open('config.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row)==2:
                if row[0]==username and row[1]==password:
                    correct = True
    if correct:
        place_order(username)
    else:
        status.set('Incorrect Username or Password')
        login()

def place_order(username):
    label1 = tk.Label(canvas, text='Enter Order')
    label1.config(font=('helvetica', 10))
    canvas.create_window(200, 50, window=label1)
    label2 = tk.Label(canvas, text='TRANS')
    label2.config(font=('helvetica', 10))
    canvas.create_window(100, 100, window=label2)
    label3 = tk.Label(canvas, text='STOCK')
    label3.config(font=('helvetica', 10))
    canvas.create_window(100, 125, window=label3)
    label4 = tk.Label(canvas, text='QTY')
    label4.config(font=('helvetica', 10))
    canvas.create_window(100, 150, window=label4)
    label5 = tk.Label(canvas, text='PRICE')
    label5.config(font=('helvetica', 10))
    canvas.create_window(100, 175, window=label5)
    label6 = tk.Label(canvas, text='TERM')
    label6.config(font=('helvetica', 10))
    canvas.create_window(100, 200, window=label6)
    entry1 = tk.Entry(canvas)
    canvas.create_window(250, 125, window=entry1)
    entry2 = tk.Entry(canvas)
    canvas.create_window(250, 150, window=entry2)
    entry3 = tk.Entry(canvas)
    canvas.create_window(250, 175, window=entry3)
    type = tk.StringVar(value='buy')
    Radiobutton1 = tk.Radiobutton(canvas, text='BUY', padx=20, variable=type, value='buy')
    Radiobutton2 = tk.Radiobutton(canvas, text='SELL', padx=20, variable=type, value='sell')
    canvas.create_window(212.5, 100, window=Radiobutton1)
    canvas.create_window(287.5, 100, window=Radiobutton2)
    options = {'DAY', 'GTW', 'GTM'}
    term = tk.StringVar(value='DAY')
    drop_down= tk.OptionMenu(canvas , term, *options)
    canvas.create_window(225, 200, window=drop_down)
    button1 = tk.Button(canvas, text='Back', command=lambda: [canvas.delete('all'), login()])
    button2 = tk.Button(canvas, text='SUBMIT', command=lambda: [canvas.delete('all'), valid(username, type.get(), entry1.get(), entry2.get(), entry3.get(), term.get())])
    canvas.create_window(100, 250, window=button1)
    canvas.create_window(300, 250, window=button2)

def valid(username, type, stock, qty, price, term):
    exist = False
    check1 = False
    check2 = False
    validity1 = False
    validity2 = False
    try:
        qty = int(qty)
        check1 = True
    except:
        pass
    try:
        try:
            if float(price) <= 0:
                raise
            check2 = True
            price = float(price)
        except:
            print('not a float')
            if int(price) <= 0:
                raise
            check2 = True
            price = int(price)
    except:
        pass
    today = datetime.today()
    table = [[0.0001, 0.0099, 0.0001], [0.010, 0.049, 0.001], [0.050, 0.249, 0.001], [0.250, 0.495, 0.005],[0.50, 4.99, 0.01], [5.00, 9.99, 0.01], [10.00, 19.98, 0.02],[20.00, 49.95, 0.05], [50.00, 99.95, 0.05],[100.00, 199.90, 0.1], [200.00, 499.80, 0.2], [500.00, 999.50, 0.5], [1000, 1999, 1], [2000, 4998, 2]]
    while True:
        try:
            path = 'stock_data\\' + today.strftime('%m-%d-%y') + '.csv'
            with open(path, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row[0]==stock:
                        exist = True
                        if check1:
                            if qty%int(row[9])==0:
                                validity1 = True
                        if check2:
                            if price>=float(row[3].replace(',',''))*0.5 and price<=float(row[3].replace(',',''))*1.5:
                                for row in table:
                                    if price >= row[0] and price <= row[1]:
                                        if (price / row[2]).is_integer():
                                            validity2 = True
                                if price >= 5000.0000:
                                    if (price/5.0000).is_integer():
                                        validity2 = True
            break
        except Exception as e:
            status.set(e)
            if today.strftime('%Y-%m-%d') > '2020-04-25':
                today = today - timedelta(days=1)
            else:
                status.set('missing stock data')
                break
    if exist:
        if not validity1:
            status.set('Invalid quantity')
        if not validity2:
            status.set('Invalid price')
    else:
        status.set('Invalid stock code')
        place_order(username)
    if not (validity1 and validity2):
        place_order(username)
    else:
        receipt(username, type, stock, qty, price, term)

def receipt(username, type, stock, qty, price, term):
    label1 = tk.Label(canvas, text='Receipt')
    label1.config(font=('helvetica', 10))
    canvas.create_window(200, 50, window=label1)
    label2 = tk.Label(canvas, text='TRANS:')
    label2.config(font=('helvetica', 10))
    canvas.create_window(125, 100, window=label2)
    label3 = tk.Label(canvas, text='STOCK:')
    label3.config(font=('helvetica', 10))
    canvas.create_window(125, 125, window=label3)
    label4 = tk.Label(canvas, text='QTY:')
    label4.config(font=('helvetica', 10))
    canvas.create_window(125, 150, window=label4)
    label5 = tk.Label(canvas, text='PRICE:')
    label5.config(font=('helvetica', 10))
    canvas.create_window(125, 175, window=label5)
    label6 = tk.Label(canvas, text='TERM:')
    label6.config(font=('helvetica', 10))
    canvas.create_window(125, 200, window=label6)
    label7 = tk.Label(canvas, text='Password:')
    label7.config(font=('helvetica', 10))
    canvas.create_window(125, 225, window=label7)
    value1 = tk.Label(canvas, text= type)
    value1.config(font=('helvetica', 10))
    canvas.create_window(250, 100, window=value1)
    value2 = tk.Label(canvas, text=stock)
    value2.config(font=('helvetica', 10))
    canvas.create_window(250, 125, window=value2)
    value3 = tk.Label(canvas, text=str(qty))
    value3.config(font=('helvetica', 10))
    canvas.create_window(250, 150, window=value3)
    value4 = tk.Label(canvas, text=str(price))
    value4.config(font=('helvetica', 10))
    canvas.create_window(250, 175, window=value4)
    value5 = tk.Label(canvas, text=term)
    value5.config(font=('helvetica', 10))
    canvas.create_window(250, 200, window=value5)
    entry = tk.Entry(canvas)
    canvas.create_window(250, 225, window=entry)
    button1 = tk.Button(canvas, text='Back', command=lambda: [canvas.delete('all'), place_order(username)])
    button2 = tk.Button(canvas, text='Enter', command=lambda: confirm(username, entry.get(), type, stock, qty, price, term))
    canvas.create_window(125, 275, window=button1)
    canvas.create_window(275, 275, window=button2)

def confirm(username, password, type, stock, qty, price, term):
    canvas.delete('all')
    if password != get(username):
        receipt(username, type, stock, qty, price, term)
    else:
        path = os.path.join('auto_place', username + '.csv')
        if not os.path.isdir('auto_place'):
            os.mkdir('auto_place')
        if not os.path.isfile(path):
            with open(path, 'w+', newline='') as file:
                pass
        with open(path, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([type, stock, qty, price, term])
        place_order(username)

main_menu()
root.mainloop()