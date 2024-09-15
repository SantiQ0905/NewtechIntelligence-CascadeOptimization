from pathlib import Path
from ultralytics import YOLO

models_dir = Path("")
models_dir.mkdir(exist_ok=True)

DET_MODEL_NAME = "yolov8s"

det_model = YOLO(models_dir / f"{DET_MODEL_NAME}.pt")
label_map = det_model.model.names

res = det_model()
det_model_path = models_dir / f"{DET_MODEL_NAME}_openvino_model/{DET_MODEL_NAME}.xml"
if not det_model_path.exists():
    det_model.export(format="openvino", dynamic=True, half=True)