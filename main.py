import torch
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_cifar10, get_dataset_info
from model import SimpleCNN

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

print("\n✓ Model test successful!")

