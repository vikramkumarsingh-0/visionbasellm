from pathlib import Path
from typing import List, Dict
import yaml
import shutil
from loguru import logger
from config import settings
from core.vision_detector import VisionDetector
from core.security import SecurityValidator

class TrainingPipeline:
    def __init__(self):
        self.train_dir = settings.data_dir / "train"
        self.val_dir = settings.data_dir / "val"
        self.train_dir.mkdir(exist_ok=True)
        self.val_dir.mkdir(exist_ok=True)
    
    def prepare_dataset(self, failed_actions: List[Dict]):
        logger.info(f"Preparing dataset from {len(failed_actions)} failed actions")
        
        validated_count = 0
        for idx, action in enumerate(failed_actions):
            if 'screenshot' in action:
                img_path = Path(action['screenshot'])
                if img_path.exists():
                    try:
                        # Validate training data before adding
                        visual_elements = action.get('visual_elements', [])
                        bboxes = [el['bbox'] for el in visual_elements if 'bbox' in el]
                        SecurityValidator.validate_training_data(img_path, bboxes)
                        
                        dest = self.train_dir / f"fail_{idx}.png"
                        shutil.copy(img_path, dest)
                        
                        label_path = self.train_dir / f"fail_{idx}.txt"
                        self._create_yolo_label(action, label_path)
                        validated_count += 1
                    except ValueError as e:
                        logger.warning(f"Skipping invalid training sample {idx}: {e}")
        
        logger.info(f"Validated {validated_count}/{len(failed_actions)} training samples")
    
    def _create_yolo_label(self, action: Dict, label_path: Path):
        if 'visual_elements' in action:
            with open(label_path, 'w') as f:
                for el in action['visual_elements']:
                    bbox = el['bbox']
                    cls = el['class']
                    x_center = (bbox[0] + bbox[2]) / 2 / 640
                    y_center = (bbox[1] + bbox[3]) / 2 / 640
                    width = (bbox[2] - bbox[0]) / 640
                    height = (bbox[3] - bbox[1]) / 640
                    f.write(f"{cls} {x_center} {y_center} {width} {height}\n")
    
    def create_data_yaml(self) -> str:
        data_yaml = {
            'path': str(settings.data_dir),
            'train': 'train',
            'val': 'val',
            'names': {
                0: 'button',
                1: 'input',
                2: 'link',
                3: 'form'
            }
        }
        
        yaml_path = settings.data_dir / "data.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(data_yaml, f)
        
        return str(yaml_path)
    
    def retrain_model(self, failed_actions: List[Dict], epochs: int = 30):
        logger.info("Starting retraining pipeline")
        
        # Limit training samples to prevent data poisoning
        max_samples = 100
        if len(failed_actions) > max_samples:
            logger.warning(f"Limiting training to {max_samples} samples")
            failed_actions = failed_actions[:max_samples]
        
        self.prepare_dataset(failed_actions)
        data_yaml = self.create_data_yaml()
        
        detector = VisionDetector()
        results = detector.train(data_yaml, epochs=epochs, batch=8)
        
        logger.info("Retraining completed")
        return results
