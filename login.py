from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'Mohan' and passwordEntry.get() == '1234':
        messagebox.showinfo('Success', 'Welcome')
        Window.destroy()
        import sms
    else:
        messagebox.showerror('Error', 'Please enter correct details')

Window = Tk()

Window.geometry('1280x854+0+0')
Window.title('Login System of Student Management System')

Window.resizable(False, False)

backgroundImage = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(Window, image=backgroundImage)
bgLabel.place(x=0, y=0)

loginFrame = Frame(Window, bg='white')
loginFrame.place(x=400, y=150)

logoImage = PhotoImage(file='logo.png')

logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue', show='*')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15, fg='white',
                     bg='cornflowerblue', activebackground='cornflowerblue', activeforeground='white',
                     cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)

Window.mainloop()
