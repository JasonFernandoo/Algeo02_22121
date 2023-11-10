from flask import Flask, request
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img

# Tentukan folder tujuan untuk menyimpan file yang diunggah
app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/user_file_input'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    pic = request.files['pic']

    if not pic:
        return "No file uploaded", 400
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()

    return "File uploaded successfully", 200

if __name__ == '__main__':
    app.run()
