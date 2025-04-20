import re
import json
from datetime import datetime
import os

DATA_FILE = "login_data.json"

# Load data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Validation functions
def validate_name(name):
    return name.isalpha()

def validate_dob(dob):
    try:
        datetime.strptime(dob, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_email(email):
    return "@" in email and "." in email

def validate_password(password):
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False

# Register
def register():
    data = load_data()
    name = input("Enter your name: ")
    if not validate_name(name):
        print("Invalid name. Only alphabets allowed.")
        return

    dob = input("Enter DOB (dd-mm-yyyy): ")
    if not validate_dob(dob):
        print("Invalid date format.")
        return

    phone = input("Enter phone number: ")
    if not validate_phone(phone):
        print("Phone number must be 10 digits.")
        return

    email = input("Enter your email: ")
    if not validate_email(email):
        print("Invalid email format.")
        return

    if email in data:
        print("User already exists. Try logging in.")
        return

    password = input("Enter password: ")
    if not validate_password(password):
        print("Password must have at least one uppercase, one lowercase, one number, one special character and be at least 8 characters.")
        return

    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match.")
        return

    data[email] = {
        "name": name,
        "dob": dob,
        "phone": phone,
        "password": password
    }

    save_data(data)
    print("Registration successful!")

# Login
def login():
    data = load_data()
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = data.get(email)
    if user and user["password"] == password:
        print(f"Welcome back, {user['name']}!")
    else:
        print("Invalid email or password.")

# Forgot Password
def forgot_password():
    data = load_data()
    email = input("Enter your email: ")

    if email not in data:
        print("Email not registered.")
        return

    print(f"Your current password is: {data[email]['password']}")
    new_password = input("Enter new password: ")
    if not validate_password(new_password):
        print("Password does not meet requirements.")
        return

    confirm_password = input("Confirm new password: ")
    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    data[email]["password"] = new_password
    save_data(data)
    print("Password updated successfully!")

# Menu
def main():
    while True:
        print("\n--- Login System ---")
        print("1. Register")
        print("2. Login")
        print("3. Forgot Password")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            forgot_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
