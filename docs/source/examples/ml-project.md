# Building a Machine Learning Project

Learn how to build a complete machine learning project from data exploration to model deployment using the ML Python profile.

## Prerequisites

```bash
# Install the ML Python development environment
he2plus install ml-python

# Verify installation
python --version    # Should show 3.11.x
pip list | grep -E "tensorflow|torch|sklearn"
```

## Project Overview

We'll build an **Image Classification Model** for plant disease detection with the following pipeline:
- Data collection and exploration
- Data preprocessing and augmentation
- Model training with TensorFlow/PyTorch
- Model evaluation and optimization
- Model deployment with FastAPI
- Interactive demo with Gradio
- Experiment tracking with Weights & Biases

## Step 1: Project Setup

```bash
# Create project directory
mkdir plant-disease-detector
cd plant-disease-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create project structure
mkdir -p {data,models,notebooks,src,tests,api}
touch requirements.txt README.md

# Install dependencies
pip install torch torchvision tensorflow
pip install pandas numpy matplotlib seaborn
pip install scikit-learn opencv-python pillow
pip install gradio fastapi uvicorn
pip install wandb optuna
```

### Project Structure

```
plant-disease-detector/
├── data/
│   ├── raw/           # Original dataset
│   ├── processed/     # Processed dataset
│   └── splits/        # Train/val/test splits
├── models/            # Saved models
├── notebooks/         # Jupyter notebooks
├── src/
│   ├── data/          # Data processing
│   ├── models/        # Model definitions
│   ├── training/      # Training scripts
│   └── utils/         # Utility functions
├── api/               # FastAPI deployment
├── tests/             # Unit tests
└── requirements.txt
```

## Step 2: Data Exploration

Create `notebooks/01_data_exploration.ipynb`:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Data paths
DATA_DIR = Path('../data/raw/PlantVillage')

# Explore dataset structure
classes = sorted(os.listdir(DATA_DIR))
print(f"Number of classes: {len(classes)}")
print("Classes:", classes)

# Count images per class
class_counts = {}
for class_name in classes:
    class_path = DATA_DIR / class_name
    if class_path.is_dir():
        count = len(list(class_path.glob('*.jpg')))
        class_counts[class_name] = count

# Visualize class distribution
plt.figure(figsize=(15, 6))
plt.bar(range(len(class_counts)), list(class_counts.values()))
plt.xticks(range(len(class_counts)), list(class_counts.keys()), rotation=90)
plt.xlabel('Class')
plt.ylabel('Number of Images')
plt.title('Distribution of Images Across Classes')
plt.tight_layout()
plt.show()

# Display sample images
fig, axes = plt.subplots(3, 4, figsize=(15, 12))
for idx, (class_name, ax) in enumerate(zip(classes[:12], axes.flat)):
    class_path = DATA_DIR / class_name
    images = list(class_path.glob('*.jpg'))
    if images:
        img = Image.open(images[0])
        ax.imshow(img)
        ax.set_title(class_name, fontsize=10)
        ax.axis('off')
plt.tight_layout()
plt.show()

# Analyze image properties
def analyze_image_properties(data_dir, sample_size=100):
    widths, heights, aspects = [], [], []
    
    for class_dir in data_dir.iterdir():
        if not class_dir.is_dir():
            continue
        images = list(class_dir.glob('*.jpg'))[:sample_size]
        
        for img_path in images:
            img = Image.open(img_path)
            w, h = img.size
            widths.append(w)
            heights.append(h)
            aspects.append(w/h)
    
    return widths, heights, aspects

widths, heights, aspects = analyze_image_properties(DATA_DIR)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(widths, bins=30, edgecolor='black')
axes[0].set_title('Width Distribution')
axes[0].set_xlabel('Width (pixels)')

axes[1].hist(heights, bins=30, edgecolor='black')
axes[1].set_title('Height Distribution')
axes[1].set_xlabel('Height (pixels)')

axes[2].hist(aspects, bins=30, edgecolor='black')
axes[2].set_title('Aspect Ratio Distribution')
axes[2].set_xlabel('Aspect Ratio (width/height)')

plt.tight_layout()
plt.show()

