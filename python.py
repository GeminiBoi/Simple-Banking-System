from abc import ABC
import random
import sqlite3
from datetime import datetime

class AccountState:
    def __init__(self):
        self.amount = 0.0
        self.pin = 0

    def set_amount(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount

    def set_pin(self, pin):
        self.pin = pin

    def get_pin(self):
        return self.pin

account_state = AccountState()

class Bank(ABC):
    def __init__(self):
        self.state = account_state

    def create_table(self):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT,
                    second_name TEXT,
                    other_name TEXT,
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
        other_name = input("Othername: ")
        date = input("Date of birth (DD/MM/YYYY): ")
        age = input("Age: ")
        email = input("Email: ")
        password = input("Password: ")
        pin = input("Pin: ")
        security_question = input("Security Question: ")
        security_answer = input("Security Answer: ")

        def is_only_alphabets(s):
            return s.isalpha()

        def contains_at_symbol(m):
            return '@' in m and '.com' in m

        def is_valid_date(n):
            try:
                month, day, year = map(int, n.split('/'))
                return 1 <= month <= 12 and 1 <= day <= 31 and year > 1850
            except ValueError:
                return False

        if all(is_only_alphabets(name) for name in [firstname, second_name, other_name]):
            if contains_at_symbol(email):
                if is_valid_date(date):
                    if int(age) > 0:
                        if len(password) >= 8:
                            self.state.set_amount(float(input("Enter your first deposit: ")))
                            if self.state.get_amount() >= 50:
                                self.state.set_pin(pin)
                                account_number = self.create_accountnum()
                                print("Account created successfully")
                                print("Your Account number is", account_number, "and your balance is", self.state.get_amount())
                                self.save_account(firstname, second_name, other_name, date, age, email, password, pin, self.state.get_amount(), account_number, security_question, security_answer)
                            else:
                                print("Account couldn't be created due to insufficient deposit.")
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
                    INSERT INTO accounts (firstname, second_name, other_name, dob, age, email, password, pin, balance, account_number, security_question, security_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (firstname, second_name, other_name, dob, int(age), email, password, pin, balance, account_number, security_question, security_answer))
                conn.commit()
                print("Account saved successfully.")
                return True
            except sqlite3.IntegrityError:
                print("Error: Email or Account number already exists.")
                return False

    def login_account(self):
        email = input("Email: ")
        password = input("Password: ")
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM accounts WHERE email = ? AND password = ?
            ''', (email, password))
            account = c.fetchone()
            if account:
                print("Login successful!")
                self.state.set_amount(account[8])
                self.state.set_pin(account[7])
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
                print(f"Your PIN is {pin[0]}")
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
                print(f"Your password is {password[0]}")
            else:
                print("Invalid email or security answer.")

class AccountManagement(Bank):
    def __init__(self):
        super().__init__()

    def deposit(self):
        amount = float(input("Enter the amount to deposit: "))
        if amount > 0:
            self.state.set_amount(self.state.get_amount() + amount)
            print(f"Congrats, you have deposited {amount}. New balance: {self.state.get_amount()}.")
        else:
            print("Invalid amount. Enter a valid amount.")

    def withdraw(self):
        amount = float(input("Enter the amount to withdraw: "))
        if amount > 0:
            pin = input("Enter your pin: ")
            if pin == str(self.state.get_pin()):
                if amount <= self.state.get_amount():
                    self.state.set_amount(self.state.get_amount() - amount)
                    print(f"Congrats, you have successfully withdrawn {amount}. New balance: {self.state.get_amount()}.")
                else:
                    print("Insufficient funds.")
            else:
                print("Invalid pin. Try again.")
        else:
            print("Invalid amount.")

    def check_balance(self):
        pin = input("Enter your pin: ")
        if pin == str(self.state.get_pin()):
            print(f"Your account balance is {self.state.get_amount()}.")
        else:
            print("Invalid pin. Try again.")

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
                        self.record_transaction("Domestic Transfer", amount)
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
                        self.record_transaction("Bank Transfer", amount)
                        print(f"You have successfully debited {amount} to {name} at {bank_name}.")
                    else:
                        print("Incorrect pin!")
                else:
                    print("Insufficient funds.")
            else:
                print("Invalid amount.")
        else:
            print("Invalid account number.")

    def record_transaction(self, transaction_type, amount):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                INSERT INTO transactions (account_number, transaction_type, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (self.create_accountnum(), transaction_type, amount, date))
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
                                self.record_transaction("Mobile Transfer", amount)
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

    def record_transaction(self, transaction_type, amount):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                INSERT INTO transactions (account_number, transaction_type, amount, date)
                VALUES (?, ?, ?, ?)
            ''', (self.create_accountnum(), transaction_type, amount, date))
            conn.commit()
