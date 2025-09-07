from ultralytics import YOLO
import os

MODEL_PRETRAINED = os.getenv('MODEL_PRETRAINED', 'yolov8n.pt')
DATA_YAML = os.getenv('DATA_YAML', 'dataset.yaml')
EPOCHS = int(os.getenv('EPOCHS', '50'))
BATCH = int(os.getenv('BATCH', '8'))
IMG_SIZE = int(os.getenv('IMG_SIZE', '640'))
DEVICE = os.getenv('DEVICE', '0')

def train():
    model = YOLO(MODEL_PRETRAINED)
    model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        device=DEVICE
    )

if __name__ == '__main__':
    train()
