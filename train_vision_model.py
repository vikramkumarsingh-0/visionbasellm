from core.vision_detector import VisionDetector
from core.training_pipeline import TrainingPipeline
from pathlib import Path
import shutil
from loguru import logger

logger.add("logs/training.log")

# Create sample training data
train_dir = Path("data/train")
train_dir.mkdir(exist_ok=True)

# Copy sample screenshot for training
screenshots = list(Path("data/screenshots").glob("*.png"))
if screenshots:
    logger.info(f"Found {len(screenshots)} screenshots for training")
    for idx, img in enumerate(screenshots[:5]):
        dest = train_dir / f"sample_{idx}.png"
        shutil.copy(img, dest)
        
        # Create dummy label
        label = train_dir / f"sample_{idx}.txt"
        with open(label, 'w') as f:
            f.write("0 0.5 0.5 0.3 0.2\n")  # button class
    
    pipeline = TrainingPipeline()
    data_yaml = pipeline.create_data_yaml()
    
    logger.info("Starting model training...")
    detector = VisionDetector()
    results = detector.train(data_yaml, epochs=10, batch=4)
    
    logger.info("Training completed!")
else:
    logger.warning("No screenshots found. Run test_simple.py first.")
