import os
from flask import Flask, request, redirect, render_template, jsonify
# from color import color
# from texture import texture
from driver_color import get_similar_images

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
            result = get_similar_images()
        # elif choice == "texture":
        #     result
        return jsonify(result)


# @app.route("/color", methods=["POST"])
# def colorRoute():
#     persentage = color()
#     colorResult = [
#         {"filename": f"data{i+1}", "percentage": number}
#         for i, number in enumerate(persentage)
#     ]
#     colorResult = sorted(
#         [x for x in colorResult if x["percentage"] > 60],
#         key=lambda x: x["percentage"],
#         reverse=True,
#     )
#     return jsonify(colorResult)


# @app.route("/texture", methods=["POST"])
# def textureRoute():
#     if request.method == "POST":
#         persentage = texture()
#         textureResult = [
#             {"filename": f"data{i+1}", "percentage": number}
#             for i, number in enumerate(persentage)
#         ]
#         textureResult = sorted(
#             [x for x in textureResult if x["percentage"] > 60],
#             key=lambda x: x["percentage"],
#             reverse=True,
#         )
#         return jsonify(textureResult)


if __name__ == "__main__":
    app.run(debug=True)