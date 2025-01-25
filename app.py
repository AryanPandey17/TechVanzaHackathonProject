from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import requests
from requests.auth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key

# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',  # Replace with your MySQL password
        database='appointment_booking'  # The database name
    )

# Login Required Decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash("You must be logged in to access this page.", "error")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (username,))
                user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                session['user'] = user['email']
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password.", "error")
        except Error as e:
            print(f"Database error: {e}")
            flash("An error occurred. Please try again later.", "error")

    return render_template('login.html')

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

# Appointment Route (Protected)
@app.route('/appointment', methods=['GET', 'POST'])

def appointment():
    if request.method == 'POST':
        doctor = request.form['doctor']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        patient_symptoms = request.form.get('patient_symptoms', '')

        # Insert form data into MySQL
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (doctor, appointment_date, appointment_time, patient_name, patient_age, patient_symptoms) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (doctor, appointment_date, appointment_time, patient_name, patient_age, patient_symptoms))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Appointment booked successfully!", "success")
            return redirect(url_for('home'))
        except Error as e:
            print(f"Error: {e}")
            flash("There was an error submitting your appointment. Please try again.", "error")

    return render_template('appointment.html')

# Lab Test Route (Protected)
@app.route('/labtest', methods=['GET', 'POST'])

def labtest():
    if request.method == 'POST':
        try:
            full_name = request.form['full_name']
            email = request.form['email']
            phone = request.form['phone']
            preferred_date = request.form['preferred_date']
            address = request.form['address']
            terms_accepted = request.form.get('terms') == 'on'

            # Insert form data into MySQL
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (full_name, email, phone, preferred_date, address, terms_accepted) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (full_name, email, phone, preferred_date, address, terms_accepted))
            conn.commit()
            cursor.close()
            conn.close()

            # Send confirmation message via Twilio
            message_body = f"Hello {full_name}, your appointment has been confirmed for {preferred_date}."
            send_twilio_message(message_body)
            flash("Lab test booked successfully!", "success")
            return redirect(url_for('home'))
        except Error as e:
            print(f"Database error: {e}")
            flash("There was an error booking your lab test. Please try again.", "error")

    return render_template('labtest.html')

# Function to send a message through Twilio
def send_twilio_message(message_body):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json"
    data = {
        'To': RECIPIENT_PHONE,
        'From': TWILIO_PHONE_NUMBER,
        'Body': message_body
    }
    response = requests.post(url, data=data, auth=HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN))
    if response.status_code == 201:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")

# Route for Blogs Page
@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

# Route for About Us Page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Validate form input
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('register'))

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password, method='sha256')

        # Store data in the database
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (email, password) 
                    VALUES (%s, %s)
                """, (email, hashed_password))
                conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except Error as e:
            print(f"Database error: {e}")
            flash("An error occurred while creating your account. Please try again.", "error")

    return render_template('register.html')  # Handle GET request and return the registration form

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
