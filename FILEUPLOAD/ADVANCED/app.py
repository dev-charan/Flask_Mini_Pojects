import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set custom upload folder
UPLOAD_FOLDER = os.path.join('FILEUPLOAD','app', 'assets', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Max upload size = 5 MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file types
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename):
    if '.' in filename:
        extension = filename.split('.')[-1].lower()
        return extension in ALLOWED_EXTENSIONS
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files' not in request.files:
            return "No file part"

        files = request.files.getlist('files')
        uploaded = []

        for file in files:
            if file.filename == '':
                continue
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded.append(filename)

        if not uploaded:
            return "❌ No valid files uploaded"

        return render_template('upload_success.html', files=uploaded)

    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=uploaded_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(filepath):
        os.remove(filepath)
        return f"✅ Deleted: {filename} <br><a href='/'>Back</a>"
    return f"❌ File not found: {filename} <br><a href='/'>Back</a>"

@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large (max 5MB)", 413

if __name__ == '__main__':
    app.run(debug=True)
