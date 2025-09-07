import os
import cv2
from ultralytics import YOLO
from aws_utils import download_file, upload_file

MODEL_LOCAL = os.getenv('MODEL_LOCAL', 'yolov8n.pt')

def detect_image(local_image_path: str, out_path: str = 'out.jpg', model_path: str = MODEL_LOCAL):
    model = YOLO(model_path)
    img = cv2.imread(local_image_path)
    if img is None:
        raise FileNotFoundError(local_image_path)
    results = model(img)
    annotated = results[0].plot()
    cv2.imwrite(out_path, annotated)
    print('Saved annotated image to', out_path)
    return out_path

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3-key', help='S3 key of image to download and detect')
    parser.add_argument('--local', help='Local image path to run detection on')
    parser.add_argument('--out', default='output_image.jpg')
    args = parser.parse_args()

    if args.s3_key:
        local_in = 'tmp/input_image.jpg'
        download_file(args.s3_key, local_in)
    else:
        local_in = args.local

    out_file = detect_image(local_in, out_path=args.out)
    upload_file(out_file, 'processed/' + os.path.basename(out_file))
