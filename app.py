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

# ================================
# Core API
# ================================


@app.get("/db")
def db():
    return jsonify(success_res(ps.get_db()))


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

# ================================
# Scene API
# ================================


@app.post("/scene/<scene_id>")
def run_scene(scene_id):
    try:
        result = scene_controller.run_scene(scene_id)
        return jsonify(success_res(result))
    except Exception as e:
        return jsonify(error_res(str(e))), 500


# ================================
# SESSIONS API
# ================================

@app.get("/sessions/current")
def sessions_current():
    return jsonify(success_res(ps.get_current_sessions()))


@app.get("/sessions/past")
def sessions_past():
    return jsonify(success_res(ps.get_past_sessions()))


@app.get("/sessions/plate/<plate>")
def sessions_plate_all(plate):
    return jsonify(success_res(ps.get_sessions_of_plate(plate)))


@app.get("/sessions/plate/<plate>/latest")
def sessions_plate_latest(plate):
    print("hahsaijxjaksnxk")
    return jsonify(success_res(ps.get_last_session_of_plate(plate)))


# ================================
# SECURITY TOGGLE API
# ================================

@app.get("/security/status")
def security_status():
    return jsonify(success_res({"enabled": ps.is_security_enabled()}))


@app.post("/security/enable")
def security_enable():
    ps.enable_security()
    return jsonify(success_res({"enabled": True}))


@app.post("/security/disable")
def security_disable():
    ps.disable_security()
    return jsonify(success_res({"enabled": False}))


@app.post("/security/toggle")
def security_toggle():
    new_value = ps.toggle_security()
    return jsonify(success_res({"enabled": new_value}))


# ================================
# ALLOWED CAR API
# ================================

@app.get("/allowed/list")
def allowed_list():
    return jsonify(success_res(ps.get_allowed_list()))


@app.post("/allowed/add")
def allowed_add():
    data = request.json
    plate = data.get("plate")

    if not plate:
        return jsonify(error_res("Missing plate")), 400

    added = ps.add_allowed(plate)
    return jsonify(success_res({"added": added, "plate": plate}))


@app.post("/allowed/remove")
def allowed_remove():
    data = request.json
    plate = data.get("plate")

    if not plate:
        return jsonify(error_res("Missing plate")), 400

    ps.remove_allowed(plate)
    return jsonify(success_res({"removed": True, "plate": plate}))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
