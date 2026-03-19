import torch
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_cifar10, get_dataset_info
from model import SimpleCNN
from training import TrainingConfig, train_model, plot_training_curves, load_history

# Load data
print("Loading CIFAR10 dataset...")
train_loader, val_loader, test_loader, classes = load_cifar10()

# Print info
get_dataset_info()

# Get a batch and visualize
print("\nLoading first batch...")
images, labels = next(iter(train_loader))

print(f"Batch shape: {images.shape}")
print(f"Labels in batch: {labels}")
print(f"Classes: {classes}")

# Denormalize for visualization
images_viz = images * 0.5 + 0.5

# Plot first 4 images
fig, axes = plt.subplots(2, 2, figsize=(8, 8))
for i in range(4):
    img = images_viz[i].permute(1, 2, 0).numpy()
    axes[i//2, i%2].imshow(img)
    axes[i//2, i%2].set_title(f"Class: {classes[labels[i]]}")
    axes[i//2, i%2].axis('off')

plt.tight_layout()
plt.savefig('sample_images.png')
print("Sample images saved to 'sample_images.png'")

# Test the model
print("\n" + "="*50)
print("Testing SimpleCNN Model")
print("="*50)

# Create model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model = SimpleCNN()
model = model.to(device)

# Print model architecture
print("\nModel Architecture:")
print(model)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\nTotal parameters: {total_params:,}")
print(f"Trainable parameters: {trainable_params:,}")

# Test forward pass with a batch
print("\nTesting forward pass...")
images_batch = images.to(device)
with torch.no_grad():
    output = model(images_batch)

print(f"Input shape: {images_batch.shape}")
print(f"Output shape: {output.shape}")
print(f"Output (logits) sample: {output[0]}")

# Get predicted classes
predictions = torch.argmax(output, dim=1)
print(f"\nPredicted classes for first batch: {predictions[:8]}")
print(f"Actual classes for first batch: {labels[:8]}")

print("\n[OK] Model test successful!")

# ============================================================
# TRAINING PHASE
# ============================================================
print("\n" + "="*50)
print("TRAINING MODEL")
print("="*50)

# Setup training configuration
config = TrainingConfig(checkpoint_name="iteration3_model")
print(f"Device: {config.device}")
print(f"Learning rate: {config.learning_rate}")
print(f"Num epochs: {config.num_epochs}")
print(f"Patience: {config.patience}")

# Reset model and move to device
model = SimpleCNN()
model = model.to(config.device)

# Train the model
print("\nStarting training...")
model, history = train_model(model, train_loader, val_loader, config)

# Plot training curves
print("\nPlotting training curves...")
plot_training_curves(history, save_path="checkpoints/iteration3_training_curves.png")

# Display final metrics
print("\n" + "="*50)
print("TRAINING SUMMARY")
print("="*50)
print(f"Final training loss: {history['train_loss'][-1]:.4f}")
print(f"Final validation loss: {history['val_loss'][-1]:.4f}")
print(f"Best validation accuracy: {max(history['val_accuracy']):.2f}%")
print(f"Final validation accuracy: {history['val_accuracy'][-1]:.2f}%")
print("="*50)

