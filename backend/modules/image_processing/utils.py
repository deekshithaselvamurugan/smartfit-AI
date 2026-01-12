import cv2
import mediapipe as mp


mp_pose = mp.solutions.pose


def extract_pose_keypoints(image_path):
    pose = mp_pose.Pose(static_image_mode=True)

    image = cv2.imread(image_path)
    if image is None:
        return None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return None

    keypoints = {}

    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        keypoints[mp_pose.PoseLandmark(idx).name] = {
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z,
            "visibility": landmark.visibility
        }

    return keypoints
