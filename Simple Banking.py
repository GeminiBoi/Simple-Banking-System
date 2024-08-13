import sqlite3
from tkinter import *
from tkinter import ttk, Toplevel, messagebox, simpledialog
from tkinter.font import Font
import re

# Initialize database
conn = sqlite3.connect('banking_app.db')
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                second_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                balance REAL DEFAULT 0.0
            )''')

# Create transactions table
c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')

conn.commit()

# Tkinter root window setup
root = Tk()
root.geometry("1000x700")
root.title("Meridian Bank of Ghana")

# New color scheme
BACKGROUND_COLOR = "#1E1E2E"
FOREGROUND_COLOR = "#CDD6F4"
ACCENT_COLOR = "#89B4FA"
SECONDARY_COLOR = "#BAC2DE"
BUTTON_COLOR = "#313244"
ERROR_COLOR = "#F38BA8"

# Custom fonts
LARGE_FONT = Font(family="Roboto", size=28, weight="bold")
MEDIUM_FONT = Font(family="Roboto", size=16)
SMALL_FONT = Font(family="Roboto", size=12)

# Variables
email_var = StringVar()
password_var = StringVar()
first_name_var = StringVar()
second_name_var = StringVar()
create_email_var = StringVar()
create_password_var = StringVar()
confirm_password_var = StringVar()

class GradientFrame(Canvas):
    def __init__(self, parent, color1=BACKGROUND_COLOR, color2="#181825", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")

class RoundedButton(Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None, text=''):
        Canvas.__init__(self, parent, borderwidth=0,
                        relief="flat", highlightthickness=0, bg=bg)
        self.command = command

        if cornerradius > 0.5 * width:
            cornerradius = 0.5 * width
        if cornerradius > 0.5 * height:
            cornerradius = 0.5 * height

        self.create_polygon((0, height - cornerradius, 0, 0, height, 0, width, 0, width, height, 0, height),
                            fill=color, outline=color)
        self.create_polygon(
            (0, height, cornerradius, height - cornerradius, width - cornerradius, height - cornerradius,
             width, height), fill=color, outline=color)
        self.create_polygon((width - cornerradius, height - cornerradius, width - cornerradius, cornerradius,
                             width, cornerradius), fill=color, outline=color)
        self.create_polygon((0, height - cornerradius, cornerradius, height - cornerradius, cornerradius, cornerradius,
                             0, cornerradius), fill=color, outline=color)

        self.create_oval((0, 0, 2 * cornerradius, 2 * cornerradius), fill=color, outline=color)
        self.create_oval((width - 2 * cornerradius, 0, width, 2 * cornerradius), fill=color, outline=color)
        self.create_oval((0, height - 2 * cornerradius, 2 * cornerradius, height), fill=color, outline=color)
        self.create_oval((width - 2 * cornerradius, height - 2 * cornerradius, width, height), fill=color,
                         outline=color)

        self.create_text(width / 2, height / 2, text=text, fill=FOREGROUND_COLOR, font=MEDIUM_FONT)

        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()

def create_styled_label(parent, text, font=MEDIUM_FONT, fg=FOREGROUND_COLOR):
    return Label(parent, text=text, font=font, fg=fg, bg=BACKGROUND_COLOR)

def create_styled_entry(parent, textvariable, show=None):
    entry = Entry(parent, textvariable=textvariable, font=SMALL_FONT, bg=BUTTON_COLOR,
                  fg=FOREGROUND_COLOR, insertbackground=ACCENT_COLOR, width=30, show=show)
    entry.configure(relief=FLAT, bd=0, highlightthickness=1, highlightcolor=ACCENT_COLOR)
    return entry

def sign_in():
    sign_in_window = Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("400x500")
    sign_in_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(sign_in_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=40, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Sign In", LARGE_FONT, ACCENT_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 30))
    create_styled_label(frame, "Email").grid(row=1, column=0, sticky="w", pady=(10, 0))
    create_styled_entry(frame, email_var).grid(row=2, column=0, sticky="we", pady=(5, 10))
    create_styled_label(frame, "Password").grid(row=3, column=0, sticky="w", pady=(10, 0))
    create_styled_entry(frame, password_var, show='*').grid(row=4, column=0, sticky="we", pady=(5, 10))

    login_button = RoundedButton(frame, 200, 40, 20, 10, ACCENT_COLOR, BACKGROUND_COLOR, confirm_account, "Login")
    login_button.grid(row=5, column=0, pady=(30, 0))

def confirm_account():
    email = email_var.get()
    password = password_var.get()

    if not is_valid_email(email):
        messagebox.showwarning("Email Error", "Please enter a valid email address.")
        return

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome back, {user[1]}!")
        main_page(user[0])
    else:
        messagebox.showwarning("Login Failed", "Invalid email or password. Please try again or create a new account.")

def create_account():
    create_account_window = Toplevel(root)
    create_account_window.title("Create Account")
    create_account_window.geometry("500x600")
    create_account_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(create_account_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=40, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Create Your Account", LARGE_FONT, ACCENT_COLOR).grid(row=0, column=0, columnspan=2,
                                                                                     pady=(0, 30))

    fields = [("First Name", first_name_var), ("Second Name", second_name_var), ("Email", create_email_var),
              ("Password", create_password_var), ("Confirm Password", confirm_password_var)]

    for i, (text, var) in enumerate(fields, start=1):
        create_styled_label(frame, text).grid(row=2 * i - 1, column=0, sticky="w", pady=(10, 0))
        create_styled_entry(frame, var, show='*' if 'Password' in text else None).grid(row=2 * i, column=0, sticky="we",
                                                                                       pady=(5, 10))

    create_button = RoundedButton(frame, 200, 40, 20, 10, ACCENT_COLOR, BACKGROUND_COLOR, create_confirm,
                                  "Create Account")
    create_button.grid(row=len(fields) * 2 + 1, column=0, pady=(30, 0))

    back_button = RoundedButton(frame, 200, 40, 20, 10, BUTTON_COLOR, BACKGROUND_COLOR, create_account_window.destroy,
                                "Back to Login")
    back_button.grid(row=len(fields) * 2 + 2, column=0, pady=(15, 0))

def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z]+$', name))

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, email))

def create_confirm():
    fields = [first_name_var, second_name_var, create_email_var, create_password_var, confirm_password_var]
    if not all(field.get() for field in fields):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    if not is_valid_name(first_name_var.get()):
        messagebox.showwarning("Name Error", "First name should contain only alphabets.")
        return

    if not is_valid_name(second_name_var.get()):
        messagebox.showwarning("Name Error", "Second name should contain only alphabets.")
        return

    if not is_valid_email(create_email_var.get()):
        messagebox.showwarning("Email Error", "Please enter a valid email address.")
        return

    if create_password_var.get() != confirm_password_var.get():
        messagebox.showwarning("Password Error", "Passwords do not match.")
        return

    try:
        c.execute("INSERT INTO users (first_name, second_name, email, password, balance) VALUES (?, ?, ?, ?, ?)",
                  (first_name_var.get(), second_name_var.get(), create_email_var.get(), create_password_var.get(), 0.0))
        conn.commit()
        messagebox.showinfo("Account Created", "Your account has been created successfully!")
        sign_in()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Account Error", "Email already registered.")

def main_page(user_id):
    main_window = Toplevel(root)
    main_window.title("Main Page")
    main_window.geometry("600x700")
    main_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(main_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=50, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Welcome to Your Account", LARGE_FONT, ACCENT_COLOR).pack(pady=(0, 30))

    buttons = [("Check Balance", lambda: check_balance(user_id)),
               ("Deposit", lambda: deposit(user_id)),
               ("Withdrawal", lambda: withdraw(user_id)),
               ("Transaction History", lambda: show_transaction_history(user_id)),
               ("Logout", main_window.destroy)]

    for text, command in buttons:
        button = RoundedButton(frame, 250, 50, 25, 10, ACCENT_COLOR if text != "Logout" else ERROR_COLOR,
                               BACKGROUND_COLOR, command, text)
        button.pack(pady=10)


def check_balance(user_id):
    balance_window = Toplevel(root)
    balance_window.title("Account Balance")
    balance_window.geometry("450x600")
    balance_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(balance_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=40, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Updated font definitions
    TITLE_FONT = Font(family="Roboto", size=32, weight="bold")
    SUBTITLE_FONT = Font(family="Roboto", size=18, weight="bold")
    NAME_FONT = Font(family="Roboto", size=24, weight="bold")
    EMAIL_FONT = Font(family="Roboto", size=14)
    BALANCE_LABEL_FONT = Font(family="Roboto", size=16)
    BALANCE_FONT = Font(family="Roboto", size=48, weight="bold")
    SECTION_TITLE_FONT = Font(family="Roboto", size=14, weight="bold")
    DETAIL_FONT = Font(family="Roboto", size=12)

    Label(frame, text="Account Overview", font=TITLE_FONT, fg=ACCENT_COLOR, bg=BACKGROUND_COLOR).pack(pady=(0, 30))

    c.execute("SELECT balance, first_name, second_name, email FROM users WHERE id=?", (user_id,))
    result = c.fetchone()

    if result:
        balance, first_name, second_name, email = result
        balance_text = f"₵{balance:.2f}"

        # User Info Section
        user_info_frame = Frame(frame, bg=BACKGROUND_COLOR, relief=RIDGE, bd=2)
        user_info_frame.pack(pady=(0, 20), padx=10, fill=X)

        Label(user_info_frame, text=f"{first_name} {second_name}", font=NAME_FONT, fg=FOREGROUND_COLOR,
              bg=BACKGROUND_COLOR).pack(pady=(15, 5))
        Label(user_info_frame, text=email, font=EMAIL_FONT, fg=SECONDARY_COLOR, bg=BACKGROUND_COLOR).pack(pady=(0, 15))

        # Balance Section
        balance_frame = Frame(frame, bg=BUTTON_COLOR, relief=RIDGE, bd=2)
        balance_frame.pack(pady=20, padx=10, fill=X)

        Label(balance_frame, text="Current Balance", font=BALANCE_LABEL_FONT, fg=SECONDARY_COLOR, bg=BUTTON_COLOR).pack(
            pady=(20, 10))
        Label(balance_frame, text=balance_text, font=BALANCE_FONT, fg=ACCENT_COLOR, bg=BUTTON_COLOR).pack(pady=(5, 20))

        # Last Transaction Section
        c.execute(
            "SELECT transaction_type, amount, timestamp FROM transactions WHERE user_id=? ORDER BY timestamp DESC LIMIT 1",
            (user_id,))
        last_transaction = c.fetchone()

        if last_transaction:
            trans_type, amount, timestamp = last_transaction
            trans_frame = Frame(frame, bg=BACKGROUND_COLOR)
            trans_frame.pack(pady=20, fill=X)

            Label(trans_frame, text="Last Transaction", font=SECTION_TITLE_FONT, fg=SECONDARY_COLOR,
                  bg=BACKGROUND_COLOR).pack()
            Label(trans_frame, text=f"{trans_type.capitalize()}: ₵{amount:.2f}", font=SUBTITLE_FONT,
                  fg=FOREGROUND_COLOR, bg=BACKGROUND_COLOR).pack(pady=10)
            Label(trans_frame, text=timestamp, font=DETAIL_FONT, fg=SECONDARY_COLOR, bg=BACKGROUND_COLOR).pack()
    else:
        Label(frame, text="Unable to retrieve account information.", font=SUBTITLE_FONT, fg=ERROR_COLOR,
              bg=BACKGROUND_COLOR).pack()

    close_button = RoundedButton(frame, 200, 50, 25, 10, BUTTON_COLOR, BACKGROUND_COLOR, balance_window.destroy,
                                 "Close")
    close_button.pack(pady=(40, 0))

    # Center the balance window on the screen
    balance_window.update_idletasks()
    width = balance_window.winfo_width()
    height = balance_window.winfo_height()
    x = (balance_window.winfo_screenwidth() // 2) - (width // 2)
    y = (balance_window.winfo_screenheight() // 2) - (height // 2)
    balance_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    balance_window.grab_set()  # Make the window modal
    balance_window.focus_set()  # Set focus to the new window


def deposit(user_id):
    deposit_window = Toplevel(root)
    deposit_window.title("Deposit")
    deposit_window.geometry("400x300")
    deposit_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(deposit_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=40, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Deposit", LARGE_FONT, ACCENT_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    create_styled_label(frame, "Amount (₵)").grid(row=1, column=0, sticky="w", pady=(10, 0))
    amount_var = StringVar()
    amount_entry = create_styled_entry(frame, amount_var)
    amount_entry.grid(row=2, column=0, sticky="we", pady=(5, 10))

    def validate_amount():
        try:
            amount = float(amount_var.get())
            if amount <= 0:
                raise ValueError
            return True
        except ValueError:
            messagebox.showwarning("Invalid Amount", "Please enter a valid positive number.")
            return False

    def confirm_deposit():
        if not validate_amount():
            return

        amount = float(amount_var.get())
        confirm = messagebox.askyesno("Confirm Deposit", f"Are you sure you want to deposit ₵{amount:.2f}?")

        if confirm:
            c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
            balance = c.fetchone()[0]
            new_balance = balance + amount
            c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
            c.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (?, ?, ?)",
                      (user_id, "deposit", amount))
            conn.commit()
            messagebox.showinfo("Deposit Successful", f"Deposited ₵{amount:.2f}. New balance: ₵{new_balance:.2f}")
            deposit_window.destroy()

    deposit_button = RoundedButton(frame, 200, 40, 20, 10, ACCENT_COLOR, BACKGROUND_COLOR, confirm_deposit, "Deposit")
    deposit_button.grid(row=3, column=0, pady=(20, 0))

    cancel_button = RoundedButton(frame, 200, 40, 20, 10, BUTTON_COLOR, BACKGROUND_COLOR, deposit_window.destroy,
                                  "Cancel")
    cancel_button.grid(row=4, column=0, pady=(10, 0))

def withdraw(user_id):
    withdraw_window = Toplevel(root)
    withdraw_window.title("Withdraw")
    withdraw_window.geometry("400x300")
    withdraw_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(withdraw_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=40, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Withdraw", LARGE_FONT, ACCENT_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    create_styled_label(frame, "Amount (₵)").grid(row=1, column=0, sticky="w", pady=(10, 0))
    amount_var = StringVar()
    amount_entry = create_styled_entry(frame, amount_var)
    amount_entry.grid(row=2, column=0, sticky="we", pady=(5, 10))

    def validate_amount():
        try:
            amount = float(amount_var.get())
            if amount <= 0:
                raise ValueError
            return True
        except ValueError:
            messagebox.showwarning("Invalid Amount", "Please enter a valid positive number.")
            return False

    def confirm_withdraw():
        if not validate_amount():
            return

        amount = float(amount_var.get())
        c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
        balance = c.fetchone()[0]

        if balance >= amount:
            confirm = messagebox.askyesno("Confirm Withdrawal", f"Are you sure you want to withdraw ₵{amount:.2f}?")

            if confirm:
                new_balance = balance - amount
                c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
                c.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (?, ?, ?)",
                          (user_id, "withdrawal", amount))
                conn.commit()
                messagebox.showinfo("Withdrawal Successful", f"Withdrew ₵{amount:.2f}. New balance: ₵{new_balance:.2f}")
                withdraw_window.destroy()
        else:
            messagebox.showwarning("Insufficient Funds", f"Your current balance (₵{balance:.2f}) is insufficient for this withdrawal.")

    withdraw_button = RoundedButton(frame, 200, 40, 20, 10, ACCENT_COLOR, BACKGROUND_COLOR, confirm_withdraw, "Withdraw")
    withdraw_button.grid(row=3, column=0, pady=(20, 0))

    cancel_button = RoundedButton(frame, 200, 40, 20, 10, BUTTON_COLOR, BACKGROUND_COLOR, withdraw_window.destroy, "Cancel")
    cancel_button.grid(row=4, column=0, pady=(10, 0))

def show_transaction_history(user_id):
    history_window = Toplevel(root)
    history_window.title("Transaction History")
    history_window.geometry("600x400")
    history_window.configure(bg=BACKGROUND_COLOR)

    gradient_frame = GradientFrame(history_window)
    gradient_frame.pack(fill=BOTH, expand=True)

    frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    create_styled_label(frame, "Transaction History", LARGE_FONT, ACCENT_COLOR).pack(pady=(0, 20))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=BUTTON_COLOR,
                    fieldbackground=BUTTON_COLOR, foreground=FOREGROUND_COLOR)
    style.configure("Treeview.Heading", background=ACCENT_COLOR,
                    foreground=BACKGROUND_COLOR, font=MEDIUM_FONT)

    columns = ("Type", "Amount", "Date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", style="Treeview")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=BOTH, expand=1)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')

    tree.configure(yscrollcommand=scrollbar.set)

    c.execute("SELECT transaction_type, amount, timestamp FROM transactions WHERE user_id=? ORDER BY timestamp DESC", (user_id,))
    for transaction in c.fetchall():
        tree.insert("", "end", values=transaction)

# Main Window
gradient_frame = GradientFrame(root)
gradient_frame.pack(fill=BOTH, expand=True)

main_frame = Frame(gradient_frame, bg=BACKGROUND_COLOR, padx=50, pady=30)
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

create_styled_label(main_frame, "Meridian Bank", LARGE_FONT, ACCENT_COLOR).pack(pady=(0, 10))
create_styled_label(main_frame, "OF GHANA", MEDIUM_FONT, SECONDARY_COLOR).pack(pady=(0, 30))
create_styled_label(main_frame, "Welcome to Modern Banking", MEDIUM_FONT).pack(pady=(20, 30))

sign_in_button = RoundedButton(main_frame, 200, 50, 25, 10, ACCENT_COLOR, BACKGROUND_COLOR, sign_in, "Sign In")
sign_in_button.pack(pady=10)

create_account_button = RoundedButton(main_frame, 200, 50, 25, 10, BUTTON_COLOR, BACKGROUND_COLOR, create_account, "Create Account")
create_account_button.pack(pady=10)

exit_button = RoundedButton(main_frame, 200, 50, 25, 10, ERROR_COLOR, BACKGROUND_COLOR, root.quit, "Exit")
exit_button.pack(pady=30)

# Center the main window on the screen
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry(f"+{position_right}+{position_down}")

root.mainloop()

conn.close()  # Close the database connection when the application exits