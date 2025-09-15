from flask import Flask, render_template, request, redirect, url_for, session, flash
import scripts.database as db 

app = Flask(__name__)
db.init_db()
db.seed_data()

app.secret_key = "verysecretkey"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'login':
            # Handle login
            user = db.login_user(username,password)
            if user:
                session['user'] = user
                flash(f"Welcome {user['name']} (Grade: {user['grade']})!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password", "danger")
        elif action == 'register':
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():    
    if request.method == "POST":
        action = request.form['action']
        if action == "register":
            username = request.form['username']
            password = request.form['password']
            grade  = request.form['grade']
            name = request.form['name']
            if db.register_user(username, password, name, int(grade)):
                flash(f"Registration successfully! You can now log in ", "success")
                return redirect(url_for('login'))
            else:
                flash("Username already exist try login!", 'danger')
        elif action == "login":
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    user = session['user']
    return render_template("dashboard.html", user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", 'info')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)