"""
Evaluation Script for Colab (Self-Contained)
Add this to the end of your colab_training.ipynb to automatically evaluate the model
"""

# ============================================================
# EVALUATION ON TEST SET
# ============================================================

import torch
from torch import nn
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

print("\n" + "="*60)
print("EVALUATING MODEL ON TEST SET")
print("="*60)

# Load the best model from checkpoint
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)

# Load saved weights
model.load_state_dict(torch.load(config.checkpoint_path, map_location=device))
print(f"[OK] Model loaded from checkpoint: {config.checkpoint_path}")

# Evaluate on test set
model.eval()
all_preds = []
all_labels = []
correct = 0
total = 0
test_loss = 0

criterion = nn.CrossEntropyLoss()

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        test_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
        
        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

test_accuracy = 100 * correct / total
avg_test_loss = test_loss / len(test_loader)

print(f"\nTest Accuracy: {test_accuracy:.2f}%")
print(f"Test Loss: {avg_test_loss:.4f}")
print(f"Correct Predictions: {correct}/{total}")

# Classification report
print("\n" + "-"*60)
print("CLASSIFICATION REPORT")
print("-"*60)
report = classification_report(all_labels, all_preds, target_names=classes)
print(report)

# Confusion matrix visualization
print("\nGenerating confusion matrix...")
cm = confusion_matrix(all_labels, all_preds)

fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)

ax.set_title('Confusion Matrix', fontsize=16, fontweight='bold')
plt.colorbar(im, ax=ax)

tick_marks = range(len(classes))
ax.set_xticks(tick_marks)
ax.set_yticks(tick_marks)
ax.set_xticklabels(classes, rotation=45, ha='right')
ax.set_yticklabels(classes)

ax.set_ylabel('True Label', fontsize=12)
ax.set_xlabel('Predicted Label', fontsize=12)

# Add text annotations
thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], 'd'),
               ha="center", va="center",
               color="white" if cm[i, j] > thresh else "black",
               fontsize=9)

plt.tight_layout()
plt.show()

# Print summary
print("\n" + "="*60)
print("EVALUATION SUMMARY")
print("="*60)
print(f"Test Accuracy: {test_accuracy:.2f}%")
print(f"Test Loss: {avg_test_loss:.4f}")
print(f"Correct: {correct}/{total}")
print(f"\nBest Validation Accuracy: {max(history['val_accuracy']):.2f}%")
print(f"Final Validation Accuracy: {history['val_accuracy'][-1]:.2f}%")
print("="*60)

