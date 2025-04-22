from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Use a static key for demo; in real apps, use password-derived key
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        action = request.form['action']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            data = f.read()

        if action == 'encrypt':
            processed = cipher.encrypt(data)
            out_filename = file.filename + '.enc'
        else:
            processed = cipher.decrypt(data)
            out_filename = file.filename.replace('.enc', '')

        out_path = os.path.join(UPLOAD_FOLDER, out_filename)
        with open(out_path, 'wb') as f:
            f.write(processed)

        return send_file(out_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
 