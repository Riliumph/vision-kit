from pathlib import Path
from urllib.request import urlopen, urlretrieve

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

IMAGE_URL = "https://ultralytics.com/images/bus.jpg"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/latest/"
    "pose_landmarker_lite.task"
)


def ensure_model() -> str:
    model_path = Path(__file__).parent / "pose_landmarker_lite.task"

    if not model_path.exists():
        print("モデルをダウンロードします...")
        urlretrieve(MODEL_URL, str(model_path))
        print("ダウンロード完了")

    return str(model_path)


def main():
    model_path = ensure_model()

    print("画像ダウンロード中...")

    image_bytes = urlopen(IMAGE_URL).read()

    img = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8),
        cv2.IMREAD_COLOR,
    )

    if img is None:
        raise RuntimeError("画像の読み込みに失敗しました")

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb,
    )

    base_options = python.BaseOptions(
        model_asset_path=model_path,
    )

    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_poses=10,
    )

    print("姿勢推定実行中...")

    with vision.PoseLandmarker.create_from_options(options) as detector:
        result = detector.detect(mp_image)

    print(f"検出人数: {len(result.pose_landmarks)}")

    h, w = img.shape[:2]

    for pose in result.pose_landmarks:
        for landmark in pose:
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(
                img,
                (x, y),
                3,
                (0, 255, 0),
                -1,
            )

    output = Path("result.jpg")

    cv2.imwrite(str(output), img)

    print(f"保存完了: {output.resolve()}")


if __name__ == "__main__":
    main()
