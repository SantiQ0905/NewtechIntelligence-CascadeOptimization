class YOLOv8_openVINO:
    def __init__(self, device):
        from pathlib import Path
        from ultralytics import YOLO
        import torch
        import openvino as ov

        models_dir = Path("")
        models_dir.mkdir(exist_ok=True)

        DET_MODEL_NAME = "yolov8s"
        self.det_model = YOLO(models_dir / f"{DET_MODEL_NAME}.pt")
        res = self.det_model()
        det_model_path = models_dir / f"{DET_MODEL_NAME}_openvino_model/{DET_MODEL_NAME}.xml"

        # openVINO
        core = ov.Core()

        det_ov_model = core.read_model(det_model_path)
        ov_config = {}

        compiled_model = core.compile_model(det_ov_model, device, ov_config)

        def infer(*args):
            result = compiled_model(args)
            return torch.from_numpy(result[0])

        # Use openVINO as inference engine
        self.det_model.predictor.inference = infer
        self.det_model.predictor.model.pt = False

        self.classes_to_count = [0]

    def inference(self, frame):
        import cv2

        result = self.det_model(frame, classes=self.classes_to_count)

        detections = result[0].boxes
        result = result[0].plot()
        result_brg = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

        status = len(detections) > 0
        return result_brg, status
