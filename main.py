import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
import sqlite3
from configparser import ConfigParser

root = tk.Tk()
root.title('program')
root.attributes('-topmost', True)
# root.overrideredirect(True)

root.resizable(width=True, height=True)

app_width = 1000
app_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

my_font = Font(family='Brush Script MT', size=20, weight='bold', slant='italic')

parser = ConfigParser()
parser.read('treebase.txt')
save_primary_color = parser.get('color', 'primary_color')
save_second_color = parser.get('color', 'second_color')
save_highlight_color = parser.get('color', 'highlight_color')


def query_database():
    for i in my_tree.get_children():
        my_tree.delete(i)
    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('SELECT rowid, * FROM customers')
    records = c.fetchall()
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('evenrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        else:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('oddrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        count += 1
    conn.commit()
    conn.close()


def primary_color():
    pri_color = colorchooser.askcolor()[1]

    if pri_color:
        # my_tree.tag_configure('oddrow', background='white')
        my_tree.tag_configure('evenrow', background=pri_color)

        parser = ConfigParser()
        parser.read('treebase.txt')
        parser.set('color', 'primary_color', pri_color)

        with open('treebase.txt', 'w') as configfile:
            parser.write(configfile)


def second_color():
    se_color = colorchooser.askcolor()[1]

    if se_color:
        my_tree.tag_configure('oddrow', background=se_color)
        # my_tree.tag_configure('evenrow', background='white')

        parser = ConfigParser()
        parser.read('treebase.txt')
        parser.set('color', 'second_color', se_color)

        with open('treebase.txt', 'w') as configfile:
            parser.write(configfile)


def highlight_color():
    high_color = colorchooser.askcolor()[1]

    if high_color:
        style.map('Treeview', background=[('selected', high_color)])

        parser = ConfigParser()
        parser.read('treebase.txt')
        parser.set('color', 'high_color', high_color)

        with open('treebase.txt', 'w') as configfile:
            parser.write(configfile)


def reset_color():
    parser = ConfigParser()
    parser.read('treebase.txt')
    parser.set('color', 'primary_color', 'lightblue')
    parser.set('color', 'second_color', 'white')
    parser.set('color', 'high_color', '#347083')

    with open('treebase.txt', 'w') as configfile:
        parser.write(configfile)

    my_tree.tag_configure('oddrow', background=save_second_color)
    my_tree.tag_configure('evenrow', background=save_primary_color)

    style.map('Treeview', background=[('selected', save_highlight_color)])


def search_record():
    lookup_re = search_entry.get()
    win.destroy()

    for i in my_tree.get_children():
        my_tree.delete(i)

    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('SELECT rowid, * FROM customers WHERE last_name = ?', (lookup_re,))

    records = c.fetchall()
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('evenrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        else:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('oddrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        count += 1
    conn.commit()
    conn.close()


def lookup_record():
    global win, search_entry

    win = tk.Toplevel(root)
    win.title('lookup record')
    win.geometry('400x200')

    search_frame = tk.LabelFrame(win, text='last name')
    search_frame.pack(padx=10, pady=10)

    search_entry = tk.Entry(search_frame, font=my_font)
    search_entry.pack(padx=20, pady=20)

    search_btn = tk.Button(win, text='search record', command=search_record)
    search_btn.pack(padx=20, pady=20)


my_menu = tk.Menu(root)
root.config(menu=my_menu)

option_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='option', menu=option_menu)
option_menu.add_command(label='primary color', command=primary_color)
option_menu.add_command(label='second color', command=second_color)
option_menu.add_command(label='highlight color', command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label='reset color', command=reset_color)
option_menu.add_separator()
option_menu.add_command(label='exit', command=root.quit)

search_menu = tk.Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='search', menu=search_menu)
search_menu.add_command(label='lookup record', command=lookup_record)
search_menu.add_separator()
search_menu.add_command(label='start over', command=query_database)

