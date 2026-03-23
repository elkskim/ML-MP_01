"""
Evaluation Script for Colab
Add this to the end of your colab_training.ipynb to automatically evaluate the model
"""

# ============================================================
# EVALUATION ON TEST SET
# ============================================================

from training import evaluate_model, plot_confusion_matrix, load_checkpoint
import torch

print("\n" + "="*60)
print("EVALUATING MODEL ON TEST SET")
print("="*60)

# Load the best model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
model = load_checkpoint(model, config.checkpoint_path, device)

# Evaluate on test set
eval_results = evaluate_model(
    model,
    test_loader,
    device,
    classes=classes,
    save_path=None  # Don't save report in Colab
)

# Generate confusion matrix
print("\nGenerating confusion matrix...")
plot_confusion_matrix(
    eval_results['labels'],
    eval_results['predictions'],
    classes,
    save_path=None  # Don't save in Colab
)

# Print summary
print("\n" + "="*60)
print("EVALUATION SUMMARY")
print("="*60)
print(f"Test Accuracy: {eval_results['test_accuracy']:.2f}%")
print(f"Test Loss: {eval_results['test_loss']:.4f}")
print(f"Correct: {eval_results['correct']}/{eval_results['total']}")
print(f"\nBest Validation Accuracy: {max(history['val_accuracy']):.2f}%")
print(f"Final Validation Accuracy: {history['val_accuracy'][-1]:.2f}%")
print("="*60)

