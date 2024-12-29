import random
import mysql.connector
from decimal import Decimal
from datetime import datetime
import re


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhinav@123",
    database="banking_system"
)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    account_number VARCHAR(10) UNIQUE,
    dob DATE,
    city VARCHAR(255),
    password VARCHAR(255),
    balance DECIMAL(10, 2),
    contact_number VARCHAR(10),
    email VARCHAR(255),
    address TEXT,
    active TINYINT DEFAULT 1
)''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(10),
    type VARCHAR(50),
    amount DECIMAL(10, 2),
    date DATETIME
)''')

conn.commit()

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def is_valid_contact(contact):
    return re.match(r"^\d{10}$", contact)

def is_valid_password(password):
    return (len(password) >= 8 and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()-_+=' for c in password))

def add_user():
    name = input("Enter name: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    city = input("Enter city: ")
    password = input("Enter password: ")

    while not is_valid_password(password):
        print("Password must be at least 8 characters long, include an uppercase letter, a number, and a special character.")
        password = input("Enter password: ")

    balance = float(input("Enter initial balance (minimum 2000): "))
    while balance < 2000:
        print("Initial balance must be at least 2000.")
        balance = float(input("Enter initial balance (minimum 2000): "))

    contact = input("Enter contact number: ")
    while not is_valid_contact(contact):
        print("Invalid contact number. It must contain 10 digits.")
        contact = input("Enter contact number: ")

    email = input("Enter email ID: ")
    while not is_valid_email(email):
        print("Invalid email address.")
        email = input("Enter email ID: ")

    address = input("Enter address: ")

    account_number = generate_account_number()

    try:
        c.execute('''INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                  (name, account_number, dob, city, password, balance, contact, email, address))
        conn.commit()
        print(f"User added successfully. Account Number: {account_number}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def show_users():
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    if users:
        for user in users:
            print(f"ID: {user[0]}\nName: {user[1]}\nAccount Number: {user[2]}\nDOB: {user[3]}\nCity: {user[4]}\nBalance: {user[5]}\nContact: {user[6]}\nEmail: {user[7]}\nAddress: {user[8]}\nActive: {'Yes' if user[9] else 'No'}\n")
    else:
        print("No users found.")

def transfer_amount(user):
    # Transfer amount functionality
    amount = float(input("Enter amount to transfer: "))
    if Decimal(amount) > Decimal(user[6]):
        print("Insufficient balance.")
    else:
        receiver_account = Decimal(input("Enter receiver's account number: "))
        c.execute("SELECT * FROM users WHERE account_number = %s", (receiver_account,))
        receiver = c.fetchone()

        if receiver:
            new_sender_balance = (Decimal(user[6]) - Decimal(amount))
            new_receiver_balance = Decimal(receiver[6]) + Decimal(amount)
            c.execute("UPDATE users SET balance = %s WHERE account_number = %s", (new_sender_balance, user[2]))
            c.execute("UPDATE users SET balance = %s WHERE account_number = %s", (new_receiver_balance, receiver_account))
            c.execute("INSERT INTO transactions (account_number, type, amount, date) VALUES (%s, 'Debit', %s, %s)",
                      (user[2], amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            c.execute("INSERT INTO transactions (account_number, type, amount, date) VALUES (%s, 'Credit', %s, %s)",
                      (receiver_account, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            #user[6] = Decimal(new_sender_balance)
            print("Transfer successful.")
        else:
            print("Receiver account not found.")

def toggle_account_status(user):
    
    if user[9] == 1:
        c.execute("UPDATE users SET active = 0 WHERE account_number = %s", (user[2],))
        print("Account deactivated.")
    else:
        c.execute("UPDATE users SET active = 1 WHERE account_number = %s", (user[2],))
        print("Account activated.")
    conn.commit()

def change_password(user):
    
    old_password = input("Enter your old password: ")
    if old_password == user[5]:
        new_password = input("Enter your new password: ")
        while not is_valid_password(new_password):
            print("Password must be at least 8 characters long, include an uppercase letter, a number, and a special character.")
            new_password = input("Enter new password: ")
        c.execute("UPDATE users SET password = %s WHERE account_number = %s", (new_password, user[2]))
        conn.commit()
        print("Password changed successfully.")
    else:
        print("Old password is incorrect.")

def update_profile(user):
   
    print("Updating profile...")
    name = input(f"Enter new name (Current: {user[1]}): ") or user[1]
    city = input(f"Enter new city (Current: {user[4]}): ") or user[4]
    contact = input(f"Enter new contact number (Current: {user[6]}): ") or user[6]
    while not is_valid_contact(contact):
        print("Invalid contact number. It must contain 10 digits.")
        contact = input("Enter contact number: ")
    
    email = input(f"Enter new email (Current: {user[7]}): ") or user[7]
    while not is_valid_email(email):
        print("Invalid email address.")
        email = input("Enter email ID: ")
    
    address = input(f"Enter new address (Current: {user[8]}): ") or user[8]

    c.execute('''UPDATE users SET name = %s, city = %s, contact_number = %s, email = %s, address = %s 
                 WHERE account_number = %s''',
              (name, city, contact, email, address, user[2]))
    conn.commit()
    print("Profile updated successfully.")




def login():
    acc_num = input("Enter account number: ")
    password = input("Enter password: ")

    c.execute("SELECT * FROM users WHERE account_number = %s AND password = %s", (acc_num, password))
    user = c.fetchone()

    if user:
        print("Login successful!")
        while True:
            print("\n1. Show Balance\n2. Show Transactions\n3. Credit Amount\n4. Debit Amount\n5. Transfer Amount\n6. Activate/Deactivate Account\n7. Change Password\n8. Update Profile\n9. Logout")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                print(f"Current Balance: {user[6]}")
            elif choice == 2:
                c.execute("SELECT * FROM transactions WHERE account_number = %s", (acc_num,))
                transactions = c.fetchall()
                for t in transactions:
                    print(f"Type: {t[2]}, Amount: {t[3]}, Date: {t[4]}")
            elif choice == 3:
                amount = float(input("Enter amount to credit: "))
                new_balance = user[6] + Decimal(amount)
                c.execute("UPDATE users SET balance = %s WHERE account_number = %s", (new_balance, acc_num))
                c.execute("INSERT INTO transactions (account_number, type, amount, date) VALUES (%s, 'Credit', %s, %s)",
                          (acc_num, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                user = list(user)
                user[6] = Decimal(new_balance)
                print("Amount credited successfully.")
            elif choice == 4:
                amount = Decimal(input("Enter amount to debit: "))
                if amount > user[6]:
                    print("Insufficient balance.")
                else:
                    new_balance = user[6] - Decimal(amount)
                    c.execute("UPDATE users SET balance = %s WHERE account_number = %s", (new_balance, acc_num))
                    c.execute("INSERT INTO transactions (account_number, type, amount, date) VALUES (%s, 'Debit', %s, %s)",
                              (acc_num, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    user = list(user)
                    user[6] = Decimal(new_balance)
                    print("Amount debited successfully.")
            elif choice == 5:
                transfer_amount(user)
            elif choice == 6:
                toggle_account_status(user)
            elif choice == 7:
                change_password(user)
            elif choice == 8:
                update_profile(user)        
            elif choice == 9:
                print("Logged out.")
                break
            else:
                print("Invalid choice.")
    else:
        print("Invalid account number or password.")

def main():
    while True:
        print("\nBANKING SYSTEM")
        print("1. Add User\n2. Show Users\n3. Login\n4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_user()
        elif choice == 2:
            show_users()
        elif choice == 3:
            login()
        elif choice == 4:
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

conn.close()
