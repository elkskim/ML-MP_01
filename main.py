import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_cifar10, get_dataset_info

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
images = images * 0.5 + 0.5

# Plot first 4 images
fig, axes = plt.subplots(2, 2, figsize=(8, 8))
for i in range(4):
    img = images[i].permute(1, 2, 0).numpy()
    axes[i//2, i%2].imshow(img)
    axes[i//2, i%2].set_title(f"Class: {classes[labels[i]]}")
    axes[i//2, i%2].axis('off')

plt.tight_layout()
plt.savefig('sample_images.png')
print("Sample images saved to 'sample_images.png'")
