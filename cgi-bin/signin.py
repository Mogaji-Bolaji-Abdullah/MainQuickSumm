#!/usr/bin/env python3
import cgi
import hashlib

# Function to hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate the user by checking the email and hashed password against stored data
def authenticate_user(email, password):
    try:
        with open('users.txt', 'r') as file:
            users = file.readlines()  # Read all lines from the users.txt file
            for user in users:
                user_email, user_password = user.strip().split(',')  # Split each line into email and hashed password
                if user_email == email and user_password == hash_password(password):  # Check if the email matches and the password hashes match
                    return True  # Return True if authentication is successful
    except FileNotFoundError:
        print("<p>Error: User database not found.</p>")
    return False  # Return False if authentication fails

# Print the HTTP content type header for HTML output
print("Content-type: text/html\n")

# Create an instance of the FieldStorage class to get form data
form = cgi.FieldStorage()
email = form.getvalue('email')  # Get the email from the form data
password = form.getvalue('password')  # Get the password from the form data

# Check if the user is authenticated
if authenticate_user(email, password):
    print("Location: http://localhost:8000/Index.html")  # Redirect to the specific URL
    print()  # End of headers
else:
    print("Password or Email invalid")  