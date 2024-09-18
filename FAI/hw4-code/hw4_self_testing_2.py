import os
import numpy as np
import torch
from PIL import Image
from src.autoencoder_RMSPROP import DenoisingAutoencoder
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

DATA_PATH = './data'
np.random.seed(0)

def read_image():
    file_path = './data/subject_05_17.png'
    img = Image.open(file_path).convert("L")
    img_array = np.array(img)
    img_vector = img_array.flatten()
    img_vector = img_vector/255.0
    return np.array(img_vector, dtype='float')

def load_data(split: str) -> tuple[np.ndarray, np.ndarray]:
    data_path = DATA_PATH+'/'+split
    files = os.listdir(data_path)
    image_vectors = []
    label_vectors = []
    for f in files:
        img = Image.open(data_path + '/'+f).convert("L")
        f_name, f_type = os.path.splitext(f)
        label = int(f_name[-2:])-1
        label_vectors.append(label)
        img_array = np.array(img)
        img_vector = img_array.flatten()
        img_vector = img_vector/255.0
        image_vectors.append(img_vector)
    return np.array(image_vectors), np.array(label_vectors)

def compute_acc(y_pred: np.ndarray, y_val: np.ndarray):
    return np.sum(y_pred == y_val) / len(y_val)

def reconstruction_loss(img_vec: np.ndarray, img_vec_reconstructed: np.ndarray) -> float:
    return ((img_vec - img_vec_reconstructed)**2).mean()

def main():
    print("Loading data...")
    X_train, y_train = load_data("train")
    X_val, y_val = load_data("val")

    deno_autoencoder = DenoisingAutoencoder(input_dim=4880, encoding_dim=488)
    print("DenoisingAutoencoder Training Start...")
    deno_autoencoder.fit(X_train, epochs=5000, batch_size=135)

    X_train_transformed_deno_ae = deno_autoencoder.transform(X_train)
    X_val_transformed_deno_ae = deno_autoencoder.transform(X_val)

    clf_deno_ae = LogisticRegression(max_iter=10000, random_state=0)
    print("Logistic Regression Training Start...")
    clf_deno_ae.fit(X_train_transformed_deno_ae, y_train)

    y_pred_deno_ae = clf_deno_ae.predict(X_val_transformed_deno_ae)
    print(f"Acc from DenoisingAutoencoder: {compute_acc(y_pred_deno_ae, y_val)}")

    img_vec = read_image()
    img_reconstruct_deno_ae = deno_autoencoder.reconstruct(torch.tensor(img_vec, dtype=torch.float32))

    reconstruction_loss_deno_ae = reconstruction_loss(img_vec, img_reconstruct_deno_ae)
    print(f"Reconstruction Loss with DenoisingAutoencoder: {reconstruction_loss_deno_ae}")

    def image_reshape(img_data_reconstructed_flat: np.ndarray) -> np.ndarray:
        img_data_reconstructed = img_data_reconstructed_flat.reshape([61, 80])
        return (img_data_reconstructed * 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(image_reshape(img_vec), cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(image_reshape(img_reconstruct_deno_ae), cmap='gray')
    axes[1].set_title('Reconstructed Image with DenoisingAutoencoder')
    axes[1].axis('off')

    plt.show()

if __name__ == "__main__":
    main()
