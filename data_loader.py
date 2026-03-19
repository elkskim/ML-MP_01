import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

def load_cifar10():
    """
    Load CIFAR10 dataset with basic preprocessing
    Returns: train_loader, val_loader, test_loader, and dataset info
    """
    # Define preprocessing: normalize to [-1, 1] range
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    # Download and load training data
    trainset = torchvision.datasets.CIFAR10(
        root='./data', 
        train=True, 
        download=True, 
        transform=transform
    )
    
    # Download and load test data
    testset = torchvision.datasets.CIFAR10(
        root='./data', 
        train=False, 
        download=True, 
        transform=transform
    )
    
    # Split training data: 80% train, 20% validation
    train_size = int(0.8 * len(trainset))
    val_size = len(trainset) - train_size
    train_set, val_set = torch.utils.data.random_split(
        trainset, 
        [train_size, val_size]
    )
    
    # Create dataloaders
    train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=32, shuffle=False)
    test_loader = DataLoader(testset, batch_size=32, shuffle=False)
    
    return train_loader, val_loader, test_loader, trainset.classes

def get_dataset_info():
    """Print basic info about CIFAR10"""
    print("CIFAR10 Dataset Info:")
    print("- Image size: 32x32 pixels")
    print("- Channels: 3 (RGB)")
    print("- Number of classes: 10")
    print("- Total training samples: 50,000")
    print("- Total test samples: 10,000")

