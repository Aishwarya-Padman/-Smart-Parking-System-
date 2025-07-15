from flask import Flask, jsonify, render_template, request, redirect, flash, session, url_for
from flask_mysqldb import MySQL  # ✅ Correct MySQL library
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key

# ✅ MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "parking"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)  # ✅ Initialize MySQL connection

# ✅ SQLAlchemy Configuration (If using SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/parking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # ✅ Initialize SQLAlchemy


# ✅ **User Model (Only if using SQLAlchemy)**
class User(db.Model):  # ✅ Must inherit from db.Model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    def set_password(self, password):  # ✅ Hashing function
        self.password = generate_password_hash(password)

    def check_password(self, password):  # ✅ Checking password
        return check_password_hash(self.password, password)


# ✅ **Registration Route**
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Validate input
        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("register"))

        cursor = mysql.connection.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email is already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ✅ **Login Route**
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session['username'] = user["name"]
            session['email'] = user["email"]
            flash('Login successful!', 'success')
            return redirect(url_for('reservation'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')




class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_number = db.Column(db.String(10), nullable=False)
    car_make = db.Column(db.String(50), nullable=False)
    car_model = db.Column(db.String(50), nullable=False)
    car_year = db.Column(db.String(4), nullable=False)
    car_license = db.Column(db.String(20), unique=True, nullable=False)


@app.route('/reserve', methods=['POST'])
def reserve_parking():
    try:
        data = request.json
        print("Received data:", data)  # Debugging ke liye

        new_reservation = Reservation(
            slot_number=data.get('slotNumber', 'P1'),  # Default slot if not provided
            car_make=data['carMake'],
            car_model=data['carModel'],
            car_year=data['carYear'],
            car_license=data['carLicense']
        )

        db.session.add(new_reservation)
        db.session.commit()
        print("Data inserted successfully!")  # Debugging ke liye
        
        return jsonify({'message': 'Reservation successful!', 'reservation_id': new_reservation.id})

    except Exception as e:
        print("Error:", e)  # Error print karne ke liye
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# ✅ **Parking Page (Protected Route)**
@app.route('/parking')
def parking():
    if 'username' in session:
        session['last_page'] = request.path  # Track last visited page
        return render_template('parking.html', username=session['username'])
    flash("Please log in first.", "danger")
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


# ✅ **Logout**
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ✅ **Ensure Database Tables Exist**
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