conn = sqlite3.connect('tree_crm.db')
c = conn.cursor()

c.execute('''CREATE TABLE if not exists customers (
       first_name text,
       last_name text,
       id integer,
       address text,
       city text,
       state text,
       zipcode text)
        ''')
"""data = [
    ['cuong', 'bui', '1', 'me linh', 'ha noi', 'single', '2020602992'],
    ['duc', 'ngo', '2', 'binh phu', 'hung yen', 'dating', '2020603596'],
    ['dien', 'dinh', '3', 'cam pha', 'quang ninh', 'vague', '2020607182'],
    ['dat', 'pham', '4', 'co le', 'nam dinh', 'vague', '2020530912'],
    ['dat', 'nguyen', '5', 'lien mac', 'ha noi', 'vague', '2020212902'],
]
for i in data:
    c.execute('INSERT INTO customers VALUES (:first_name, :last_name, :id, :address, :city, :state, :zipcode)',
              {
                  'first_name': i[0],
                  'last_name': i[1],
                  'id': i[2],
                  'address': i[3],
                  'city': i[4],
                  'state': i[5],
                  'zipcode': i[6]
              })"""
conn.commit()
conn.close()

"""def query_database():
    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('SELECT rowid, * FROM customers')
    records = c.fetchall()
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('evenrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        else:
            my_tree.insert(parent='', index=tk.END, iid=count, text='', tags=('oddrow'),
                           values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]))
        count += 1
    conn.commit()
    conn.close()"""

style = ttk.Style()

style.theme_use('default')

style.configure('Treeview',
                background='#D3D3D3',
                foreground='black',
                rowheight=25,
                fieldbackground='#D3D3D3')

style.map('Treeview', background=[('selected', save_highlight_color)])

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

x_scroll = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
y_scroll = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)

x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

my_tree = ttk.Treeview(tree_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, selectmode=tk.EXTENDED)
my_tree.pack()

x_scroll.config(command=my_tree.xview)
y_scroll.config(command=my_tree.yview)

my_tree['columns'] = ('firstname', 'lastname', 'id', 'address', 'city', 'state', 'zipcode')
my_tree.column('#0', width=0, stretch=tk.NO)
my_tree.column('firstname', anchor=tk.W, width=140)
my_tree.column('lastname', anchor=tk.W, width=140)
my_tree.column('id', anchor=tk.CENTER, width=140)
my_tree.column('address', anchor=tk.CENTER, width=140)
my_tree.column('city', anchor=tk.CENTER, width=140)
my_tree.column('state', anchor=tk.CENTER, width=140)
my_tree.column('zipcode', anchor=tk.CENTER, width=140)

my_tree.heading('#0', text='', anchor=tk.W)
my_tree.heading('firstname', text='first name', anchor=tk.W)
my_tree.heading('lastname', text='last name', anchor=tk.W)
my_tree.heading('id', text='id', anchor=tk.CENTER)
my_tree.heading('address', text='address', anchor=tk.CENTER)
my_tree.heading('city', text='city', anchor=tk.CENTER)
my_tree.heading('state', text='state', anchor=tk.CENTER)
my_tree.heading('zipcode', text='zipcode', anchor=tk.CENTER)

"""data = [
    ['cuong', 'bui', '1', 'me linh', 'ha noi', 'single', '2020602992'],
    ['duc', 'ngo', '2', 'binh phu', 'hung yen', 'dating', '2020603596'],
    ['dien', 'dinh', '3', 'cam pha', 'quang ninh', 'vague', '2020607182'],
    ['dat', 'pham', '4', 'co le', 'nam dinh', 'vague', '2020530912'],
    ['dat', 'nguyen', '5', 'lien mac', 'ha noi', 'vague', '2020212902'],
]
"""
my_tree.tag_configure('oddrow', background=save_second_color)
my_tree.tag_configure('evenrow', background=save_primary_color)

