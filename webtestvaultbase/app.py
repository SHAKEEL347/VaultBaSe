from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this for better security
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return "Login Successful!"
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return "Password is correct!"
    else:
        return "Password is incorrect!"


@app.route('/check_password', methods=['POST'])
def check_password():
    username = request.form['username']
    password = request.form['password']
    result = verify_password(username, password)
    return result  # Returns whether the password is correct or incorrect


from vaultbase import VaultBaSe


vault = VaultBaSe()
print("VaultBaSe module is working correctly!")


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database has been reset!")


    app.run(host='0.0.0.0', port=5000, debug=True)