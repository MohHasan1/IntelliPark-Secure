from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2

from ParkingSystem import ParkingSystem
from SceneController import SceneController
from utils.index import successRes as success_res, errorRes as error_res



app = Flask(__name__)
CORS(app)

ps = ParkingSystem()
scene_controller = SceneController()


@app.get("/health")
def health():
    return jsonify(success_res("ok"))


@app.get("/db")
def db():
    return jsonify(success_res(ps.get_db()))


# ENTRY
@app.post("/event/entry")
def entry():
    data = request.json
    path = data.get("image_path")

    if not path:
        return jsonify(error_res("Missing image_path")), 400

    try:
        session = ps.handle_entry(path)
        return jsonify(success_res(session))
    except Exception as e:
        return jsonify(error_res(str(e))), 500


# SCAN
@app.post("/event/scan")
def scan():
    data = request.json
    path = data.get("image_path")

    if not path:
        return jsonify(error_res("Missing image_path")), 400

    img = cv2.imread(path)
    if img is None:
        return jsonify(error_res("Could not load image")), 400

    try:
        summary = ps.scan_parking_lot(img)
        return jsonify(success_res(summary))
    except Exception as e:
        return jsonify(error_res(str(e))), 500


# EXIT
@app.post("/event/exit")
def exit_event():
    data = request.json
    path = data.get("image_path")

    if not path:
        return jsonify(error_res("Missing image_path")), 400

    try:
        session = ps.handle_exit(path)
        return jsonify(success_res(session))
    except Exception as e:
        return jsonify(error_res(str(e))), 500


@app.post("/event/reset")
def reset():
    ps.reset()
    return jsonify(success_res("System reset"))

@app.post("/scene/<scene_id>")
def run_scene(scene_id):
    try:
        result = scene_controller.run_scene(scene_id)
        return jsonify(success_res(result))
    except Exception as e:
        return jsonify(error_res(str(e))), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
