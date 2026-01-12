from flask import Blueprint, request, jsonify
from .services import save_temp_image, delete_temp_image
from .utils import extract_pose_keypoints

image_bp = Blueprint("image_bp", __name__)


@image_bp.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save temporarily
    temp_path = save_temp_image(image)

    # ---- REAL PROCESSING ----
    keypoints = extract_pose_keypoints(temp_path)

    # Delete image immediately
    delete_temp_image(temp_path)

    if keypoints is None:
        return jsonify({
            "message": "No human pose detected",
            "status": "failed"
        }), 400

    return jsonify({
        "status": "processed",
        "keypoints": keypoints
    }), 200

