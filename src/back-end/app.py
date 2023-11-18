import os
from flask import Flask, request, redirect, render_template, jsonify
from driver_color import get_similar_color
from driver_texture import get_similar_texture
import time

start_time = time.time()
app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER_IMAGE = "database/image"
UPLOAD_FOLDER_DATASET = "database/dataset"
app.config["UPLOAD_FOLDER_IMAGE"] = UPLOAD_FOLDER_IMAGE
app.config["UPLOAD_FOLDER_DATASET"] = UPLOAD_FOLDER_DATASET

if not os.path.exists(UPLOAD_FOLDER_IMAGE):
    os.makedirs(UPLOAD_FOLDER_IMAGE)
if not os.path.exists(UPLOAD_FOLDER_DATASET):
    os.makedirs(UPLOAD_FOLDER_DATASET)


def clearFolder(folder_path):
    files = os.listdir(folder_path)

    for file in files:
        os.remove(os.path.join(folder_path, file))
    

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    if request.files:
        clearFolder(app.config["UPLOAD_FOLDER_IMAGE"])
        clearFolder(app.config["UPLOAD_FOLDER_DATASET"])
        image = request.files["image"]
        dataset = request.files.getlist("dataset")
        choice = request.form["choice"]
        filename = "image.jpg"
        image.save(os.path.join(app.config["UPLOAD_FOLDER_IMAGE"], filename))
        i = 1
        for file in dataset:
            file.save(os.path.join(app.config["UPLOAD_FOLDER_DATASET"], f"data{i}.jpg"))
            i += 1
        if choice == "color":
            result = get_similar_color()
        elif choice == "texture":
            result = get_similar_texture()
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

end_time = time.time()
execution_time = end_time - start_time
print("Waktu eksekusi:", execution_time, "detik")