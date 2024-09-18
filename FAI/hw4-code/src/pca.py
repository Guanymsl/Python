import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

"""
Implementation of Principal Component Analysis.
"""
class PCA:
    def __init__(self, n_components: int) -> None:
        self.n_components = n_components
        self.mean = None
        self.components = None

    def fit(self, X: np.ndarray) -> None:
        #TODO: 10%
        self.mean = np.mean(X, axis=0)
        XCentered = X - self.mean
        Cov = np.cov(XCentered, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(Cov)
        ind = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, ind]
        self.components = eigenvectors[:, :self.n_components]

        draw_image(self)

    def transform(self, X: np.ndarray) -> np.ndarray:
        #TODO: 2%
        XCentered = X - self.mean
        return np.dot(XCentered, self.components)

    def reconstruct(self, X):
        #TODO: 2%
        XTransformed = self.transform(X)
        return np.dot(XTransformed, self.components.T) + self.mean

def image_reshape(img_data_reconstructed_flat: np.ndarray) -> np.ndarray:
    return img_data_reconstructed_flat.reshape([61, 80])

def draw_image(pca: PCA):
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))

    axes[0].imshow(image_reshape(pca.mean), cmap='gray')
    axes[0].set_title('Mean Image')
    axes[0].axis('off')

    for i in range(4):
        eigenvector_image = image_reshape(pca.components[:, i])
        axes[i+1].imshow(eigenvector_image, cmap='gray')
        axes[i+1].set_title(f'Eigenvector {i+1}')
        axes[i+1].axis('off')

    plt.show()
