from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'

# 🔐 Store hashed passwords
USERS = {
    'Aditya': generate_password_hash('mypassword'),
    'Varsha': generate_password_hash('test123'),
    'Akshay': generate_password_hash('test123'),
    'Shubham': generate_password_hash('test123')
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
for user in USERS:
    os.makedirs(os.path.join(UPLOAD_FOLDER, user), exist_ok=True)

@app.before_request
def reset_session_on_restart():
    if not request.endpoint or request.endpoint == 'static':
        return
    if 'username' not in session and request.endpoint not in ['login']:
        session.clear()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and check_password_hash(USERS[username], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">
            <style>
                body {
                    background: linear-gradient(to right, #141e30, #243b55);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Orbitron', sans-serif;
                    margin: 0;
                    color: white;
                }
                .login-container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                input[type="text"], input[type="password"] {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border: none;
                    background: rgba(255,255,255,0.2);
                    color: white;
                    font-size: 16px;
                }
                input[type="text"]::placeholder,
                input[type="password"]::placeholder {
                    color: #ccc;
                }
                input[type="submit"] {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(90deg, #00d2ff, #3a7bd5);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                    margin-top: 10px;
                }
                input[type="submit"]:hover {
                    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
                }
                .error {
                    color: #ff6b6b;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>🔐 Futuristic Login</h2>
                <form method="post">
                    <input type="text" name="username" placeholder="Username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <input type="submit" value="Login">
                </form>
                {% if error %}<div class="error">{{ error }}</div>{% endif %}
            </div>
        </body>
        </html>
    ''', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    current_user = session['username']
    if current_user == 'Aditya':
        user_dirs = USERS.keys()
    else:
        user_dirs = [current_user]

    user_files = {}
    for user in user_dirs:
        folder_path = os.path.join(UPLOAD_FOLDER, user)
        user_files[user] = os.listdir(folder_path)

    return render_template_string(''' ... [REMAINS UNCHANGED] ... ''', user_files=user_files)

@app.route('/files/<user>/<filename>')
def serve_file(user, filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    current_user = session['username']
    if current_user != 'Aditya' and user != current_user:
        return "Unauthorized", 403

    folder = os.path.join(UPLOAD_FOLDER, user)
    return send_from_directory(folder, filename)

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user = session['username']
    f = request.files['file']
    if f:
        f.save(os.path.join(UPLOAD_FOLDER, user, f.filename))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
