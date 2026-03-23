"""
Comprehensive evaluation script for the trained CNN model.
Loads the best trained model and evaluates it on the test set.
Generates detailed metrics and visualizations.
"""

import torch
import os
from data_loader import load_cifar10
from model import SimpleCNN
from training import load_checkpoint, evaluate_model, plot_confusion_matrix, load_history

def main():
    # Configuration
    CHECKPOINT_PATH = "checkpoints/colab_experiment_v1.pt"
    HISTORY_PATH = "checkpoints/colab_experiment_v1_history.json"
    EVAL_REPORT_PATH = "checkpoints/evaluation_report.txt"
    CONFUSION_MATRIX_PATH = "checkpoints/confusion_matrix.png"
    
    # Check if checkpoint exists
    if not os.path.exists(CHECKPOINT_PATH):
        print(f"ERROR: Checkpoint not found at {CHECKPOINT_PATH}")
        print("Please train a model first using main.py")
        return
    
    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load data
    print("\nLoading CIFAR10 dataset...")
    train_loader, val_loader, test_loader, classes = load_cifar10()
    print(f"Classes: {classes}")
    
    # Load model
    print("\nLoading model...")
    model = SimpleCNN().to(device)
    model = load_checkpoint(model, CHECKPOINT_PATH, device)
    
    # Load training history
    print("\nLoading training history...")
    history = load_history(HISTORY_PATH)
    print(f"Training completed in {len(history['train_loss'])} epochs")
    print(f"Best validation accuracy: {max(history['val_accuracy']):.2f}%")
    
    # Evaluate on test set
    print("\n" + "="*60)
    print("EVALUATING ON TEST SET")
    print("="*60)
    
    eval_results = evaluate_model(
        model, 
        test_loader, 
        device, 
        classes=classes,
        save_path=EVAL_REPORT_PATH
    )
    
    # Generate confusion matrix
    print("\nGenerating confusion matrix...")
    plot_confusion_matrix(
        eval_results['labels'],
        eval_results['predictions'],
        classes,
        save_path=CONFUSION_MATRIX_PATH
    )
    
    # Print summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Test Accuracy: {eval_results['test_accuracy']:.2f}%")
    print(f"Test Loss: {eval_results['test_loss']:.4f}")
    print(f"Validation Accuracy (best): {max(history['val_accuracy']):.2f}%")
    print(f"Validation Accuracy (final): {history['val_accuracy'][-1]:.2f}%")
    print(f"\nResults saved to:")
    print(f"  - Evaluation report: {EVAL_REPORT_PATH}")
    print(f"  - Confusion matrix: {CONFUSION_MATRIX_PATH}")
    print("="*60)

if __name__ == "__main__":
    main()

