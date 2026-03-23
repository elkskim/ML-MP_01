# Google Colab Training Guide

## Quick Start

### 1. Upload Notebook to Colab
- Go to https://colab.research.google.com/
- Click "Upload" tab
- Select `colab_training.ipynb` from your project folder

### 2. Run the Notebook
- Execute cells in order (use Shift+Enter or play button)
- GPU will automatically be available
- Training runs much faster than locally!

### 3. Adjust Hyperparameters
Before training, edit the **Configuration** cell:
```python
NUM_EPOCHS = 50
LEARNING_RATE = 0.001
BATCH_SIZE = 32
PATIENCE = 10
CHECKPOINT_NAME = "experiment_v1"  # Change for each run
```

### 4. Download Results
After training completes, use the **Download Results** cell to get:
- `experiment_v1.pt` - Model weights
- `experiment_v1_history.json` - Training metrics
- `experiment_v1_curves.png` - Loss/accuracy plots

Move these to your local `checkpoints/` folder.

---

## Workflow for Iteration 5 (Fine-tuning)

### Experiment 1: Baseline
```python
CHECKPOINT_NAME = "v1_baseline"
NUM_EPOCHS = 50
LEARNING_RATE = 0.001
PATIENCE = 10
```

### Experiment 2: Higher Learning Rate
```python
CHECKPOINT_NAME = "v2_higher_lr"
NUM_EPOCHS = 50
LEARNING_RATE = 0.005
PATIENCE = 10
```

### Experiment 3: Lower Learning Rate
```python
CHECKPOINT_NAME = "v3_lower_lr"
NUM_EPOCHS = 50
LEARNING_RATE = 0.0001
PATIENCE = 10
```

Do the same for batch sizes, patience, etc.

**Track results**: Keep a spreadsheet of which experiment gave the best accuracy!

---

## Optional: Google Drive Auto-Sync

Uncomment the last cell to automatically save all results to Google Drive:
```python
# Uncomment to enable Google Drive auto-sync
from google.colab import drive
drive.mount('/content/drive')

!mkdir -p /content/drive/MyDrive/ML-MP_01-Results
!cp -r checkpoints/* /content/drive/MyDrive/ML-MP_01-Results/
```

This way results backup automatically without manual downloads.

---

## Notes

- **GPU Speed**: ~10-20x faster than CPU
- **Runtime Limit**: ~12 hours per day (auto-resets)
- **Free Tier**: Includes T4 GPU (plenty for CIFAR10)
- **Pro Tip**: Start with small num_epochs to test, then increase

---

## After Training: Iteration 4 (Local Evaluation)

Once you download a checkpoint:
1. Move it to your local `checkpoints/` folder
2. Run iteration 4 to evaluate on the test set
3. Use the best checkpoint for final evaluation

Example loading in local code:
```python
from training import load_checkpoint
from model import SimpleCNN

device = torch.device("cpu")
model = SimpleCNN().to(device)
model = load_checkpoint(model, "checkpoints/v1_baseline.pt", device)
# Now evaluate on test set
```

