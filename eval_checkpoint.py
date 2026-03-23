"""
Quick Evaluation Script - Load and Evaluate Any Checkpoint Locally

This script loads a trained model from checkpoints/ and evaluates it on the test set.
Usage: python eval_checkpoint.py <checkpoint_name>
Example: python eval_checkpoint.py colab_experiment_v2_lr_0p0005
"""

import torch
from torch import nn
from data_loader import load_cifar10
from model import SimpleCNN
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import sys

def evaluate_checkpoint(checkpoint_name):
    """Evaluate a saved checkpoint on the test set"""
    
    checkpoint_path = f"checkpoints/{checkpoint_name}.pt"
    
    print("\n" + "="*60)
    print(f"EVALUATING CHECKPOINT: {checkpoint_name}")
    print("="*60)
    
    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load data
    print("\nLoading CIFAR10 dataset...")
    train_loader, val_loader, test_loader, classes = load_cifar10()
    
    # Load model
    print(f"Loading model from: {checkpoint_path}")
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    print("[OK] Model loaded")
    
    # Evaluate
    print("\nEvaluating on test set...")
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
    
    # Print results
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(f"Test Accuracy: {test_accuracy:.2f}%")
    print(f"Test Loss: {avg_test_loss:.4f}")
    print(f"Correct: {correct}/{total}")
    print("="*60)
    
    # Classification report
    print("\nPER-CLASS METRICS:")
    print("-"*60)
    print(classification_report(all_labels, all_preds, target_names=classes))
    
    return test_accuracy, avg_test_loss, all_preds, all_labels, classes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eval_checkpoint.py <checkpoint_name>")
        print("Example: python eval_checkpoint.py colab_experiment_v2_lr_0p0005")
        print("\nAvailable checkpoints:")
        import os
        for f in os.listdir("checkpoints"):
            if f.endswith(".pt"):
                print(f"  - {f[:-3]}")
        sys.exit(1)
    
    checkpoint_name = sys.argv[1]
    evaluate_checkpoint(checkpoint_name)

