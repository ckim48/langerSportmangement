# Flask --> Open-source Python framework which allows you to make web application with python.
# every html goes to folder 'templates'
# every css/js + image files go to 'static'


from flask import Flask, render_template, request, url_for, redirect, flash, session #we are going to use flask for this python code
from datetime import timedelta
import sqlite3

app = Flask(__name__) # it creates an empty web application
app.secret_key = "abc"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=3)
# Session = {}
# As soon as user logs in
# Session = {"username" : "test"}
# added the homepage --> for now we dont have the html file for the homepage, but we just have "hello world"
@app.route('/')
def index():
    isLogin = False
    if 'username' in session:
        isLogin = True
    return render_template('index.html', isLogin=isLogin)

@app.route('/admin')
def admin():
    isLogin = False
    if 'username' in session:
        isLogin = True

    conn = sqlite3.connect('static/database.db')
    cursor = conn.cursor()
    command = "SELECT username,gender,age FROM Users;"
    cursor.execute(command)
    result = cursor.fetchall() # [ (scott,Male,20), (alice,Female,30), ....)

    users_index = [i for i in range(1, len(result)+1)] # [1,2,3,... N]
    users_username = []
    users_gender = []
    users_age = []
    for user in result:
        users_username.append(user[0]) #["scott","alice",,]
        users_gender.append(user[1])  # ["Male","Female",,]
        users_age.append(user[2])  # [20,30,,]

    return render_template('datadisplay.html', isLogin=isLogin, num_users = len(result), users_index = users_index, username = users_username,gender=users_gender,age = users_age )

# we added the login page to our web application
@app.route('/login', methods = ["GET", "POST"] )
def login():
    if request.method == "POST":
        username = request.form['username'] # scott
        password = request.form['password'] # 123

        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()
        command = "SELECT password FROM Users Where username = ?;"
        cursor.execute(command, (username, ))
        password_db = cursor.fetchone() # (abc, ) or None
        if password_db is None: # when user tries to login with the username that have not registered.
            flash('Wrong username or password')
            return render_template('login.html')


        if password == password_db[0]: #when username and password are valid
            session["username"] = username #session = {"username" : "test"}
            return redirect(url_for('index')) #we are sending user to the homepage
        else: #when invalid
            flash('wrong username or password')
            return render_template('login.html')#stay in the login page
    else:
        return render_template('login.html')

@app.route('/register', methods = ["GET", "POST"] )
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()

        command = "SELECT password FROM Users Where username = ?;"
        cursor.execute(command, (username,))
        result = cursor.fetchone()
        if result is None:
            command = "INSERT INTO Users (username,password) VALUES (?,?);"
            cursor.execute(command, (username, password,))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            flash("Existing Username")
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000) #run our web application