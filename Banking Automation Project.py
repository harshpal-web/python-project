from tkinter import *
from tkinter import messagebox
import time
import sqlite3

def create_connection():
    """Create a database connection."""
    try:
        conobj = sqlite3.connect(database='sqlite')
        return conobj
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error creating database connection: {e}")
        return None

def create_table():
    """Create the accounts table if it doesn't exist."""
    conobj = create_connection()
    if conobj:
        try:
            curobj = conobj.cursor()
            curobj.execute('CREATE TABLE IF NOT EXISTS acn(acn_acno INTEGER PRIMARY KEY AUTOINCREMENT, acn_name TEXT, acn_pass TEXT, acn_email TEXT, acn_mob TEXT, acn_bal FLOAT, acn_opendate TEXT)')
            conobj.commit()
            print('Table created')
        except sqlite3.Error as e:
            print(f'Error creating table: {e}')
        finally:
            conobj.close()

create_table()

win = Tk()
win.configure(bg='powder blue')
win.state('zoomed')
win.resizable(width=False, height=False)

lbl_title = Label(win, text='Banking Automation', font=('', 25, 'bold', 'underline'), bg='powder blue')
lbl_title.pack()

date = time.strftime('%d-%m-%Y')
lbl_date = Label(win, text=date, font=('', 20, 'bold'), bg='powder blue')
lbl_date.place(relx=.89, rely=.08)

def main_screen():
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.13, relwidth=1, relheight=.87)

    def newuser():
        frm.destroy()
        newuser_screen()

    def forgot():
        frm.destroy()
        forgot_screen()

    def login():
        global acn
        acn = e_acn.get()
        pwd = e_pass.get()
        if len(acn) == 0 or len(pwd) == 0:
            messagebox.showwarning('Validation', 'Empty fields are not allowed')
        else:
            conobj = create_connection()
            if conobj:
                try:
                    curobj = conobj.cursor()
                    curobj.execute('SELECT * FROM acn WHERE acn_acno=? AND acn_pass=?', (acn, pwd))
                    tup = curobj.fetchone()
                finally:
                    conobj.close()
                if tup is None:
                    messagebox.showerror('Login', 'Invalid account number/password')
                else:
                    frm.destroy()
                    welcome_screen()

    def reset():
        e_acn.delete(0, 'end')
        e_pass.delete(0, 'end')
        e_acn.focus()

    lbl_acn = Label(frm, text='ACN', font=('', 20, 'bold'), bg='pink')
    lbl_acn.place(relx=.35, rely=.1)

    e_acn = Entry(frm, font=('', 15), bd=5)
    e_acn.place(relx=.45, rely=.1)

    lbl_pass = Label(frm, text='Pass', font=('', 20, 'bold'), bg='pink')
    lbl_pass.place(relx=.35, rely=.2)

    e_pass = Entry(frm, font=('', 15), bd=5)
    e_pass.place(relx=.45, rely=.2)

    btn_login = Button(frm, command=login, text='Login', font=('', 15, 'bold'), bd=5)
    btn_login.place(relx=.478, rely=.3)

    btn_reset = Button(frm, command=reset, text='Reset', font=('', 15, 'bold'), bd=5)
    btn_reset.place(relx=.55, rely=.3)

    btn_newuser = Button(frm, command=newuser, text='New Users', font=('', 15, 'bold'), bd=5)
    btn_newuser.place(relx=.41, rely=.45)

    btn_frgtpwd = Button(frm, command=forgot, text='Forgot Password', font=('', 15, 'bold'), bd=5)
    btn_frgtpwd.place(relx=.51, rely=.45)

