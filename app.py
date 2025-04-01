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
            <style>
                body {
                    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Segoe UI', sans-serif;
                }
                .login-container {
                    background: #fff;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                }
                input[type="text"], input[type="password"] {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border: 1px solid #ccc;
                }
                input[type="submit"] {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(45deg, #00c6ff, #007bff);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                }
                input[type="submit"]:hover {
                    background: linear-gradient(45deg, #0096c7, #0056b3);
                }
                .error {
                    color: red;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <h2>🔐 Secure Login</h2>
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

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>File Server Dashboard</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
                    margin: 0;
                    background: radial-gradient(circle at top, #1a2a6c, #b21f1f, #fdbb2d);
                    color: #fff;
                }
                .container {
                    max-width: 1000px;
                    margin: auto;
                    padding: 40px;
                    background: rgba(0, 0, 0, 0.7);
                    border-radius: 20px;
                    box-shadow: 0 0 25px rgba(255, 255, 255, 0.1);
                    margin-top: 40px;
                }
                h2 {
                    text-align: center;
                    font-size: 32px;
                    margin-bottom: 20px;
                    background: -webkit-linear-gradient(#eee, #333);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .upload-form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    margin-top: 20px;
                }
                .file-input-wrapper {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    background: #fff;
                    border-radius: 6px;
                    padding: 10px;
                    color: #333;
                }
                input[type="file"] {
                    flex: 1;
                    border: none;
                    font-size: 14px;
                }
                input[type="submit"] {
                    background: linear-gradient(90deg, #00c9ff, #92fe9d);
                    border: none;
                    color: #000;
                    font-weight: bold;
                    border-radius: 6px;
                    padding: 12px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: transform 0.2s;
                }
                input[type="submit"]:hover {
                    transform: scale(1.05);
                }
                .folder {
                    margin-top: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 10px 20px;
                }
                .folder h3 {
                    cursor: pointer;
                    user-select: none;
                    margin: 0;
                }
                .file-list {
                    display: none;
                    margin-top: 10px;
                }
                ul {
                    list-style: none;
                    padding-left: 0;
                }
                li {
                    padding: 6px 0;
                    display: flex;
                    align-items: center;
                }
                .file-icon {
                    margin-right: 10px;
                    color: #ffdd57;
                }
                a {
                    color: #80ffdb;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                .logout {
                    text-align: center;
                    margin-top: 30px;
                }
                .logout a {
                    color: #ff4d4d;
                    font-weight: bold;
                    text-decoration: none;
                }
            </style>
            <script>
                function toggleFiles(id) {
                    const section = document.getElementById(id);
                    section.style.display = section.style.display === 'block' ? 'none' : 'block';
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h2>🚀 Welcome, {{ session['username'] }}</h2>

                <form class="upload-form" method="post" action="/upload" enctype="multipart/form-data">
                    <div class="file-input-wrapper">
                        <i class="fas fa-upload"></i>
                        <input type="file" name="file" required>
                    </div>
                    <input type="submit" value="⬆ Upload File">
                </form>

                {% for user, files in user_files.items() %}
                <div class="folder">
                    <h3 onclick="toggleFiles('files_{{ loop.index }}')">📁 {{ user }}'s Files</h3>
                    <div class="file-list" id="files_{{ loop.index }}">
                        <ul>
                            {% for file in files %}
                            <li><i class="fas fa-file file-icon"></i><a href="/files/{{ user }}/{{ file }}">{{ file }}</a></li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endfor %}

                <div class="logout">
                    <a href="/logout">🚪 Logout</a>
                </div>
            </div>
        </body>
        </html>
    ''', user_files=user_files)

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
