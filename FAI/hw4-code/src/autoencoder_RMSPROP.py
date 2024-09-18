import torch
from tqdm.auto import tqdm
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

"""
Implementation of Autoencoder
"""
class Autoencoder(nn.Module):
    def __init__(self, input_dim: int, encoding_dim: int) -> None:
        """
        Modify the model architecture here for comparison
        """
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, encoding_dim),
            nn.Linear(encoding_dim, encoding_dim//2),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim//2, encoding_dim),
            nn.Linear(encoding_dim, input_dim),
        )

    def forward(self, x):
        #TODO: 5%
        return self.decoder(self.encoder(x))

    def fit(self, X, epochs=10, batch_size=32):
        #TODO: 5%
        if isinstance(X, np.ndarray):
            X = torch.tensor(X, dtype=torch.float32)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        X = X.to(device)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.parameters(), lr=0.1)
        dataset = torch.utils.data.TensorDataset(X)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.train()
        loss_values = []

        for epoch in range(epochs):
            epoch_loss = 0
            for data in tqdm(dataloader, desc=f'Epoch {epoch+1}/{epochs}'):
                inputs = data[0]
                optimizer.zero_grad()
                outputs = self.forward(inputs)
                loss = criterion(outputs, inputs)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            avg_loss = epoch_loss / len(dataloader)
            loss_values.append(avg_loss)
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')

        plt.plot(range(1, epochs+1), loss_values)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training Loss for Autoencoder')
        plt.show()

    def transform(self, X):
        #TODO: 2%
        if isinstance(X, np.ndarray):
            X = torch.tensor(X, dtype=torch.float32)
        X = X.to(next(self.parameters()).device)
        self.eval()
        with torch.no_grad():
            encoded = self.encoder(X)
        return encoded.cpu().numpy()

    def reconstruct(self, X):
        #TODO: 2%
        if isinstance(X, np.ndarray):
            X = torch.tensor(X, dtype=torch.float32)
        X = X.to(next(self.parameters()).device)
        self.eval()
        with torch.no_grad():
            reconstructed = self(X)
        return reconstructed.cpu().numpy()


"""
Implementation of DenoisingAutoencoder
"""
class DenoisingAutoencoder(Autoencoder):
    def __init__(self, input_dim, encoding_dim, noise_factor=0.2):
        super(DenoisingAutoencoder, self).__init__(input_dim,encoding_dim)
        self.noise_factor = noise_factor

    def add_noise(self, x):
        #TODO: 3%
        noise = self.noise_factor * torch.randn_like(x)
        noisy_x = x + noise
        noisy_x = torch.clip(noisy_x, 0., 1.)
        return noisy_x

    def fit(self, X, epochs=10, batch_size=32):
        #TODO: 4%
        if isinstance(X, np.ndarray):
            X = torch.tensor(X, dtype=torch.float32)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(device)
        X = X.to(device)

        criterion = nn.MSELoss()
        optimizer = optim.RMSprop(self.parameters(), lr=0.001)
        dataset = torch.utils.data.TensorDataset(X)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.train()
        loss_values = []

        for epoch in range(epochs):
            epoch_loss = 0
            for data in tqdm(dataloader, desc=f'Epoch {epoch+1}/{epochs}'):
                inputs = data[0]
                noisy_inputs = self.add_noise(inputs)
                optimizer.zero_grad()
                outputs = self.forward(noisy_inputs)
                loss = criterion(outputs, inputs)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()

            avg_loss = epoch_loss / len(dataloader)
            loss_values.append(avg_loss)
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')

        plt.plot(range(1, epochs+1), loss_values)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training Loss for DenoisingAutoencoder')
        plt.show()
