
Banking System
Overview
A console-based banking system that manages user accounts and transactions. The system allows users to create accounts, log in, view balances, perform transactions (credit, debit, transfer), and manage profiles.

Features
Add User: Register a new user with:

Name
Random 10-digit Account Number
Date of Birth
City
Valid Password
Initial Balance (min 2000)
Contact Number
Email ID
Address
Show User: Display user details.

Login: Users can log in with their account number and password to:

View balance
View transactions
Credit, debit, or transfer funds
Activate/Deactivate account
Change password
Update profile
Exit: Exit the system.

Database Structure
Database: banking_system
Users: Stores user information.
Login: Stores login credentials (account number & password).
Transaction: Stores transaction details.
Technologies Used
Python: For the core logic.
MySQL: For database management.
random: For generating random account numbers.
decimal: For accurate financial calculations.
datetime: For managing transaction timestamps.
re: For validating user inputs such as emails, phone numbers, and passwords.
Installation
Clone the repository.
Set up the banking_system database in MySQL.
Run the Python application.
