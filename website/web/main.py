import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory, request, jsonify

from performRecognition import DigitDetection

app = Flask(__name__,
            template_folder='./templates')


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/getMatrix', methods=['POST'])
def get_matrix():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    digit_recogn = DigitDetection("digits_cls2.pkl")
    res, bytes = digit_recogn.get_rectangles(im, False)

    return jsonify({"digits": res})


#
# @app.route('/matrix_detection')
# def main(request):
#     print(request.json)
#
#
#     # return render_template("index.html")
#

#
# @app.route('/', methods=['POST'])
# def create_pet():
#     pass


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
