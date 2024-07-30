from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox
import pymysql

# Global variables
mycursor = None
con = None

def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    row = content['values']
    if not row:
        messagebox.showerror('Error', 'Please select a student to delete')
        return
    id = row[0]
    try:
        query = "DELETE FROM student WHERE id=%s"
        mycursor.execute(query, (id,))
        con.commit()
        messagebox.showinfo('Success', 'Student deleted successfully')
        show_students()
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error while deleting student: {e}')

def search_student():
    def search_data():
        try:
            # Clear previous entries in the studentTable widget
            studentTable.delete(*studentTable.get_children())

            # Construct the SQL query to search for data
            query = "SELECT * FROM student WHERE id=%s OR name=%s OR mobile=%s OR address=%s OR gender=%s OR dob=%s OR mail=%s"
            
            # Execute the query with parameters from the GUI entries
            mycursor.execute(query, (
                idEntry.get(),
                nameEntry.get(),
                phoneEntry.get(),
                addressEntry.get(),
                genderEntry.get(),
                dobEntry.get(),
                emailEntry.get()
            ))

            # Fetch all the rows returned by the query
            fetched_data = mycursor.fetchall()
            
            # Insert fetched data into the studentTable widget
            for data in fetched_data:
                studentTable.insert('', END, values=data)
        
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error while searching data: {e}')

    search_window = Toplevel()
    search_window.title("Search Student")
    search_window.grab_set()
    search_window.resizable(False, False)

    labels = ['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = []
    for i, label in enumerate(labels):
        lbl = Label(search_window, text=label, font=('times new roman', 20, 'bold'))
        lbl.grid(row=i, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=i, column=1, pady=15, padx=10)
        entries.append(entry)

    idEntry, nameEntry, phoneEntry, emailEntry, addressEntry, genderEntry, dobEntry = entries

    search_student_button = ttk.Button(search_window, text='SEARCH STUDENT', command=search_data)
    search_student_button.grid(row=len(labels), columnspan=2, pady=15)

def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or phoneEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All fields are required', parent=add_window)
        else:
            currentdate = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            try:
                query = 'INSERT INTO student (id, name, mobile, mail, address, gender, dob, reg_date, reg_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                mycursor.execute(query, (
                    idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), currentdate, currenttime
                ))
                con.commit()
                result = messagebox.askyesno('Confirm', 'Student added successfully. Do you want to clean the form?', parent=add_window)
                if result:
                    for entry in [idEntry, nameEntry, phoneEntry, emailEntry, addressEntry, genderEntry, dobEntry]:
                        entry.delete(0, END)
                show_students()
            except pymysql.Error as e:
                messagebox.showerror('Error', f'Error while adding student: {e}', parent=add_window)

    add_window = Toplevel()
    add_window.grab_set()
    add_window.resizable(False, False)

    labels = ['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = []
    for i, label in enumerate(labels):
        lbl = Label(add_window, text=label, font=('times new roman', 20, 'bold'))
        lbl.grid(row=i, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=i, column=1, pady=15, padx=10)
        entries.append(entry)

    idEntry, nameEntry, phoneEntry, emailEntry, addressEntry, genderEntry, dobEntry = entries

    add_student_button = ttk.Button(add_window, text='ADD STUDENT', command=add_data)
    add_student_button.grid(row=len(labels), columnspan=2, pady=15)

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()

            try:
                query = 'CREATE DATABASE studentmanagementsystem'
                mycursor.execute(query)
                query = 'USE studentmanagementsystem'
                mycursor.execute(query)
                query = '''
                    CREATE TABLE student (
                        id INT NOT NULL PRIMARY KEY,
                        name VARCHAR(30),
                        mobile VARCHAR(10),
                        mail VARCHAR(50),
                        address VARCHAR(100),
                        gender VARCHAR(20),
                        dob VARCHAR(20),
                        reg_date VARCHAR(50),
                        reg_time VARCHAR(50)
                    )
                '''
                mycursor.execute(query)
            except pymysql.Error:
                query = 'USE studentmanagementsystem'
                mycursor.execute(query)
                
            messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
            connectWindow.destroy()
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}", parent=connectWindow)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'))
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'))
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'))
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)

def show_students():
    try:
        query = "SELECT * FROM student"
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error while fetching data: {e}")

def update_student():
    def update_data():
        try:
            query = "UPDATE student SET name=%s, mobile=%s, mail=%s, address=%s, gender=%s, dob=%s WHERE id=%s"
            mycursor.execute(query, (
                nameEntry.get(),
                phoneEntry.get(),
                emailEntry.get(),
                addressEntry.get(),
                genderEntry.get(),
                dobEntry.get(),
                id
            ))
            con.commit()
            messagebox.showinfo("Success", "Student data updated successfully.")
            show_students()
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error while updating data: {e}")

    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    row = content['values']
    if not row:
        messagebox.showerror("Error", "Please select a student to update")
        return
    id = row[0]

    update_window = Toplevel()
    update_window.title("Update Student")
    update_window.grab_set()
    update_window.resizable(False, False)

    labels = ['Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = []
    for i, label in enumerate(labels):
        lbl = Label(update_window, text=label, font=('times new roman', 20, 'bold'))
        lbl.grid(row=i, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=i, column=1, pady=15, padx=10)
        entries.append(entry)

    nameEntry, phoneEntry, emailEntry, addressEntry, genderEntry, dobEntry = entries

    def fill_entries():
        nameEntry.insert(0, row[1])
        phoneEntry.insert(0, row[2])
        emailEntry.insert(0, row[3])
        addressEntry.insert(0, row[4])
        genderEntry.insert(0, row[5])
        dobEntry.insert(0, row[6])

    fill_entries()

    update_button = ttk.Button(update_window, text="Update Student", command=update_data)
    update_button.grid(row=len(labels), columnspan=2, pady=15)

count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'  Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry("1174x680+50+20")
root.resizable(0, 0)
root.title('Student Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Student Management System'
sliderLabel = Label(root, text=s, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='connect database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED, command=add_student)
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED, command=search_student)
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED, command=update_student)
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_students)
showstudentButton.grid(row=5, column=0, pady=20)

exitstudentButton = ttk.Button(leftFrame, text='Exit', width=25, command=root.quit)
exitstudentButton.grid(row=6, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

ScrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
ScrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Time'), xscrollcommand=ScrollBarX.set, yscrollcommand=ScrollBarY.set)

ScrollBarX.config(command=studentTable.xview)
ScrollBarY.config(command=studentTable.yview)

ScrollBarX.pack(side=BOTTOM, fill=X)
ScrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile No', text='Mobile No')
studentTable.heading('Email', text='Email')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Time', text='Added Time')

studentTable.config(show='headings')

root.mainloop()
