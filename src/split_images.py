import os
import shutil
import numpy as np


# Definiowanie ścieżek
base_dir = 'data/pre_images'
train_dir = 'data/train'
val_dir = 'data/validation'

# Tworzenie katalogów treningowych i walidacyjnych, jeśli jeszcze nie istnieją
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Przechodzenie przez każdy folder (gatunek) w folderze bazowym
for folder in os.listdir(base_dir):
    current_dir = os.path.join(base_dir, folder)
    if os.path.isdir(current_dir):
        files = os.listdir(current_dir)

        # Mieszanie plików
        np.random.shuffle(files)

        # Tworzenie odpowiednich folderów dla każdego gatunku
        os.makedirs(os.path.join(train_dir, folder), exist_ok=True)
        os.makedirs(os.path.join(val_dir, folder), exist_ok=True)

        # Dzieląc dane na zestaw treningowy (80%) i walidacyjny (20%)
        train_files = files[:int(len(files) * 0.8)]
        val_files = files[int(len(files) * 0.8):]

        # Kopiowanie plików do odpowiednich folderów
        for file in train_files:
            shutil.copy(
                os.path.join(current_dir, file),
                os.path.join(train_dir, folder)
            )
        for file in val_files:
            shutil.copy(
                os.path.join(current_dir, file),
                os.path.join(val_dir, folder)
            )
