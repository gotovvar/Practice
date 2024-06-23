import os
import numpy as np
import imagehash
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.model_operation import extract_features


def process_image(image_path):
    try:
        image = Image.open(image_path)
        image.verify()
        image = Image.open(image_path)
        image_hash = imagehash.phash(image)
        image_features = extract_features(image_path)
        return image_path, image_hash, image_features
    except (IOError, SyntaxError) as e:
        print(f"Could not open or verify image file {image_path}: {e}")
        return image_path, None, None


def find_duplicate_images(folder):
    hashes = {}
    features = {}
    duplicates = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, os.path.join(folder, filename)): filename
                   for filename in os.listdir(folder) if
                   filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))}

        for future in as_completed(futures):
            image_path, image_hash, image_features = future.result()
            if image_hash and image_features is not None:
                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                    continue

                duplicate_found = False
                for stored_path, stored_features in features.items():
                    similarity = np.linalg.norm(image_features - stored_features)
                    if similarity < 0.5:
                        duplicates.append((image_path, stored_path))
                        duplicate_found = True
                        break

                if not duplicate_found:
                    hashes[image_hash] = image_path
                    features[image_path] = image_features

    return duplicates