def newuser_screen():
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.13, relwidth=1, relheight=.87)

    def newacn():
        name = e_name.get()
        pwd = e_pass.get()
        email = e_email.get()
        mob = e_mob.get()
        bal = 0
        date = time.strftime("%d-%m-%Y")

        # Basic validation for email and mobile number
        if not validate_email(email):
            messagebox.showwarning('Validation', 'Invalid email format')
            return
        if not validate_mobile(mob):
            messagebox.showwarning('Validation', 'Invalid mobile number format')
            return

        conobj = create_connection()
        if conobj:
            try:
                curobj = conobj.cursor()
                curobj.execute('INSERT INTO acn (acn_name, acn_pass, acn_email, acn_mob, acn_bal, acn_opendate) VALUES (?, ?, ?, ?, ?, ?)', (name, pwd, email, mob, bal, date))
                conobj.commit()
                curobj.execute('SELECT MAX(acn_acno) FROM acn')
                tup = curobj.fetchone()
                messagebox.showinfo('New Account', f'Account created, ACN: {tup[0]}')
            finally:
                conobj.close()

    def back():
        frm.destroy()
        main_screen()

    btn_back = Button(frm, command=back, text='Back', font=('', 15, 'bold'), bd=5)
    btn_back.place(relx=0, rely=0)

    lbl_name = Label(frm, text='Name', font=('', 20, 'bold'), bg='pink')
    lbl_name.place(relx=.35, rely=.1)

    e_name = Entry(frm, font=('', 15), bd=5)
    e_name.place(relx=.45, rely=.1)

    lbl_pass = Label(frm, text='Pass', font=('', 20, 'bold'), bg='pink')
    lbl_pass.place(relx=.35, rely=.2)

    e_pass = Entry(frm, font=('', 15), bd=5)
    e_pass.place(relx=.45, rely=.2)

    lbl_email = Label(frm, text='E-mail', font=('', 20, 'bold'), bg='pink')
    lbl_email.place(relx=.35, rely=.3)

    e_email = Entry(frm, font=('', 15), bd=5)
    e_email.place(relx=.45, rely=.3)

    lbl_mob = Label(frm, text='Mob', font=('', 20, 'bold'), bg='pink')
    lbl_mob.place(relx=.35, rely=.4)

    e_mob = Entry(frm, font=('', 15), bd=5)
    e_mob.place(relx=.45, rely=.4)

    btn_submit = Button(frm, command=newacn, text='Submit', font=('', 15, 'bold'), bd=5)
    btn_submit.place(relx=.5, rely=.6)

def forgot_screen():
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.13, relwidth=1, relheight=.87)

    def back():
        frm.destroy()
        main_screen()

    def forgot():
        email = e_email.get()
        mob = e_mob.get()
        acn = e_acn.get()

        conobj = create_connection()
        if conobj:
            try:
                curobj = conobj.cursor()
                curobj.execute('SELECT acn_pass FROM acn WHERE acn_acno=? AND acn_email=? AND acn_mob=?', (acn, email, mob))
                tup = curobj.fetchone()
                if tup is None:
                    messagebox.showerror('Error', 'Account not found')
                else:
                    messagebox.showinfo('Password', f'Pass: {tup[0]}')
            finally:
                conobj.close()

    btn_back = Button(frm, command=back, text='Back', font=('', 15, 'bold'), bd=5)
    btn_back.place(relx=0, rely=0)

    lbl_email = Label(frm, text='E-mail', font=('', 20, 'bold'), bg='pink')
    lbl_email.place(relx=.35, rely=.1)

    e_email = Entry(frm, font=('', 15), bd=5)
    e_email.place(relx=.45, rely=.1)

    lbl_mob = Label(frm, text='Mob', font=('', 20, 'bold'), bg='pink')
    lbl_mob.place(relx=.35, rely=.2)

    e_mob = Entry(frm, font=('', 15), bd=5)
    e_mob.place(relx=.45, rely=.2)

    lbl_acn = Label(frm, text='ACN', font=('', 20, 'bold'), bg='pink')
    lbl_acn.place(relx=.35, rely=.3)

    e_acn = Entry(frm, font=('', 15), bd=5)
    e_acn.place(relx=.45, rely=.3)

    btn_submit = Button(frm, command=forgot, text='Submit', font=('', 15, 'bold'), bd=5)
    btn_submit.place(relx=.5, rely=.5)

