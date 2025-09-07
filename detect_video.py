import os
import cv2
from ultralytics import YOLO
from aws_utils import download_file, upload_file

MODEL_LOCAL = os.getenv('MODEL_LOCAL', 'yolov8n.pt')

def detect_video(local_video_path: str, out_path: str = 'output_detected.mp4', model_path: str = MODEL_LOCAL):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(local_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(local_video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated = results[0].plot()
        out.write(annotated)

    cap.release()
    out.release()
    print('Saved processed video to', out_path)
    return out_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3-key', help='S3 key of video to download and detect')
    parser.add_argument('--local', help='Local video path to run detection on')
    parser.add_argument('--out', default='output_detected.mp4')
    args = parser.parse_args()

    if args.s3_key:
        local_in = 'tmp/input_video.mp4'
        download_file(args.s3_key, local_in)
    else:
        local_in = args.local

    out_file = detect_video(local_in, out_path=args.out)
    upload_file(out_file, 'processed/' + os.path.basename(out_file))
