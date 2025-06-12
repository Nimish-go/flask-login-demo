from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = psycopg2.connect(database = "flaskdemo", 
                            user = "nimish", 
                            password = "PDolikaM7RrdDDyNm4CnRPkOOWrponpB", 
                            host = "dpg-d15ci33uibrs73br3l7g-a.oregon-postgres.render.com", 
                            port="5432")
    
    if conn :
        print("Connected to database")
    
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
#             print (user[2])
            return redirect('/dashboard')
        return "Invalid Credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username = session['username'])
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)