data_frame = tk.LabelFrame(root, text='record')
data_frame.pack(fill=tk.X, expand=True, padx=20)

fn_lbl = tk.Label(data_frame, text='first name')
fn_entry = tk.Entry(data_frame)

fn_lbl.grid(row=0, column=0, padx=10, pady=10)
fn_entry.grid(row=0, column=1, padx=10, pady=10)

ln_lbl = tk.Label(data_frame, text='last name')
ln_entry = tk.Entry(data_frame)

ln_lbl.grid(row=0, column=2, padx=10, pady=10)
ln_entry.grid(row=0, column=3, padx=10, pady=10)

id_lbl = tk.Label(data_frame, text='id')
id_entry = tk.Entry(data_frame)

id_lbl.grid(row=0, column=4, padx=10, pady=10)
id_entry.grid(row=0, column=5, padx=10, pady=10)

add_lbl = tk.Label(data_frame, text='address')
add_entry = tk.Entry(data_frame)

add_lbl.grid(row=1, column=0, padx=10, pady=10)
add_entry.grid(row=1, column=1, padx=10, pady=10)

ct_lbl = tk.Label(data_frame, text='city')
ct_entry = tk.Entry(data_frame)

ct_lbl.grid(row=1, column=2, padx=10, pady=10)
ct_entry.grid(row=1, column=3, padx=10, pady=10)

st_lbl = tk.Label(data_frame, text='state')
st_entry = tk.Entry(data_frame)

st_lbl.grid(row=1, column=4, padx=10, pady=10)
st_entry.grid(row=1, column=5, padx=10, pady=10)

zc_lbl = tk.Label(data_frame, text='zipcode')
zc_entry = tk.Entry(data_frame)

zc_lbl.grid(row=1, column=6, padx=10, pady=10)
zc_entry.grid(row=1, column=7, padx=10, pady=10)


def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('DELETE from customers WHERE oid=' + id_entry.get())

    conn.commit()
    conn.close()

    clear_entry()

    messagebox.showinfo('delete!', 'you record has been deleted')


def remove_many():
    response = messagebox.askyesno('delete!', 'are you sure?')

    ids_to_delete = []
    if response == 1:
        x = my_tree.selection()

        for j in x:
            ids_to_delete.append(my_tree.item(j, 'values')[2])

        for i in x:
            my_tree.delete(i)
        conn = sqlite3.connect('tree_crm.db')
        c = conn.cursor()

        c.executemany('DELETE FROM customers WHERE id = ?', [(k,) for k in ids_to_delete])

        conn.commit()
        conn.close()

        clear_entry()


def remove_all():
    response = messagebox.askyesno('delete!', 'are you sure?')

    if response == 1:
        for i in my_tree.get_children():
            my_tree.delete(i)

        conn = sqlite3.connect('tree_crm.db')
        c = conn.cursor()

        c.execute('DROP TABLE customers')

        conn.commit()
        conn.close()

        clear_entry()
        create_table_again()


def move_up():
    rows = my_tree.selection()
    for i in rows:
        my_tree.move(i, my_tree.parent(i), my_tree.index(i) - 1)


def move_down():
    rows = my_tree.selection()
    for i in reversed(rows):
        my_tree.move(i, my_tree.parent(i), my_tree.index(i) + 1)


def clear_entry():
    fn_entry.delete(0, tk.END)
    ln_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    add_entry.delete(0, tk.END)
    ct_entry.delete(0, tk.END)
    st_entry.delete(0, tk.END)
    zc_entry.delete(0, tk.END)


def select_record(e):
    clear_entry()

    selected = my_tree.focus()
    value = my_tree.item(selected, 'values')

    fn_entry.insert(0, value[0])
    ln_entry.insert(0, value[1])
    id_entry.insert(0, value[2])
    add_entry.insert(0, value[3])
    ct_entry.insert(0, value[4])
    st_entry.insert(0, value[5])
    zc_entry.insert(0, value[6])


