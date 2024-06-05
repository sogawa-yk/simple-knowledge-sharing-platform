from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import sqlite3
import markdown
import os
from werkzeug.utils import secure_filename
from custom_markdown import CodeBlockExtension

app = Flask(__name__)

# 画像アップロードの設定
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# データベースの初期化
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, title TEXT, content TEXT)')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
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
        cursor.execute('INSERT INTO articles (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('new.html')

@app.route('/article/<int:article_id>')
def show_article(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, content FROM articles WHERE id = ?', (article_id,))
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
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        file_url = url_for('uploaded_file', filename=filename)
        return jsonify({'filePath': file_url})
    return jsonify({'error': 'File not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
