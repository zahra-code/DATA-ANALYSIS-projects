"""This MyAuthManager Project is made with mysql and tkinter in python.This user interactive login and signup system has properties to update,delete,log out and viewing profile."""
from tkinter import *
from tkinter import messagebox
import re
import mysql.connector
from config import HOST,DB_USERNAME,DB_PASSWORD

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("410x200")
        self.root.minsize(400, 200)
        self.root.maxsize(400, 200)
        self.root.title("WELCOME!")
        self.main_interface()
        self.database_connection()
    def database_connection(self):
        '''Function for connection with the database in mysql'''
        try:
            self.connection=mysql.connector.connect(
                host=HOST,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database="loginDatabase"
            )
            self.cursor=self.connection.cursor()
        except Exception as e:
            print("Failed to create connection",e)

    def save_accounts(self,username,email,password):
        '''Function for saving accounts creation information in the database'''
        try:
            self.cursor.execute(
                f"INSERT into usernames_information(username,email,password)VALUES(%s,%s,%s)",(username,email,password)
            )
            self.connection.commit()
        except Exception as e:
            self.alert_box("Signup saving ERROR",f"ERROR:{e}")

    def check_credentials(self, username, password):
        '''function for checking the credentials using mysql query'''
        self.cursor.execute("SELECT * FROM usernames_information WHERE username = %s AND password = %s", (username, password))
        return self.cursor.fetchone()
    def save_login_info(self,username):
        '''function for storing the login information in the database'''
        try:
            self.cursor.execute(f"INSERT INTO login_information(username) values (%s)",(username,))
            self.connection.commit()
        except Exception as e:
            self.alert_box("login saving ERROR",f"ERROR:{e}")

    def main_interface(self):
        '''For creating main interface of the system'''
        self.root.configure(bg='#FFC0CB')
        Label(self.root, text="Welcome!", fg="purple", font=("ALGERIAN", 18, 'bold'), bg='#FFC0CB').grid(row=0, column=1, pady=(10, 10))
        Label(self.root, text="      Do you want to:", bg='#FFC0CB', font=("Arial", 10, 'italic', 'bold')).grid(row=1)
        login_button = Button(self.root, text="Login", command=self.login, width=10, bg='#007BFF', fg='white', font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        login_button.grid(row=3, column=1, pady=20)
        login_button.config(background='#800080')

        signup_button = Button(self.root, text="Signup", command=self.signup, width=10, bg='#28a745', fg='white', font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        signup_button.grid(row=5, column=1, pady=10)
        signup_button.config(background='#FF69B4')


    def clear_placeholder(self, event, entry):
        placeholder_texts = ["Enter Username", "Enter Password","New Password", "Confirm Password", "Enter Email"]
        if entry.get() in placeholder_texts:
            entry.delete(0, END)
            if entry.cget('show') == '*':
                entry.config(show="*")

    def add_placeholder(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder in ["Enter Password","New Password", "Confirm Password"]:
                entry.config(show="")
        else:
            if placeholder in ["Enter Password","New Password", "Confirm Password"]:
                entry.config(show="*")

    def alert_box(self, title, msg):
        '''message box for showing alerts and successes.'''
        messagebox.showinfo(title, message=msg)

    def getvalue_signup(self):
        '''Verifying the user's signup data'''
        s_user = self.user_name.get()
        s_email = self.email.get()
        s_pass = self.spassword.get()
        s_confirm = self.confirm_password.get()

        if s_user == "" or s_email == "" or s_pass == "" or s_confirm == "":
            self.alert_box("Signup Error", "All fields should be filled properly!")
        elif not re.findall(r"^[a-zA-Z0-9._%-]{2,}[@][a-zA-Z0-9-]*[.][a-zA-Z]{2,3}$", s_email):
            self.alert_box("Signup Error", "Invalid Email!")
        elif len(s_pass)<8:
            self.alert_box("Signup Error", "Password should contain 8 characters and atleast 1 special charcter(@,#,$,%,^,&,*)!")
        elif re.findall("[a-zA-Z0-9]+[@#$%^&*]{1}]",s_pass):
            self.alert_box("Signup Error", "Password should contain 8 characters and atleast 1 special charcter(@,#,$,%,^,&,*)!")
        elif s_pass != s_confirm:
            self.alert_box("Signup Error", "Password does not match!")
        else:
            self.save_accounts(s_user,s_email,s_pass)
            self.signup_root.destroy()
            self.alert_box("Signup Success", f"Account successfully created for username '{s_user}'")

    def signup(self):
        '''creating signup page'''
        try:
            self.login_root.destroy()
        except AttributeError:
            pass
        self.signup_root = Toplevel(self.root)
        self.signup_root.geometry("400x500")
        self.signup_root.minsize(400, 500)
        self.signup_root.maxsize(400, 500)
        self.signup_root.title("Signup")
        self.signup_root.configure(bg='#FFC0CB')

        Label(self.signup_root, text="Signup", bg='#FFC0CB', fg="purple", font=("Algerian", 20, "bold")).grid(row=0, column=0, padx=20, pady=10, sticky=E)
        Label(self.signup_root, text="Create your account:", bg='#FFC0CB', font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky=E)

        Label(self.signup_root, text="Username", bg='#FFC0CB', font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10, sticky=E)
        Label(self.signup_root, text="Email", bg='#FFC0CB', font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10, sticky=E)
        Label(self.signup_root, text="Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=4, column=0, padx=20, pady=10, sticky=E)
        Label(self.signup_root, text="Confirm Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=5, column=0, padx=20, pady=10, sticky=E)

        self.user_name = StringVar()
        self.email = StringVar()
        self.spassword = StringVar()
        self.confirm_password = StringVar()

        name_entry = Entry(self.signup_root, textvariable=self.user_name, font=("Arial", 12))
        name_entry.grid(row=2, column=1, padx=20, pady=10)
        name_entry.insert(0, "Enter Username")
        name_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, name_entry))
        name_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, name_entry, "Enter Username"))

        email_entry = Entry(self.signup_root, textvariable=self.email, font=("Arial", 12))
        email_entry.grid(row=3, column=1, padx=20, pady=10)
        email_entry.insert(0, "Enter Email")
        email_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, email_entry))
        email_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, email_entry, "Enter Email"))

        password_entry = Entry(self.signup_root, textvariable=self.spassword, show="*", font=("Arial", 12))
        password_entry.grid(row=4, column=1, padx=20, pady=10)
        password_entry.insert(0, "Enter Password")
        password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, password_entry))
        password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, password_entry, "Enter Password"))

        confirmpass_entry = Entry(self.signup_root, textvariable=self.confirm_password, show="*", font=("Arial", 12))
        confirmpass_entry.grid(row=5, column=1, padx=20, pady=10)
        confirmpass_entry.insert(0, "Confirm Password")
        confirmpass_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, confirmpass_entry))
        confirmpass_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, confirmpass_entry, "Confirm Password"))

        signup_button = Button(self.signup_root, text="Create", command=self.getvalue_signup, fg="white", pady=5, padx=10, font=("Arial 12 bold"))
        signup_button.grid(row=7, column=1, pady=(10, 10))
        signup_button.config(background='#FF69B4')

        Label(self.signup_root, text="Password should be 8 character long\n(Atleast 1 special character)", bg='#FFC0CB', font=("Arial", 7)).grid(row=6, column=1)


    def getvalue_login(self):
        '''getting and Verifying the login data of user.'''
        global user
        global passw
        user = self.username.get()
        passw = self.password.get()
        if user == "" or passw == "":
            self.alert_box("Login Error", "Username or password cannot be empty")
        elif len(passw) < 8:
            self.alert_box("Login Error", "Incorrect Password")
        elif re.findall("[a-zA-Z0-9]+[@#$%^&*]{1}]", passw):
            self.alert_box("Login Error","Incorrect Password")
        elif self.check_credentials(user, passw):
            self.save_login_info(user)
            self.alert_box("Login Success", f"Successfully logged in as {user}.")
            self.login_root.destroy()
            self.open_main_page()
        else:
            self.alert_box("Login Error", "Login credentials are not correct\nLogin Failed.")

    def login(self):
        '''Creating the login page'''
        self.login_root = Toplevel(self.root)
        self.login_root.geometry("500x300")
        self.login_root.minsize(500, 300)
        self.login_root.maxsize(500, 300)
        self.login_root.title("Login")
        self.login_root.configure(bg='#FFC0CB')

        Label(self.login_root, text="     Username", bg='#FFC0CB', font=("Arial", 13, "bold")).grid(row=0, column=0, padx=20, pady=10, sticky=E)
        Label(self.login_root, text="     Password", bg='#FFC0CB', font=("Arial", 13, "bold")).grid(row=1, column=0, padx=20, pady=10, sticky=E)

        self.username = StringVar()
        self.password = StringVar()

        username_entry = Entry(self.login_root, textvariable=self.username, font=("Arial", 12))
        username_entry.grid(row=0, column=1, padx=20, pady=10)
        username_entry.insert(0, "Enter Username")
        username_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, username_entry))
        username_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, username_entry, "Enter Username"))

        password_entry=Entry(self.login_root,textvariable=self.password ,show="*", font=("Arial", 12))
        password_entry.grid(row=1,column=1,padx=20,pady=10)
        password_entry.insert(0, "Enter Password")
        password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, password_entry))
        password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, password_entry, "Enter Password"))

        login_button=Button(self.login_root,text="Login",command=self.getvalue_login, width=10, bg='#007BFF', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        login_button.grid(row=3,column=1, pady=20)
        login_button.config(background='#800080')
        Label(self.login_root,text="Don't have an account? Create one", bg='#FFC0CB', font=("Arial", 10)).grid(row=4, column=0, columnspan=2, pady=(10, 0))

        signup_button = Button(self.login_root, text="Signup",command=self.signup, width=10, bg='#28a745', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        signup_button.grid(row=5, column=1, pady=10)
        signup_button.config(background='#FF69B4')
    def logout(self):
        '''loging out from home page'''
        self.page_root.destroy()
    def delete_account(self):
        '''Deleting account main page'''
        self.delete_root = Toplevel(self.root)
        self.delete_root.geometry("410x200")
        self.delete_root.minsize(400, 200)
        self.delete_root.maxsize(400, 200)
        self.delete_root.title("Account Settings-Delete Account")
        self.delete_root.configure(bg='#FFC0CB')

        Label(self.delete_root, text="Delete Account", fg="purple", font=("ALGERIAN", 18, 'bold'), bg='#FFC0CB').grid(row=1,column=0,pady=(10, 10))
        Label(self.delete_root, text="   Are you sure?", bg='#FFC0CB', font=("Arial", 10, 'italic', 'bold')).grid(row=2)
        no_button = Button(self.delete_root, text="No", command=self.back_delete_back, width=10, bg='#007BFF', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        no_button.grid(row=3, column=0, padx=20,pady=10)
        no_button.config(background='#800080')

        yes_button = Button(self.delete_root, text="Yes", command=self.yes_delete, width=10, bg='#28a745', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        yes_button.grid(row=3, column=1,padx=10, pady=10)
        yes_button.config(background='#FF69B4')
    def back_delete_back(self):
        '''Backing the page if usr says no to delete the account'''
        self.delete_root.destroy()
    def yes_delete(self):
        '''moving forward if user says yes to delete account.'''
        self.yes_delete_root = Toplevel(self.root)
        self.yes_delete_root.geometry("500x300")
        self.yes_delete_root.minsize(500, 300)
        self.yes_delete_root.maxsize(500, 300)
        self.yes_delete_root.title("Verify Account")
        self.yes_delete_root.configure(bg='#FFC0CB')

        Label(self.yes_delete_root, text="     Username", bg='#FFC0CB', font=("Arial", 13, "bold")).grid(row=0, column=0,padx=20, pady=10,sticky=E)
        Label(self.yes_delete_root, text="     Password", bg='#FFC0CB', font=("Arial", 13, "bold")).grid(row=1, column=0,padx=20, pady=10,sticky=E)
        self.dusername = StringVar()
        self.dpassword = StringVar()

        username_entry = Entry(self.yes_delete_root, textvariable=self.dusername, font=("Arial", 12))
        username_entry.grid(row=0, column=1, padx=20, pady=10)
        username_entry.insert(0, f"{user}")

        password_entry = Entry(self.yes_delete_root, textvariable=self.dpassword, show="*", font=("Arial", 12))
        password_entry.grid(row=1, column=1, padx=20, pady=10)
        password_entry.insert(0, "Enter Password")
        password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, password_entry))
        password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, password_entry, "Enter Password"))

        okay_button = Button(self.yes_delete_root, text="Confirm", command=self.delete_final, width=10, bg='#007BFF',fg='white', font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        okay_button.grid(row=3, column=1, pady=20)
        okay_button.config(background='#800080')
    def delete_final(self):
        '''checking the credentials and finally deleting the account.'''
        user = self.dusername.get()
        passw = self.dpassword.get()
        if user == "" or passw == "":
            self.alert_box("Verification failed", "Username or password cannot be empty")
        elif len(passw) < 8:
            self.alert_box("Verification failed", "Incorrect Password")
        elif re.findall("[a-zA-Z0-9]+[@#$%^&*]{1}]", passw):
            self.alert_box("Verification failed","Incorrect Password")
        elif self.check_credentials(user, passw):
            self.yes_delete_root.destroy()
            try:
                self.cursor.execute("DELETE FROM usernames_information where username=%s and password=%s", (user,passw))
                self.connection.commit()
                self.delete_root.destroy()
                self.page_root.destroy()
                self.alert_box("Account Deleted", f"Account successfully deleted with username '{user}'.")

            except Exception as e:
                self.alert_box("ERROR Account Deleting", f"ERROR:{e}")

        else:
            self.alert_box("Verification failed", "Login credentials are not correct\nLogin Failed.")
            self.yes_delete_root.destroy()

    def view_account_details(self):
        '''Function for showing account details to the user'''
        try:
            self.cursor.execute(
                "SELECT username, email, password FROM usernames_information WHERE username = %s and password = %s",
                (user, passw))
            result = self.cursor.fetchone()
            if result:
                acc_name, acc_email, acc_pass = result
        except Exception as e:
            self.alert_box("Error", f"Failed to fetch account details: {e}")
        self.view_root = Toplevel(self.root)
        self.view_root.geometry("400x500")
        self.view_root.minsize(400, 500)
        self.view_root.maxsize(400, 500)
        self.view_root.title("Account Setting-View Account")
        self.view_root.configure(bg='#FFC0CB')

        Label(self.view_root, text="Account", bg='#FFC0CB', fg="purple", font=("Algerian", 20, "bold")).grid(row=0, column=0,padx=20,pady=10,sticky=E)

        Label(self.view_root, text="Username", bg='#FFC0CB', font=("Arial", 12)).grid(row=2, column=0, padx=20,pady=10, sticky=E)
        Label(self.view_root, text="Email", bg='#FFC0CB', font=("Arial", 12)).grid(row=3, column=0, padx=20,pady=10, sticky=E)
        Label(self.view_root, text="Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=4, column=0, padx=20,pady=10, sticky=E)

        name_entry = Entry(self.view_root, font=("Arial", 12))
        name_entry.grid(row=2, column=1, padx=20, pady=10)
        name_entry.insert(0, f"{acc_name}")

        email_entry = Entry(self.view_root,font=("Arial", 12))
        email_entry.grid(row=3, column=1, padx=20, pady=10)
        email_entry.insert(0, f"{acc_email}")

        password_entry = Entry(self.view_root, show="*", font=("Arial", 12))
        password_entry.grid(row=4, column=1, padx=20, pady=10)
        password_entry.insert(0, f"{acc_pass}")

    def update_account(self):
        '''Creating main update account page'''
        try:
            name = self.new_name.get()
            email = self.new_email.get()
            password = passw
            self.cursor.execute(
                "SELECT username, email, password FROM usernames_information WHERE username = %s and password = %s",
                (user, passw))
            result = self.cursor.fetchone()
            if result:
                acc_name, acc_email, acc_pass = result
            # Check if the new username already exists for another user
            self.cursor.execute("SELECT COUNT(*) FROM usernames_information WHERE username = %s AND password != %s",
                                (name, password))
            username_exists = self.cursor.fetchone()[0]

            if username_exists:
                self.alert_box("Update Error", "ERROR: Username already exists")
            else:
                self.cursor.execute("UPDATE usernames_information SET username = %s WHERE password = %s and email = %s",
                                    (name,password,acc_email))
                self.connection.commit()
                self.cursor.execute("UPDATE usernames_information SET email = %s WHERE password = %s and username = %s",
                                    (email, password,name))
                self.connection.commit()
                self.alert_box("Update Success", "Account Updated Successfully")
                self.update_root.destroy()
                self.page_root.destroy()

        except Exception as e:
            self.alert_box("Update Error", f"ERROR: {e}")
    def final_change_pass(self):
        '''Verifying and finally changing the password'''
        oldp= self.oldpass.get()
        nnpass = self.newpass.get()
        ccpass=self.cconfirmpass.get()
        if oldp == "" or nnpass == "" or ccpass=="":
            self.alert_box("Update Error", "All fields must be completely filled")
        elif not self.check_credentials(user, passw):
            self.save_login_info(user)
            self.alert_box("Update Error", f"Your entered old password is incorrect.")
            self.update_root.destroy()
            self.open_main_page()
        elif len(nnpass) < 8:
            self.alert_box("Update Error", "Password should be 8 character long\n(Atleast 1 special character)")
        elif re.findall("[a-zA-Z0-9]+[@#$%^&*]{1}]", nnpass):
            self.alert_box("Update Error", "Password should be 8 character long\n(Atleast 1 special character)")
        elif nnpass!=ccpass:
            self.alert_box("Update Error", "Passwords doesn't match")
        else:
            self.cursor.execute(
                "SELECT username, email, password FROM usernames_information WHERE username = %s and password = %s",
                (user, passw))
            result = self.cursor.fetchone()
            if result:
                acc_name, acc_email, acc_pass = result
            self.cursor.execute("UPDATE usernames_information SET password = %s WHERE username = %s and email = %s",
                                (nnpass,acc_name, acc_email))
            self.connection.commit()
            self.alert_box("Update Success", f"Password successfully updated for '{acc_name}'")
            self.changepass_root.destroy()
            self.page_root.destroy()
    def change_password(self):
        '''Changing password page'''
        self.update_root.destroy()
        self.changepass_root = Toplevel(self.root)
        self.changepass_root.geometry("400x500")
        self.changepass_root.minsize(400, 500)
        self.changepass_root.maxsize(400, 500)
        self.changepass_root.title("Signup")
        self.changepass_root.configure(bg='#FFC0CB')

        Label(self.changepass_root, text="Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10,sticky=E)
        Label(self.changepass_root, text="New Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=4, column=0, padx=20,pady=10, sticky=E)
        Label(self.changepass_root, text="Confirm Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=5, column=0,padx=20, pady=10,sticky=E)

        self.oldpass = StringVar()
        self.newpass = StringVar()
        self.cconfirmpass = StringVar()


        pass_entry = Entry(self.changepass_root, textvariable=self.oldpass, font=("Arial", 12))
        pass_entry.grid(row=3, column=1, padx=20, pady=10)
        pass_entry.insert(0, "Enter Password")
        pass_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, pass_entry))
        pass_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, pass_entry, "Enter Password"))

        password_entry = Entry(self.changepass_root, textvariable=self.newpass, show="*", font=("Arial", 12))
        password_entry.grid(row=4, column=1, padx=20, pady=10)
        password_entry.insert(0, "New Password")
        password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, password_entry))
        password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, password_entry, "New Password"))

        confirmpass_entry = Entry(self.changepass_root, textvariable=self.cconfirmpass, show="*", font=("Arial", 12))
        confirmpass_entry.grid(row=5, column=1, padx=20, pady=10)
        confirmpass_entry.insert(0, "Confirm Password")
        confirmpass_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, confirmpass_entry))
        confirmpass_entry.bind("<FocusOut>",lambda event: self.add_placeholder(event, confirmpass_entry, "Confirm Password"))

        okay_button = Button(self.changepass_root, text="Corfirm",command=self.final_change_pass, fg="white", pady=5,padx=10, font=("Arial 12 bold"))
        okay_button.grid(row=7, column=1, pady=(10, 10))
        okay_button.config(background='#FF69B4')

        Label(self.changepass_root, text="Password should be 8 character long\n(Atleast 1 special character)", bg='#FFC0CB',
              font=("Arial", 7)).grid(row=6, column=1)
    def update_window(self):
        '''main update page'''
        try:
            self.cursor.execute(
                "SELECT username, email, password FROM usernames_information WHERE username = %s AND password = %s",
                (user, passw))
            result = self.cursor.fetchone()
            if result:
                acc_name, acc_email, acc_pass = result
        except Exception as e:
            self.alert_box("Error", f"Failed to fetch account details: {e}")
        self.update_root = Toplevel(self.root)
        self.update_root.geometry("400x500")
        self.update_root.minsize(400, 500)
        self.update_root.maxsize(400, 500)
        self.update_root.title("Account Settings-Update Account")
        self.update_root.configure(bg='#FFC0CB')

        Label(self.update_root, text="Account", bg='#FFC0CB', fg="purple", font=("Algerian", 20, "bold")).grid(row=0, column=0,padx=20,pady=10,sticky=E)

        Label(self.update_root, text="Username", bg='#FFC0CB', font=("Arial", 12)).grid(row=2, column=0, padx=20,pady=10, sticky=E)
        Label(self.update_root, text="Email", bg='#FFC0CB', font=("Arial", 12)).grid(row=3, column=0, padx=20,pady=10, sticky=E)
        Label(self.update_root, text="Password", bg='#FFC0CB', font=("Arial", 12)).grid(row=4, column=0, padx=20,pady=10, sticky=E)

        self.new_name=StringVar()
        self.new_email=StringVar()

        name_entry = Entry(self.update_root,textvariable=self.new_name,font=("Arial", 12))
        name_entry.grid(row=2, column=1, padx=20, pady=10)
        name_entry.insert(0, f"{acc_name}")
        name_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, name_entry))
        name_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, name_entry, "Enter Username"))

        email_entry = Entry(self.update_root,textvariable=self.new_email,font=("Arial", 12))
        email_entry.grid(row=3, column=1, padx=20, pady=10)
        email_entry.insert(0, f"{acc_email}")
        email_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, email_entry))
        email_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, email_entry, "Enter Email"))

        password_entry = Entry(self.update_root, show="*", font=("Arial", 12))
        password_entry.grid(row=4, column=1, padx=20, pady=10)
        password_entry.insert(0, f"{acc_pass}")
        password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, password_entry))
        password_entry.bind("<FocusOut>",lambda event: self.add_placeholder(event, password_entry, "can't update here"))


        update_button = Button(self.update_root, text="update", command=self.update_account, width=10, bg='#007BFF',fg='white', font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        update_button.grid(row=5, column=1, pady=20)
        update_button.config(background='#800080')

        changepass_button = Button(self.update_root, text="Change Password",command=self.change_password, width=20, bg='#28a745', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        changepass_button.grid(row=7, column=1, pady=10)
        changepass_button.config(background='#FF69B4')


    def open_main_page(self):
        '''Home page'''
        self.page_root = Toplevel(self.root)
        self.page_root.geometry("900x500")
        self.page_root.minsize(500, 300)
        self.page_root.maxsize(900, 500)
        self.page_root.title("Home")
        self.page_root.configure(bg='#FFC0CB')

        f2 = Frame(self.page_root, bg="pink", borderwidth=3, relief=SUNKEN)
        f2.pack(side=RIGHT, fill="y")
        Label(f2, text="Home", fg="purple", font=("Algerian", 26, "bold"),padx=250).grid(column=1)

        f1=Frame(self.page_root,bg="pink",borderwidth=3,relief=SUNKEN)
        f1.pack(side=LEFT,fill="y")
        Label(f1,text="Account Settings",padx=70,font=("Arial",15,"bold")).grid()

        update_button = Button(f1, text="Update", command=self.update_window, width=10, bg='#007BFF',fg='white', font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        update_button.grid(row=3, column=0, pady=20)
        update_button.config(background='#800080')

        delete_button = Button(f1, text="Delete", command=self.delete_account, width=10, bg='#007BFF', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        delete_button.grid(row=4, column=0, pady=15)
        delete_button.config(background='#800080')

        view_button = Button(f1, text="View", command=self.view_account_details, width=10, bg='#007BFF', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        view_button.grid(row=5, column=0, pady=15)
        view_button.config(background='#800080')

        logout_button = Button(f1, text="Logout", command=self.logout, width=10, bg='#007BFF', fg='white',font=("Arial", 12, 'bold'), bd=2, relief=SOLID)
        logout_button.grid(row=6, column=0, pady=15)
        logout_button.config(background='#800080')



if __name__=="__main__":
    root=Tk()
    LoginApp(root)
    root.mainloop()