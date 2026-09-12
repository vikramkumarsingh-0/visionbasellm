try:  # Optional heavy dependency: the agent runs DOM-only without it.
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception:  # pragma: no cover - optional install
    YOLO = None
    YOLO_AVAILABLE = False

import cv2
from pathlib import Path
from typing import List, Dict
from loguru import logger
from config import settings
from core.security import SecurityValidator

class VisionDetector:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or settings.models_dir / f"yolo_{settings.model_version}.pt"
        self.model = self._load_model()
        
    def _load_model(self):
        if not YOLO_AVAILABLE:
            logger.warning("ultralytics/torch not installed - running DOM-only perception")
            return None
        if self.model_path.exists():
            # Verify model integrity before loading
            try:
                SecurityValidator.verify_model_integrity(self.model_path)
                logger.info(f"Loading verified model from {self.model_path}")
                return YOLO(str(self.model_path))
            except (ValueError, FileNotFoundError) as e:
                logger.error(f"Model verification failed: {e}")
                logger.info("Falling back to base model")
        
        logger.info("Initializing new YOLOv8 model")
        base_model = Path('yolov8n.pt')
        if base_model.exists():
            SecurityValidator.verify_model_integrity(base_model)
        return YOLO('yolov8n.pt')
    
    def detect_elements(self, image_path: str, conf_threshold: float = 0.25) -> List[Dict]:
        try:
            results = self.model(image_path, conf=conf_threshold)[0]
        except Exception as e:
            logger.warning(f"YOLO detection unavailable, continuing with DOM-only perception: {e}")
            return []
        detections = []
        
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            
            detections.append({
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'confidence': conf,
                'class': cls,
                'class_name': results.names[cls],
                'center': [int((x1 + x2) / 2), int((y1 + y2) / 2)]
            })
        
        return detections
    
    def train(self, data_yaml: str, epochs: int = 50, batch: int = 16):
        # Limit training parameters to prevent resource exhaustion
        epochs = min(epochs, 100)
        batch = min(batch, 32)
        
        logger.info(f"Starting training for {epochs} epochs")
        results = self.model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch,
            imgsz=640,
            device='cuda' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu'
        )
        
        # Backup old model before saving new one
        new_model_path = settings.models_dir / f"yolo_{settings.model_version}_trained.pt"
        if new_model_path.exists():
            backup_path = settings.models_dir / f"yolo_{settings.model_version}_backup.pt"
            new_model_path.rename(backup_path)
            logger.info(f"Backed up old model to {backup_path}")
        
        self.model.save(str(new_model_path))
        # Compute and store hash for new model
        SecurityValidator.verify_model_integrity(new_model_path)
        logger.info(f"Model saved and verified: {new_model_path}")
        return results
