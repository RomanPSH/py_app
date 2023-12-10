import tkinter as tk
import sqlite3
import hashlib

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'Користувач',
        is_blocked INTEGER DEFAULT 0,
        login_attempts INTEGER DEFAULT 0
    )
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        message_label.config(text='Користувач з таким ім\'ям вже існує', fg='red')
    elif password == confirm_password:
        hashed_password = hash_password(password)
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        message_label.config(text='Реєстрація пройшла успішно!', fg='green')
    else:
        message_label.config(text='Паролі не співпадають', fg='red')


def login_user():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        login_attempts = user[5]  # Index 5 corresponds to the login_attempts field

        if login_attempts >= 3:
            message_label.config(text='Перевищено максимальну кількість спроб входу', fg='red')
        else:
            attempts_left = 3 - login_attempts

            if user[2] == hashed_password:  # Index 2 corresponds to the password field
                cursor.execute('UPDATE users SET login_attempts = 0 WHERE username = ?', (username,))
                conn.commit()
                role = user[3]  # Index 3 corresponds to the role field
                if role:
                    message_label.config(text=f'Успішний вхід. Роль користувача: {role}', fg='green')
                else:
                    message_label.config(text='Роль користувача не знайдена', fg='red')
            else:
                cursor.execute('UPDATE users SET login_attempts = login_attempts + 1 WHERE username = ?', (username,))
                conn.commit()
                attempts_left -= 1
                message_label.config(text='Неправильний пароль', fg='red')

                if attempts_left == 0:
                    message_label.config(text='Перевищено максимальну кількість спроб входу', fg='red')
                else:
                    message_label.config(text=f'Кількість спроб, що залишилися: {attempts_left}', fg='black')
    else:
        message_label.config(text='Неправильний логін або пароль', fg='red')

def show_login_form():
    login_page_button.pack_forget()
    register_page_button.pack_forget()

    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    message_label.pack()
    login_button.pack()

    have_account_button.pack()

def show_register_form():
    login_page_button.pack_forget()
    register_page_button.pack_forget()

    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    confirm_password_label.pack()
    confirm_password_entry.pack()
    message_label.pack()
    register_button.pack()

    already_registered_button.pack()

def show_have_account():
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    confirm_password_label.pack_forget()
    confirm_password_entry.pack_forget()
    message_label.pack_forget()
    register_button.pack_forget()
    already_registered_button.pack_forget()

    show_login_form()

def show_not_registered():
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    message_label.pack_forget()
    login_button.pack_forget()
    have_account_button.pack_forget()

    show_register_form()

def reset_login_attempts_on_open():
    cursor.execute('UPDATE users SET login_attempts = 0')
    conn.commit()

root = tk.Tk()
root.title('Авторизація та реєстрація')

username_label = tk.Label(root, text='Ім\'я користувача:')
username_entry = tk.Entry(root)

password_label = tk.Label(root, text='Пароль:')
password_entry = tk.Entry(root, show='*')

confirm_password_label = tk.Label(root, text='Підтвердіть пароль:')
confirm_password_entry = tk.Entry(root, show='*')

message_label = tk.Label(root, text='')

register_button = tk.Button(root, text='Зареєструватися', command=register_user)
login_button = tk.Button(root, text='Увійти', command=login_user)

register_page_button = tk.Button(root, text='Зареєструватися', command=show_register_form)
login_page_button = tk.Button(root, text='Увійти', command=show_login_form)

already_registered_button = tk.Button(root, text='Я вже маю акаунт', command=show_have_account)
have_account_button = tk.Button(root, text='Не маю акаунта', command=show_not_registered)

login_page_button.pack()
register_page_button.pack()

reset_login_attempts_on_open()

root.mainloop()

conn.close()