import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    """
    A simple CNN architecture for CIFAR10 classification.
    
    Architecture:
    - Conv2d(3→32) + ReLU + MaxPool
    - Conv2d(32→64) + ReLU + MaxPool
    - Conv2d(64→128) + ReLU + MaxPool
    - Flatten
    - Linear(2048→256) + ReLU + Dropout
    - Linear(256→10) + Dropout
    
    Args:
        dropout_p1: Dropout probability after first FC layer (default: 0.5)
        dropout_p2: Dropout probability after second FC layer (default: 0.3)
    """
    
    def __init__(self, dropout_p1=0.5, dropout_p2=0.3):
        super(SimpleCNN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)
        
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU()
        self.pool3 = nn.MaxPool2d(2, 2)
        
        # Fully connected layers
        # After 3 pooling operations: 32 → 16 → 8 → 4 pixels
        # So flattened size is 4 * 4 * 128 = 2048
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.relu4 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout_p1)  # Configurable dropout
        self.fc2 = nn.Linear(256, 10)  # 10 classes in CIFAR10
        self.dropout2 = nn.Dropout(dropout_p2)  # Configurable dropout
    
    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch_size, 3, 32, 32)
        
        Returns:
            Output tensor of shape (batch_size, 10)
        """
        # Conv block 1
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        
        # Conv block 2
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        # Conv block 3
        x = self.conv3(x)
        x = self.relu3(x)
        x = self.pool3(x)
        
        # Flatten for fully connected layers
        x = x.view(x.size(0), -1)
        
        # Fully connected layers with dropout
        x = self.fc1(x)
        x = self.relu4(x)
        x = self.dropout1(x)  # Apply dropout after ReLU activation
        
        x = self.fc2(x)
        # Note: No ReLU after fc2 since it's the output layer
        x = self.dropout2(x)  # Apply dropout after output layer
        
        return x