def welcome_screen():
    frm = Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0, rely=.13, relwidth=1, relheight=.87)

    conobj = create_connection()
    if conobj:
        try:
            curobj = conobj.cursor()
            curobj.execute('SELECT * FROM acn WHERE acn_acno=?', (acn,))
            tup = curobj.fetchone()
        finally:
            conobj.close()

    def logout():
        frm.destroy()
        main_screen()

    def details():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2, rely=.1, relwidth=.6, relheight=.7)

        conobj = create_connection()
        if conobj:
            try:
                curobj = conobj.cursor()
                curobj.execute('SELECT * FROM acn WHERE acn_acno=?', (acn,))
                tup = curobj.fetchone()
            finally:
                conobj.close()

        lbl_acn = Label(ifrm, text=f'Account NO= {tup[0]}', font=('', 20, 'bold'), bg='white')
        lbl_acn.place(relx=.2, rely=.15)

        lbl_bal = Label(ifrm, text=f'Your ACN Bal= {tup[5]}', font=('', 20, 'bold'), bg='white')
        lbl_bal.place(relx=.2, rely=.25)

        lbl_date = Label(ifrm, text=f'Account open date= {tup[6]}', font=('', 20, 'bold'), bg='white')
        lbl_date.place(relx=.2, rely=.35)

        lbl_screen = Label(ifrm, text='This is details screen', font=('', 20, 'bold'), bg='white')
        lbl_screen.pack()

    def deposite():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2, rely=.1, relwidth=.6, relheight=.7)

        def depacn():
            conobj = create_connection()
            if conobj:
                try:
                    curobj = conobj.cursor()
                    amnt = float(e_amnt.get())
                    curobj.execute('UPDATE acn SET acn_bal=acn_bal+? WHERE acn_acno=?', (amnt, acn))
                    conobj.commit()
                    messagebox.showinfo('Deposit', f'{amnt} deposited')
                finally:
                    conobj.close()

        lbl_screen = Label(ifrm, text='This is deposit screen', font=('', 20, 'bold'), bg='white')
        lbl_screen.pack()

        lbl_amnt = Label(ifrm, text='Amount', font=('', 20, 'bold'), bg='white')
        lbl_amnt.place(relx=.3, rely=.15)

        e_amnt = Entry(ifrm, font=('', 15), bd=5)
        e_amnt.place(relx=.45, rely=.15)

        btn_submit = Button(ifrm, command=depacn, text='Submit', font=('', 15, 'bold'), bd=5)
        btn_submit.place(relx=.5, rely=.3)

    def withdraw():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2, rely=.1, relwidth=.6, relheight=.7)

        def withdrawacn():
            conobj = create_connection()
            if conobj:
                try:
                    curobj = conobj.cursor()
                    amnt = float(e_amnt.get())
                    curobj.execute('UPDATE acn SET acn_bal=acn_bal-? WHERE acn_acno=?', (amnt, acn))
                    conobj.commit()
                    messagebox.showinfo('Withdraw', f'{amnt} withdrawn')
                finally:
                    conobj.close()

        lbl_screen = Label(ifrm, text='This is withdraw screen', font=('', 20, 'bold'), bg='white')
        lbl_screen.pack()

        lbl_amnt = Label(ifrm, text='Amount', font=('', 20, 'bold'), bg='white')
        lbl_amnt.place(relx=.3, rely=.15)

        e_amnt = Entry(ifrm, font=('', 15), bd=5)
        e_amnt.place(relx=.45, rely=.15)

        btn_submit = Button(ifrm, command=withdrawacn, text='Submit', font=('', 15, 'bold'), bd=5)
        btn_submit.place(relx=.5, rely=.3)

    def update():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2, rely=.1, relwidth=.6, relheight=.7)

        def updateacn():
            name = e_name.get()
            pwd = e_pass.get()
            email = e_email.get()
            mob = e_mob.get()

            conobj = create_connection()
            if conobj:
                try:
                    curobj = conobj.cursor()
                    curobj.execute('UPDATE acn SET acn_name=?, acn_pass=?, acn_email=?, acn_mob=? WHERE acn_acno=?', (name, pwd, email, mob, acn))
                    conobj.commit()
                    messagebox.showinfo('Update', 'Update Successfully')
                    frm.destroy()
                    welcome_screen()
                finally:
                    conobj.close()

        lbl_name = Label(ifrm, text='Name', font=('', 20, 'bold'), bg='white')
        lbl_name.place(relx=.15, rely=.15)

        e_name = Entry(ifrm, font=('', 15), bd=5)
        e_name.place(relx=.15, rely=.23)

        lbl_pass = Label(ifrm, text='Pass', font=('', 20, 'bold'), bg='white')
        lbl_pass.place(relx=.55, rely=.15)

        e_pass = Entry(ifrm, font=('', 15), bd=5)
        e_pass.place(relx=.55, rely=.23)

        lbl_email = Label(ifrm, text='E-mail', font=('', 20, 'bold'), bg='white')
        lbl_email.place(relx=.15, rely=.43)

        e_email = Entry(ifrm, font=('', 15), bd=5)
        e_email.place(relx=.15, rely=.51)

        lbl_mob = Label(ifrm, text='Mob', font=('', 20, 'bold'), bg='white')
        lbl_mob.place(relx=.55, rely=.43)

        e_mob = Entry(ifrm, font=('', 15), bd=5)
        e_mob.place(relx=.55, rely=.51)

        btn_update = Button(ifrm, command=updateacn, text='Update', font=('', 15, 'bold'), bd=5)
        btn_update.place(relx=.43, rely=.7)

        lbl_screen = Label(ifrm, text='This is update screen', font=('', 20, 'bold'), bg='white')
        lbl_screen.pack()

        conobj = create_connection()
        if conobj:
            try:
                curobj = conobj.cursor()
                curobj.execute('SELECT * FROM acn WHERE acn_acno=?', (acn,))
                tup = curobj.fetchone()
            finally:
                conobj.close()

        e_name.insert(0, tup[1])
        e_pass.insert(0, tup[2])
        e_email.insert(0, tup[3])
        e_mob.insert(0, tup[4])
        e_name.focus()

    def admin():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2, rely=.1, relwidth=.6, relheight=.7)

        def dltacn():
            acno = e_acno.get()
            pwd = e_pass.get()

            conobj = create_connection()
            if conobj:
                try:
                    curobj = conobj.cursor()
                    curobj.execute('DELETE FROM acn WHERE acn_acno=? AND acn_pass=?', (acno, pwd))
                    conobj.commit()
                    messagebox.showinfo('Delete', 'Delete Successfully')
                    frm.destroy()
                    main_screen()
                finally:
                    conobj.close()

        lbl_screen = Label(ifrm, text='This is Admin screen', font=('', 20, 'bold'), bg='white')
        lbl_screen.pack()

        btn_dlt = Button(ifrm, command=dltacn, text='Delete', font=('', 15, 'bold'), bd=5)
        btn_dlt.place(relx=.43, rely=.5)

        lbl_acno = Label(ifrm, text='Account No', font=('', 20, 'bold'), bg='white')
        lbl_acno.place(relx=.15, rely=.15)

        e_acno = Entry(ifrm, font=('', 15), bd=5)
        e_acno.place(relx=.15, rely=.23)

        lbl_pass = Label(ifrm, text='Pass', font=('', 20, 'bold'), bg='white')
        lbl_pass.place(relx=.55, rely=.15)

        e_pass = Entry(ifrm, font=('', 15), bd=5)
        e_pass.place(relx=.55, rely=.23)

        conobj = create_connection()
        if conobj:
            try:
                curobj = conobj.cursor()
                curobj.execute('SELECT * FROM acn WHERE acn_acno=?', (acn,))
                tup = curobj.fetchone()
            finally:
                conobj.close()

        e_acno.delete(0, tup[0])
        e_pass.delete(0, tup[2])

    btn_logout = Button(frm, command=logout, text='Logout', font=('', 15, 'bold'), bd=5)
    btn_logout.place(relx=.94, rely=0)

    lbl_wlcm = Label(frm, text=f'Welcome, {tup[1]} ', font=('', 20, 'bold'), bg='pink')
    lbl_wlcm.place(relx=0, rely=0)

    btn_details = Button(frm, command=details, text='Check Details', width=12, font=('', 15, 'bold'), bd=5)
    btn_details.place(relx=0, rely=.2)

    btn_deposite = Button(frm, command=deposite, text='Deposit Amount', width=12, font=('', 15, 'bold'), bd=5)
    btn_deposite.place(relx=0, rely=.3)

    btn_withdraw = Button(frm, command=withdraw, text='Withdraw Amount', width=12, font=('', 15, 'bold'), bd=5)
    btn_withdraw.place(relx=0, rely=.4)

    btn_update = Button(frm, command=update, text='Update Details', width=12, font=('', 15, 'bold'), bd=5)
    btn_update.place(relx=0, rely=.5)

    btn_admin = Button(frm, command=admin, text='Admin Account', width=12, font=('', 15, 'bold'), bd=5)
    btn_admin.place(relx=0, rely=.6)

def validate_email(email):
    """Basic email validation."""
    return '@' in email and '.' in email

def validate_mobile(mob):
    """Basic mobile number validation."""
    return mob.isdigit() and len(mob) == 10

main_screen()
win.mainloop()