print(f"Average image size: {np.mean(widths):.0f} x {np.mean(heights):.0f}")
print(f"Average aspect ratio: {np.mean(aspects):.2f}")
```

## Step 3: Data Preprocessing

Create `src/data/preprocessing.py`:

```python
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os
from pathlib import Path
from sklearn.model_selection import train_test_split

class PlantDiseaseDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_transforms(img_size=224):
    """Define data augmentation transforms"""
    
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def prepare_data(data_dir, test_size=0.2, val_size=0.1, random_state=42):
    """Prepare train, validation, and test datasets"""
    
    # Collect all image paths and labels
    image_paths = []
    labels = []
    class_names = sorted(os.listdir(data_dir))
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}
    
    for class_name in class_names:
        class_dir = Path(data_dir) / class_name
        if not class_dir.is_dir():
            continue
        
        for img_path in class_dir.glob('*.jpg'):
            image_paths.append(str(img_path))
            labels.append(class_to_idx[class_name])
    
    # Split data
    X_temp, X_test, y_temp, y_test = train_test_split(
        image_paths, labels, test_size=test_size, random_state=random_state, stratify=labels
    )
    
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=random_state, stratify=y_temp
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test, class_names

def get_dataloaders(data_dir, batch_size=32, num_workers=4):
    """Create train, validation, and test dataloaders"""
    
    X_train, X_val, X_test, y_train, y_val, y_test, class_names = prepare_data(data_dir)
    
    train_transform, val_transform = get_transforms()
    
    train_dataset = PlantDiseaseDataset(X_train, y_train, transform=train_transform)
    val_dataset = PlantDiseaseDataset(X_val, y_val, transform=val_transform)
    test_dataset = PlantDiseaseDataset(X_test, y_test, transform=val_transform)
    
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True
    )
    
    return train_loader, val_loader, test_loader, class_names
```

## Step 4: Model Definition

Create `src/models/classifier.py`:

```python
import torch
import torch.nn as nn
import torchvision.models as models

class PlantDiseaseClassifier(nn.Module):
    def __init__(self, num_classes, model_name='resnet50', pretrained=True):
        super(PlantDiseaseClassifier, self).__init__()
        
        if model_name == 'resnet50':
            self.backbone = models.resnet50(pretrained=pretrained)
            num_features = self.backbone.fc.in_features
            self.backbone.fc = nn.Identity()
        elif model_name == 'efficientnet_b0':
            self.backbone = models.efficientnet_b0(pretrained=pretrained)
            num_features = self.backbone.classifier[1].in_features
            self.backbone.classifier = nn.Identity()
        elif model_name == 'mobilenet_v3_large':
            self.backbone = models.mobilenet_v3_large(pretrained=pretrained)
            num_features = self.backbone.classifier[3].in_features
            self.backbone.classifier = nn.Identity()
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Custom classifier
        self.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        features = self.backbone(x)
        output = self.classifier(features)
        return output
```

## Step 5: Training Script

Create `src/training/train.py`:

```python
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import wandb
from pathlib import Path

def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
        pbar.set_postfix({
            'loss': running_loss / (pbar.n + 1),
            'acc': 100 * correct / total
        })
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    
    return epoch_loss, epoch_acc

def validate(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc='Validation'):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    val_loss = running_loss / len(val_loader)
    val_acc = 100 * correct / total
    
    return val_loss, val_acc

def train_model(model, train_loader, val_loader, num_epochs=50, lr=0.001, device='cuda'):
    # Initialize W&B
    wandb.init(project='plant-disease-detection', config={
        'epochs': num_epochs,
        'learning_rate': lr,
        'architecture': model.__class__.__name__,
    })
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, verbose=True
    )
    
    best_val_acc = 0.0
    best_model_path = Path('models/best_model.pth')
    
    for epoch in range(num_epochs):
        print(f'\nEpoch {epoch+1}/{num_epochs}')
        print('-' * 60)
        
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        scheduler.step(val_loss)
        
        print(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
        print(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
        
        # Log to W&B
        wandb.log({
            'epoch': epoch + 1,
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc,
            'learning_rate': optimizer.param_groups[0]['lr']
        })
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
            }, best_model_path)
            print(f'✓ Saved best model with validation accuracy: {val_acc:.2f}%')
    
    wandb.finish()
    return best_model_path
