from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import mysql.connector
import markdown
import os
import uuid
from werkzeug.utils import secure_filename
from custom_markdown import CodeBlockExtension
import time

app = Flask(__name__)

# 画像アップロードの設定
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# データベースの初期化
def init_db():
    conn = mysql.connector.connect(
        host=os.environ.get('DATABASE_HOST', 'db'),
        port='3306',
        user=os.environ.get('DATABASE_USER', 'root'),
        password=os.environ.get('DATABASE_PASSWORD', 'password'),
        database=os.environ.get('DATABASE_NAME', 'flask_app')
    )
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS articles (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), content TEXT)')
    conn.commit()
    cursor.close()
    conn.close()

time.sleep(10)
init_db()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get('DATABASE_HOST', 'db'),
        port='3306',
        user=os.environ.get('DATABASE_USER', 'root'),
        password=os.environ.get('DATABASE_PASSWORD', 'password'),
        database=os.environ.get('DATABASE_NAME', 'flask_app')
    )
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM articles')
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/new', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/article/<int:article_id>')
def show_article(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, content FROM articles WHERE id = %s', (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    extensions = [
        CodeBlockExtension(),
        'fenced_code',
        'codehilite',
        'nl2br'
    ]
    content_html = markdown.markdown(article[1], extensions=extensions)
    return render_template('article.html', title=article[0], content=content_html)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # ユニークなファイル名を生成
        unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        file_url = url_for('uploaded_file', filename=unique_filename)
        return jsonify({'filePath': file_url})
    return jsonify({'error': 'File not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
