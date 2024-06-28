import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.processing import process_image

SUPPORTED_IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
SIMILARITY_THRESHOLD = 0.6


def find_duplicate_images(folder):
    hashes = {}
    features = {}
    duplicates = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, os.path.join(folder, filename)): filename
                   for filename in os.listdir(folder) if
                   filename.lower().endswith(SUPPORTED_IMAGE_FORMATS)}

        for future in as_completed(futures):
            image_path, image_hash, image_features = future.result()
            if image_hash and image_features is not None:
                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                    continue

                duplicate_found = False
                for stored_path, stored_features in features.items():
                    similarity = np.linalg.norm(image_features - stored_features)
                    if similarity < SIMILARITY_THRESHOLD:
                        duplicates.append((image_path, stored_path))
                        duplicate_found = True
                        break

                if not duplicate_found:
                    hashes[image_hash] = image_path
                    features[image_path] = image_features

    return duplicates
