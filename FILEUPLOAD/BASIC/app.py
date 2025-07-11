import os
from flask import Flask, render_template, request
from flask import send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join('FILEUPLOAD', 'uploads'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename):
    if '.' in filename:
        extension = filename.split('.')[-1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return f"✅ File uploaded: {file.filename}"

        return "❌ File type not allowed"

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    app.run(debug=True)
