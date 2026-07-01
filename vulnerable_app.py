from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 1. SQL INJECTION HEDEFİ
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'S3cr3t!')")
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cursor.execute(query)
        if cursor.fetchone():
            return {"status": "success", "flag": "FLAG{SQL_INJECTION_OTONOM_BASARI}"}
        return {"status": "failed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. XSS (KOD ENJEKSİYONU) HEDEFİ
@app.route('/search', methods=['GET'])
def search():
    # Girdi temizlenmeden doğrudan HTML içine basılıyor (XSS Açığı)
    q = request.args.get('q', '')
    template = f"<h1>Arama Sonuclari</h1><p>Aranan Kelime: {q}</p>"
    if "<script>" in q:
        return render_template_string(template + "<div id='flag'>FLAG{XSS_OTONOM_BASARI}</div>")
    return render_template_string(template)

# 3. TEHLİKELİ DOSYA YÜKLEME HEDEFİ
@app.route('/upload', methods=['POST'])
def upload():
    # Dosya uzantısı kontrol edilmiyor (Dangerous File Upload Açığı)
    file = request.files.get('file')
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        if file.filename.endswith('.php') or file.filename.endswith('.sh'):
            return {"status": "uploaded", "flag": "FLAG{FILE_UPLOAD_OTONOM_BASARI}"}
        return {"status": "success", "message": "Dosya yuklendi"}
    return {"status": "failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