def update_record():
    selected = my_tree.focus()
    my_tree.item(selected, text='', values=(fn_entry.get(), ln_entry.get(), id_entry.get(), add_entry.get(),
                                            ct_entry.get(), st_entry.get(), zc_entry.get()))

    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('''UPDATE customers SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid''',
              {
                  'first': fn_entry.get(),
                  'last': ln_entry.get(),
                  'address': add_entry.get(),
                  'city': ct_entry.get(),
                  'state': st_entry.get(),
                  'zipcode': zc_entry.get(),
                  'oid': id_entry.get()
              }
              )
    conn.commit()
    conn.close()

    clear_entry()


def add_record():
    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('INSERT INTO customers VALUES (:first, :last, :id, :address, :city, :state, :zipcode)',
              {
                  'first': fn_entry.get(),
                  'last': ln_entry.get(),
                  'id': id_entry.get(),
                  'address': add_entry.get(),
                  'city': ct_entry.get(),
                  'state': st_entry.get(),
                  'zipcode': zc_entry.get(),
              })

    conn.commit()
    conn.close()

    clear_entry()

    my_tree.delete(*my_tree.get_children())
    query_database()


def create_table_again():
    conn = sqlite3.connect('tree_crm.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE if not exists customers (
           first_name text,
           last_name text,
           id integer,
           address text,
           city text,
           state text,
           zipcode text)
            ''')
    """data = [
        ['cuong', 'bui', '1', 'me linh', 'ha noi', 'single', '2020602992'],
        ['duc', 'ngo', '2', 'binh phu', 'hung yen', 'dating', '2020603596'],
        ['dien', 'dinh', '3', 'cam pha', 'quang ninh', 'vague', '2020607182'],
        ['dat', 'pham', '4', 'co le', 'nam dinh', 'vague', '2020530912'],
        ['dat', 'nguyen', '5', 'lien mac', 'ha noi', 'vague', '2020212902'],
    ]"""
    """for i in data:
        c.execute('INSERT INTO customers VALUES (:first_name, :last_name, :id, :address, :city, :state, :zipcode)',
                  {
                      'first_name': i[0],
                      'last_name': i[1],
                      'id': i[2],
                      'address': i[3],
                      'city': i[4],
                      'state': i[5],
                      'zipcode': i[6]
                  })"""
    conn.commit()
    conn.close()


btn_frame = tk.LabelFrame(root, text='commands')
btn_frame.pack(fill=tk.X, expand=True, padx=20)

update_btn = tk.Button(btn_frame, text='update record', command=update_record)
update_btn.grid(row=0, column=0, padx=10, pady=10)

add_btn = tk.Button(btn_frame, text='add record', command=add_record)
add_btn.grid(row=0, column=1, padx=10, pady=10)

remove_all_btn = tk.Button(btn_frame, text='remove all record', command=remove_all)
remove_all_btn.grid(row=0, column=2, padx=10, pady=10)

remove_one_btn = tk.Button(btn_frame, text='remove one selected', command=remove_one)
remove_one_btn.grid(row=0, column=3, padx=10, pady=10)

remove_many_btn = tk.Button(btn_frame, text='remove many selected', command=remove_many)
remove_many_btn.grid(row=0, column=4, padx=10, pady=10)

up_btn = tk.Button(btn_frame, text='move up', command=move_up)
up_btn.grid(row=0, column=5, padx=10, pady=10)

down_btn = tk.Button(btn_frame, text='move down', command=move_down)
down_btn.grid(row=0, column=6, padx=10, pady=10)

select_btn = tk.Button(btn_frame, text='clear entry', command=clear_entry)
select_btn.grid(row=0, column=7, padx=10, pady=10)

my_tree.bind('<ButtonRelease-1>', select_record)

query_database()
root.mainloop()