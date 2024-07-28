#!/usr/bin/env python3
import cgi
import hashlib

# Function to hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register a new user by appending their data to users.txt
def register_user(email, password):
    with open('users.txt', 'a') as file:  # Open users.txt in append mode
        file.write(f'{email},{hash_password(password)}\n')  # Write email and hashed password to the file

# Function to check if a user with the given email already exists
def user_exists(email):
    try:
        with open('users.txt', 'r') as file:  # Open users.txt in read mode
            users = file.readlines()  # Read all lines from the file
            for user in users:
                if user.split(',')[0] == email:  # Check if the email matches any stored email
                    return True  # Return True if a match is found
    except FileNotFoundError:
        return False  # If the file doesn't exist, assume the user doesn't exist
    return False  # Return False if no match is found

# Print the HTTP content type header for HTML output
print("Content-type: text/html\n")

# Create an instance of the FieldStorage class to get form data
form = cgi.FieldStorage()
email = form.getvalue('email')  # Get the email from the form data
password = form.getvalue('password')  # Get the password from the form data
confirm_password = form.getvalue('confirm_password')  # Get the confirm password from the form data

# Check if the passwords match
if password != confirm_password:
    print("<p>Passwords do not match!</p>")  # Print an error message if passwords do not match
# Check if the user already exists
elif user_exists(email):
    print("<p>User already exists!</p>")  # Print an error message if the user already exists
# Register the user
else:
    register_user(email, password)  # Register the new user
    print("<p>User registered successfully!</p>")  # Print a success message if registration is successful
