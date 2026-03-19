import torch
from torch import nn
import os
import json
import matplotlib.pyplot as plt


# Create checkpoints directory if it doesn't exist
CHECKPOINT_DIR = "checkpoints"
if not os.path.exists(CHECKPOINT_DIR):
    os.makedirs(CHECKPOINT_DIR)


class TrainingConfig:
    def __init__(self, checkpoint_name="best_model"):
        self.num_epochs = 20
        self.learning_rate = 0.001
        self.batch_size = 32
        self.patience = 5  # For early stopping
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.checkpoint_path = os.path.join(CHECKPOINT_DIR, f"{checkpoint_name}.pt")
        self.history_path = os.path.join(CHECKPOINT_DIR, f"{checkpoint_name}_history.json")


def train_model(model, train_loader, val_loader, config):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)

    # Tracking metrics
    history = {
        'train_loss': [],
        'val_loss': [],
        'val_accuracy': []
    }

    best_val_loss = float('inf')
    patience_counter = 0
    best_model_state = None

    for epoch in range(config.num_epochs):
        # Training
        model.train()
        train_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(config.device), labels.to(config.device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)

        # Validation
        model.eval()
        val_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(config.device), labels.to(config.device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        val_loss /= len(val_loader)
        val_accuracy = 100 * correct / total

        # Store history
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_accuracy)

        print(f"Epoch {epoch+1}/{config.num_epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.2f}%")

        # Early stopping logic
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
            print("[OK] Best model saved")
        else:
            patience_counter += 1
            if patience_counter >= config.patience:
                print(f"\nEarly stopping triggered after {epoch+1} epochs")
                model.load_state_dict(best_model_state)
                break

    # Save best model checkpoint
    torch.save(best_model_state, config.checkpoint_path)
    print(f"\n[OK] Best model checkpoint saved to: {config.checkpoint_path}")
    
    # Save training history
    save_history(history, config.history_path)
    print(f"[OK] Training history saved to: {config.history_path}")
    
    return model, history


def save_history(history, filepath):
    """Save training history to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(history, f, indent=2)


def load_checkpoint(model, checkpoint_path, device):
    """Load a saved model checkpoint"""
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    print(f"[OK] Model loaded from checkpoint: {checkpoint_path}")
    return model


def load_history(history_path):
    """Load training history from JSON file"""
    with open(history_path, 'r') as f:
        history = json.load(f)
    return history


def plot_training_curves(history, save_path="checkpoints/training_curves.png"):
    """Plot and save training curves"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot loss
    axes[0].plot(history['train_loss'], label='Training Loss', marker='o')
    axes[0].plot(history['val_loss'], label='Validation Loss', marker='s')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot accuracy
    axes[1].plot(history['val_accuracy'], label='Validation Accuracy', marker='s', color='green')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=100)
    print(f"[OK] Training curves saved to: {save_path}")
    plt.close()


