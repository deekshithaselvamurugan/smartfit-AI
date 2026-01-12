import os
import uuid

TEMP_UPLOAD_DIR = "backend/temp_uploads"


def save_temp_image(image_file):
    # Ensure temp folder exists
    if not os.path.exists(TEMP_UPLOAD_DIR):
        os.makedirs(TEMP_UPLOAD_DIR)

    # Create unique filename
    filename = f"{uuid.uuid4()}_{image_file.filename}"
    file_path = os.path.join(TEMP_UPLOAD_DIR, filename)

    # Save image
    image_file.save(file_path)

    return file_path

def delete_temp_image(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)