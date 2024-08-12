import hashlib
import sqlite3
from datetime import datetime
from abc import ABC
import re
import random

# Hashing utility function
def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Validate PIN
def validate_pin(pin):
    return pin.isdigit() and len(pin) == 4

# Validate Password
def validate_password(password):
    return len(password) >= 8

# Validate Email
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Validate Date
def is_valid_date(date_str):
    try:
        day, month, year = map(int, date_str.split('/'))
        return 1 <= day <= 31 and 1 <= month <= 12 and year > 1850
    except ValueError:
        return False

class AccountState:
    def __init__(self):
        self.amount = 0.0
        self.pin = ""
        self.account_number = ""

    def set_amount(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount

    def set_pin(self, pin):
        self.pin = pin

    def get_pin(self):
        return self.pin

    def set_account_number(self, account_number):
        self.account_number = account_number

    def get_account_number(self):
        return self.account_number

account_state = AccountState()

class Bank(ABC):
    def __init__(self):
        self.state = account_state
        self.create_table()
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()
    def create_table(self):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS accounts')  # Drop the table if it exists
            c.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT,
                    second_name TEXT,
                    dob TEXT,
                    age INTEGER,
                    email TEXT UNIQUE,
                    password TEXT,
                    pin TEXT,
                    balance REAL,
                    account_number TEXT UNIQUE,
                    security_question TEXT,
                    security_answer TEXT
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    transaction_type TEXT,
                    amount REAL,
                    date TEXT
                )
            ''')
            conn.commit()

class Account(Bank):
    def __init__(self):
        super().__init__()

    def create_accountnum(self):
        acc = "14" + ''.join([str(random.randint(10, 99)) for _ in range(4)])
        return acc

    def create_account(self):
        firstname = input("Firstname: ")
        second_name = input("Secondname: ")
        dob = input("Date of birth (DD/MM/YYYY): ")
        age = input("Age: ")
        email = input("Email: ")
        password = input("Password: ")
        pin = input("PIN (4 digits): ")
        security_question = input("Security Question: ")
        security_answer = input("Security Answer: ")

        # Validation checks
        if all(s.isalpha() for s in [firstname, second_name]):
            if is_valid_email(email):
                if is_valid_date(dob):
                    if int(age) > 0:
                        if validate_password(password):
                            if validate_pin(pin):
                                deposit_amount = float(input("Enter your first deposit: "))
                                if deposit_amount >= 50:
                                    hashed_password = hash_value(password)
                                    hashed_pin = hash_value(pin)
                                    account_number = self.create_accountnum()
                                    print("Account created successfully")
                                    print(f"Your Account number is {account_number} and your balance is {deposit_amount:.2f}")
                                    self.save_account(firstname, second_name, dob, age, email, hashed_password, hashed_pin, deposit_amount, account_number, security_question, security_answer)
                                else:
                                    print("Account couldn't be created due to insufficient deposit.")
                            else:
                                print("Invalid PIN. It must be 4 digits.")
                        else:
                            print("Password must be at least 8 characters long.")
                    else:
                        print("Invalid age.")
                else:
                    print("Invalid date of birth.")
            else:
                print("Invalid email address.")
        else:
            print("Invalid name.")

    def save_account(self, firstname, second_name, other_name, dob, age, email, password, pin, balance, account_number, security_question, security_answer):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            try:
                c.execute('''
                    INSERT INTO accounts (firstname, second_name, dob, age, email, password, pin, balance, account_number, security_question, security_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (firstname, second_name, other_name, dob, int(age), email, password, pin, balance, account_number, security_question, security_answer))
                conn.commit()
                print("Account saved successfully.")
                return True
            except sqlite3.IntegrityError:
                print("Error: Email or Account number already exists.")
                return False

    def login_account(self,email,password):
        self.email=email
        self.password=password

        email = input("Email: ")
        password = input("Password: ")
        hashed_password = hash_value(password)

        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM accounts WHERE email = ? AND password = ?
            ''', (email, hashed_password))
            account = c.fetchone()

            if account:
                print("Login successful!")
                self.state.set_amount(account[9])  # Assuming column index 9 is the balance
                self.state.set_pin(account[8])  # Assuming column index 8 is the PIN
                self.state.set_account_number(account[10])  # Assuming column index 10 is the account number
                return True
            else:
                print("Invalid email or password")
                return False

    def recover_pin(self):
        email = input("Enter your email: ")
        security_answer = input("Enter your security answer: ")
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT pin FROM accounts WHERE email = ? AND security_answer = ?
            ''', (email, security_answer))
            pin = c.fetchone()
            if pin:
                new_pin = input("Enter a new PIN (4 digits): ")
                confirm_pin = input("Confirm your new PIN: ")
                if new_pin == confirm_pin:
                    if validate_pin(new_pin):
                        hashed_pin = hash_value(new_pin)
                        c.execute('''
                            UPDATE accounts SET pin = ? WHERE email = ?
                        ''', (hashed_pin, email))
                        conn.commit()
                        print("PIN updated successfully.")
                    else:
                        print("Invalid PIN. It must be 4 digits.")
                else:
                    print("PINs do not match. Please try again.")
            else:
                print("Invalid email or security answer.")

    def recover_password(self):
        email = input("Enter your email: ")
        security_answer = input("Enter your security answer: ")
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT password FROM accounts WHERE email = ? AND security_answer = ?
            ''', (email, security_answer))
            password = c.fetchone()
            if password:
                new_password = input("Enter a new password: ")
                confirm_password = input("Confirm your new password: ")
                if new_password == confirm_password:
                    if validate_password(new_password):
                        hashed_password = hash_value(new_password)
                        c.execute('''
                            UPDATE accounts SET password = ? WHERE email = ?
                        ''', (hashed_password, email))
                        conn.commit()
                        print("Password updated successfully.")
                    else:
                        print("Password must be at least 8 characters long.")
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Invalid email or security answer.")

class AccountManagement(Bank):
    def __init__(self):
        super().__init__()

    def deposit(self):
        try:
            amount = float(input("Enter the amount to deposit: "))
            if amount > 0:
                new_balance = self.state.get_amount() + amount
                self.c.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (new_balance, self.state.get_account_number()))
                self.conn.commit()
                self.state.set_amount(new_balance)  # Update the state
                print(f"Congrats, you have deposited {amount:.2f}. New balance: {self.state.get_amount():.2f}.")
                self.record_transaction("Deposit", amount)
            else:
                print("Invalid amount. Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def withdraw(self):
        try:
            amount = float(input("Enter the amount to withdraw: "))
            if amount > 0:
                pin = input("Enter your PIN: ")
                if hash_value(pin) == self.state.get_pin():
                    if amount <= self.state.get_amount():
                        new_balance = self.state.get_amount() - amount
                        self.c.execute('UPDATE accounts SET balance = ? WHERE account_number = ?', (new_balance, self.state.get_account_number()))
                        self.conn.commit()
                        self.state.set_amount(new_balance)  # Update the state
                        print(f"Congrats, you have successfully withdrawn {amount:.2f}. New balance: {self.state.get_amount():.2f}.")
                        self.record_transaction("Withdrawal", amount)
                    else:
                        print("Insufficient funds.")
                else:
                    print("Invalid PIN. Please try again.")
            else:
                print("Invalid amount. Please enter a positive value.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    def check_balance(self):
        pin = input("Enter your PIN: ")
        if hash_value(pin) == self.state.get_pin():
            print(f"Your account balance is {self.state.get_amount():.2f}.")
        else:
            print("Invalid PIN. Please try again.")

    def record_transaction(self, transaction_type, amount):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                INSERT INTO transactions (account_number, transaction_type, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (self.state.get_account_number(), transaction_type, amount, date))
            conn.commit()

class MoneyTransfer(Bank):
    def __init__(self):
        super().__init__()

    def dom_transfer(self):
        def is_only_alphabets(s):
            return s.isalpha()

        account_num = input("Enter the account number: ")
        name = input("Enter the name on the account number: ")
        if len(account_num) == 10 and is_only_alphabets(name):
            amount = float(input("Enter the amount to transfer: "))
            if amount > 0:
                if amount <= self.state.get_amount():
                    pin = input("Enter your pin: ")
                    if pin == str(self.state.get_pin()):
                        self.state.set_amount(self.state.get_amount() - amount)
                        self.record_transaction("Domestic Transfer", amount, account_num)
                        print(f"You have successfully debited {amount} to {name}.")
                    else:
                        print("Incorrect pin!")
                else:
                    print("Insufficient funds.")
            else:
                print("Invalid amount.")
        else:
            print("Invalid account number or name.")

    def bank_transfer(self):
        bank_name = input("Enter the name of the bank: ")
        bank_account = input("Enter the account number: ")
        name = input("Enter the name of the account holder: ")
        def is_only_digit(n):
            return n.isdigit()

        if is_only_digit(bank_account):
            amount = float(input("Enter the amount to transfer: "))
            if amount > 0:
                if amount <= self.state.get_amount():
                    pin = input("Enter your pin: ")
                    if pin == str(self.state.get_pin()):
                        self.state.set_amount(self.state.get_amount() - amount)
                        self.record_transaction("Bank Transfer", amount, bank_account)
                        print(f"You have successfully debited {amount} to {name} at {bank_name}.")
                    else:
                        print("Incorrect pin!")
                else:
                    print("Insufficient funds.")
            else:
                print("Invalid amount.")
        else:
            print("Invalid account number.")

    def record_transaction(self, transaction_type, amount, account_number):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                INSERT INTO transactions (account_number, transaction_type, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (account_number, transaction_type, amount, date))
            conn.commit()

class MomoTransfer(Bank):
    def __init__(self):
        super().__init__()

    def choose_network(self):
        networks = {
            '1': 'MTN',
            '2': 'Vodafone',
            '3': 'AirtelTigo'
        }

        choice = input("""Enter your choice 
        (1: MTN Momo 
        2: Vodafone Cash 
        3: AirtelTigo Money): """)

        if choice in networks:
            number = input("Enter the number: ")
            if len(number) in [10, 12]:
                name = input("Enter the name on the number: ")
                try:
                    amount = float(input("Enter the amount to transfer: "))
                    if amount > 0:
                        if amount <= self.state.get_amount():
                            pin = input("Enter your PIN: ")
                            if pin == str(self.state.get_pin()):
                                self.state.set_amount(self.state.get_amount() - amount)
                                self.record_transaction("Mobile Transfer", amount, number)
                                print(f"You have successfully debited {amount} to {name}.")
                            else:
                                print("Invalid PIN. Please try again.")
                        else:
                            print("Insufficient funds.")
                    else:
                        print("Invalid amount. It should be greater than zero.")
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            else:
                print("Invalid number length. Please enter a 10 or 12 digit number.")
        else:
            print("Invalid choice. Please select a valid network.")

    def record_transaction(self, transaction_type, amount, number):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                INSERT INTO transactions (account_number, transaction_type, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (number, transaction_type, amount, date))
            conn.commit()
