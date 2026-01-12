import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Pose once (important for performance)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5
)

# Only the landmarks we actually need
REQUIRED_LANDMARKS = {
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "LEFT_HIP",
    "RIGHT_HIP",
    "LEFT_KNEE",
    "RIGHT_KNEE",
    "LEFT_ANKLE",
    "RIGHT_ANKLE"
}

VISIBILITY_THRESHOLD = 0.5


def extract_pose_keypoints(image_path: str):
    """
    Extract minimal pose keypoints required for
    body shape and size estimation.

    Returns:
        {
          "keypoints": { ... },
          "quality": "good" | "poor",
          "warning": optional message
        }
    """

    if not os.path.exists(image_path):
        return None

    image = cv2.imread(image_path)
    if image is None:
        return None

    # Convert BGR → RGB (required by MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return {
            "keypoints": None,
            "quality": "poor",
            "warning": "No human pose detected. Please upload a full-body image."
        }

    keypoints = {}
    low_visibility_points = []

    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        landmark_name = mp_pose.PoseLandmark(idx).name

        if landmark_name in REQUIRED_LANDMARKS:
            if landmark.visibility < VISIBILITY_THRESHOLD:
                low_visibility_points.append(landmark_name)

            keypoints[landmark_name] = {
                "x": round(landmark.x, 4),
                "y": round(landmark.y, 4),
                "visibility": round(landmark.visibility, 4)
            }

    # Decide quality
    if len(low_visibility_points) > 0:
        return {
            "keypoints": keypoints,
            "quality": "poor",
            "warning": (
                "Low visibility detected for: "
                + ", ".join(low_visibility_points)
                + ". Please retake the photo with better lighting and full body visible."
            )
        }

    return {
        "keypoints": keypoints,
        "quality": "good"
    }