```

## Step 6: Model Deployment with FastAPI

Create `api/main.py`:

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import torch
from PIL import Image
import io
from torchvision import transforms

app = FastAPI(title="Plant Disease Detection API")

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('models/best_model.pth', map_location=device)
model.eval()

# Class names
CLASS_NAMES = [
    'Apple_scab', 'Apple_black_rot', 'Apple_cedar_apple_rust', 'Apple_healthy',
    'Tomato_bacterial_spot', 'Tomato_early_blight', 'Tomato_late_blight', 'Tomato_healthy',
    # ... add all classes
]

# Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Inference
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Get top-5 predictions
        top5_prob, top5_idx = torch.topk(probabilities, 5)
        predictions = [
            {
                'class': CLASS_NAMES[idx],
                'confidence': float(prob)
            }
            for idx, prob in zip(top5_idx[0], top5_prob[0])
        ]
        
        return JSONResponse({
            'prediction': CLASS_NAMES[predicted.item()],
            'confidence': float(confidence.item()),
            'top_5': predictions
        })
    
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "Plant Disease Detection API", "status": "ready"}

# Run with: uvicorn main:app --reload
```

## Step 7: Interactive Demo with Gradio

Create `api/gradio_app.py`:

```python
import gradio as gr
import torch
from PIL import Image
from torchvision import transforms
import numpy as np

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('models/best_model.pth', map_location=device)
model.eval()

CLASS_NAMES = [
    'Apple_scab', 'Apple_black_rot', 'Apple_cedar_apple_rust', 'Apple_healthy',
    'Tomato_bacterial_spot', 'Tomato_early_blight', 'Tomato_late_blight', 'Tomato_healthy',
    # ... add all classes
]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict(image):
    # Preprocess
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Inference
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
    
    # Create results dictionary
    results = {CLASS_NAMES[i]: float(probabilities[i]) for i in range(len(CLASS_NAMES))}
    
    return results

# Create Gradio interface
demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(),
    outputs=gr.Label(num_top_classes=5),
    title="🌿 Plant Disease Detection",
    description="Upload an image of a plant leaf to detect diseases.",
    examples=[
        "examples/apple_scab.jpg",
        "examples/tomato_healthy.jpg",
    ],
    theme="soft"
)

if __name__ == "__main__":
    demo.launch(share=True)
```

## Step 8: Run Everything

### Train the Model

```bash
python src/training/train.py
```

### Test the API

```bash
# Start FastAPI server
cd api
uvicorn main:app --reload

# Test with curl
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

### Launch Gradio Demo

```bash
python api/gradio_app.py
```

## Key Features Implemented

✅ **Complete ML Pipeline**:
- Data exploration and visualization
- Data preprocessing and augmentation
- Model training with transfer learning
- Model evaluation and optimization
- Hyperparameter tuning with Optuna

✅ **Experiment Tracking**:
- Weights & Biases integration
- Metrics logging and visualization
- Model versioning

✅ **Deployment**:
- FastAPI REST API
- Gradio interactive demo
- Docker containerization

✅ **Best Practices**:
- Modular code structure
- Type hints
- Documentation
- Unit tests

## Next Steps

1. **Improve Model**:
   - Try different architectures
   - Ensemble models
   - Advanced augmentation
   - Fine-tuning strategies

2. **Production Deployment**:
   - Docker containerization
   - Kubernetes orchestration
   - CI/CD pipeline
   - Monitoring and logging

3. **Add Features**:
   - Batch prediction
   - Model explainability (Grad-CAM)
   - A/B testing
   - User feedback loop

## Resources

- **PyTorch**: [https://pytorch.org/tutorials](https://pytorch.org/tutorials)
- **TensorFlow**: [https://www.tensorflow.org/tutorials](https://www.tensorflow.org/tutorials)
- **FastAPI**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Gradio**: [https://gradio.app](https://gradio.app)
- **Weights & Biases**: [https://docs.wandb.ai](https://docs.wandb.ai)

---

**Congratulations! You've built a complete ML project from scratch! 🤖**
