from abc import ABC
import random
import sqlite3
class Bank(ABC):
    def __init__(self):
        self.amount = 0.0

    def create_table(self):
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT,
                    secondname TEXT,
                    othername TEXT,
                    dob TEXT,
                    age INTEGER,
                    email TEXT UNIQUE,
                    password TEXT,
                    balance REAL,
                    account_number TEXT UNIQUE
                )
            ''')
            conn.commit()

class Account(Bank):
    def __init__(self):
        super().__init__()

    def create_accountnum(self):
        random_int1 = random.randint(10, 99)
        acc = ''

        for i in range(1, 5):
            random_inti = random.randint(10, 100)
            acc += str(random_inti)

        print(acc)

        acc1 = "14" + acc
        return acc1
    def create_account(self):
        firstname = input("Firstname: ")
        second_name = input("Secondname: ")
        other_name = input("Othername: ")
        date = input("Date of birth(DD/MM/YYYY) ")
        Age = input("Age: ")
        email = input("Email: ")
        password = input("Password: ")

        def is_only_alphabets(s):
            return s.isalpha()

        def contains_at_symbol(m):
            return '@' and '.com' in m

        def is_only_numbers(n):
            try:
                month, day, year = map(int, n.split('/'))
                return 1 <= month <= 12 and 1 <= day <= 31 and year > 1850
            except ValueError:
                return False

        if is_only_alphabets(firstname) and is_only_alphabets(second_name) and is_only_alphabets(other_name) is True:
            if contains_at_symbol(email) is True:
                if is_only_numbers(date) is True:
                    if int(Age) > 0:
                        if len(password) >= 8:
                            self.amount = float(input("Enter your first deposit: "))
                            if self.amount >= 50:
                                pin = input("Enter your pin: ")
                                print("Account created successfully")
                                print("Your Account number is", self.create_accountnum())
                            elif self.amount < 50:
                                print("Account couldn't be created")
                    elif int(Age) <= 0:
                        print("Invalid age")
                elif is_only_numbers(date) is False:
                    print("Invalid date of birth")
            elif contains_at_symbol(email) is False:
                print("Invalid email")
        elif is_only_alphabets(firstname) and is_only_alphabets(second_name) and is_only_alphabets(other_name) is False:
            print("Invalid name")

    def save_account(self, firstname, second_name, other_name, dob, age, email, password, balance):
        account_number = self.create_accountnum()
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            try:
                c.execute('''
                    INSERT INTO accounts (firstname, secondname, othername, dob, age, email, password, balance, account_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (firstname, second_name, other_name, dob, int(age), email, password, balance, account_number))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print("Error: Email or Account number already exists.")
                return False


    def login_account(self):
        self.email = input("Email: ")
        self.password = input("Password: ")
        with sqlite3.connect('bank.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT * FROM accounts WHERE email = ? AND password = ?
            ''', (self.email, self.password))
            account = c.fetchone()
            if account:
                print("Login successful!")
                print("Account details:", account)
            else:
                print("Invalid email or password")


class MoneyTransfer(Bank):
    def __init__(self):
        super().__init__()

    def deposit(self):
        self.amount = float(input("Enter the amount to deposit: "))
        if self.amount > 0:
            print("Congrats you have deposited ", str(self.amount))
        elif self.amount < 0:
            self.amount = float(input("Enter the amount to deposit: "))
            if self.amount > 0:
                print("Congrats you have deposited ", str(self.amount))
            elif self.amount < 0:
                self.amount = float(input("Enter the amount to deposit: "))
        else:
            print("Invalid amount. Enter a valid amount.")

    def withdraw(self):
        self.amount = float(input("Enter the amount to withdraw: "))
        if self.amount > 0:
            pin = int(input("Enter your pin: "))
            if pin is True:
                print("Congrats you have successfully withdrawn ", self.amount)
            elif pin is False:
                print("Invalid pin. Try again.")
                pin = int(input("Enter your pin: "))
                if pin is True:
                    print("Congrats you have successfully withdrawn ", self.amount)
                elif pin is False:
                    print("Invalid pin. Try again.")
            else:
                print("Invalid input. Digits only.")

    def check_balance(self):
        fullname = self.firstname + self.second_name + self.other_name
        print("Welcome ", fullname)
        print(self.acc1)
        print("Show your balance.")
        pin = int(input("Enter your pin: "))

        if pin is True:
            print("Your account balance is ", self.amount)
        elif pin is False:
            print("Invalid pin. Try again.")
            pin = int(input("Enter your pin: "))
            if pin is True:
                print("Your account balance is ", self.amount)
            elif pin is False:
                print("Invalid pin. Try again.")
        else:
            print("Invalid input. Couldn't check your balance")

    def dom_transfer(self):
        def is_only_alphabets(s):
            return s.isalpha()

        account_num = input("Enter the account number: ")
        nam = input("Enter name on the account number: ")
        if len(account_num) == 10 and is_only_alphabets(nam) is True:
            balance = float(input("Enter the amount to transfer:  "))
            if balance > 0:
                if balance <= self.amount:
                    pin = int(input("Enter your pin: "))
                    print("You have successfully debited the accountnn")
                elif balance > self.amount:
                    print("Invalid amount")
                    balance = float(input("Enter the amount to transfer:  "))
            elif balance < 0:
                print("Invalid amount")
                balance = float(input("Enter the amount to transfer:  "))

        else:
            print("Invalid input")

    def display_network(self):
        print("Choose the network")
        print("""1. MTN 
                2. Vodafone
                3. AirtelTigo """)

    def choose_network(self):
        choice = input("Enter your choice: ")
        if choice == '1':
            number = input("Enter the number ")
            if len(number) == 10 or 12:
                name = input("Enter the name on the number: ")
                balance = float(input("Enter the amount to transfer: "))
                if balance > 0:
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                            pin = int(input("Enter your pin: "))
                            if pin is True:
                                print("You have successfully debited ", str(balance), " to ", name)
                            else:
                                print("Invalid pin.")
                    elif balance > self.amount:
                        print("Invalid amount")
                        balance = float(input("Enter the amount to transfer:  "))
                        if balance <= self.amount:
                            pin = int(input("Enter your pin: "))
                            print("You have successfully debited ", str(balance), " to ", name)
                        else:
                            print("Invalid amount")
                elif balance < 0:
                    print("Invalid amount")
                    balance = float(input("Enter the amount to transfer:  "))
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                else:
                    print("Invalid amount")
            else:
                print("Wrong number")
        elif choice == '2':
            number = input("Enter the number ")
            if len(number) == 10 or 12:
                name = input("Enter the name on the number: ")
                balance = float(input("Enter the amount to transfer: "))
                if balance > 0:
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                            pin = int(input("Enter your pin: "))
                            if pin is True:
                                print("You have successfully debited ", str(balance), " to ", name)
                            else:
                                print("Invalid pin.")
                    elif balance > self.amount:
                        print("Invalid amount")
                        balance = float(input("Enter the amount to transfer:  "))
                        if balance <= self.amount:
                            pin = int(input("Enter your pin: "))
                            print("You have successfully debited ", str(balance), " to ", name)
                        else:
                            print("Invalid amount")
                elif balance < 0:
                    print("Invalid amount")
                    balance = float(input("Enter the amount to transfer:  "))
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                else:
                    print("Invalid amount")
            else:
                print("Wrong number")
        elif choice == '3':
            number = input("Enter the number ")
            if len(number) == 10 or 12:
                name = input("Enter the name on the number: ")
                balance = float(input("Enter the amount to transfer: "))
                if balance > 0:
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                            pin = int(input("Enter your pin: "))
                            if pin is True:
                                print("You have successfully debited ", str(balance), " to ", name)
                            else:
                                print("Invalid pin.")
                    elif balance > self.amount:
                        print("Invalid amount")
                        balance = float(input("Enter the amount to transfer:  "))
                        if balance <= self.amount:
                            pin = int(input("Enter your pin: "))
                            print("You have successfully debited ", str(balance), " to ", name)
                        else:
                            print("Invalid amount")
                elif balance < 0:
                    print("Invalid amount")
                    balance = float(input("Enter the amount to transfer:  "))
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        elif pin is False:
                            print("Type your pin again")
                else:
                    print("Invalid amount")
            else:
                print("Wrong number")
        else:
            print("Invalid choice")

    def bank_transfer(self):
        bank_name = input("Enter the name of the bank: ")
        bank_account = input("Enter the account number: ")
        name = input("Enter the name of the account holder: ")
        def is_only_digit(n):
            return n.isdigit()

        if is_only_digit(bank_account) is True:
            balance = float(input("Enter the amount to transfer: "))
            if balance > 0:
                if balance <= self.amount:
                    pin = int(input("Enter your pin: "))
                    if pin is True:
                        print("You have successfully debited ", str(balance), " to ", name)
                    elif pin is False:
                        print("Type your pin again")
                        pin = int(input("Enter your pin: "))
                        if pin is True:
                            print("You have successfully debited ", str(balance), " to ", name)
                        else:
                            print("Invalid pin.")
                elif balance > self.amount:
                    print("Invalid amount")
                    balance = float(input("Enter the amount to transfer:  "))
                    if balance <= self.amount:
                        pin = int(input("Enter your pin: "))
                        print("You have successfully debited ", str(balance), " to ", name)
                    else:
                        print("Invalid amount")
            elif balance < 0:
                print("Invalid amount")
                balance = float(input("Enter the amount to transfer:  "))
                if balance <= self.amount:
                    pin = int(input("Enter your pin: "))
                    if pin is True:
                        print("You have successfully debited ", str(balance), " to ", name)
                    elif pin is False:
                        print("Type your pin again")
            else:
                print("Invalid amount")