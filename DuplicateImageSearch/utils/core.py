import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.processing import process_image

SUPPORTED_IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
SIMILARITY_THRESHOLD = 0.6


def find_duplicate_images(folder):
    """
    Finds duplicate images in the specified directory.

    :param folder: Path to the directory containing images.
    :type folder: str
    :return: List of pairs of paths to duplicate images.
    :rtype: list
    :raises FileNotFoundError: If the specified directory does not exist.
    :raises ValueError: If no supported image formats are found in the directory.
    """
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"The directory '{folder}' does not exist. "
                                "Please provide a valid directory path that contains images.")

    image_files = [filename for filename in os.listdir(folder) if filename.lower().endswith(SUPPORTED_IMAGE_FORMATS)]

    if not image_files:
        raise ValueError(
            f"No supported image formats found in '{folder}'. Please ensure that the directory contains images with "
            f"one of the following formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}.")

    hashes = {}
    features = {}
    duplicates = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, os.path.join(folder, filename)): filename
                   for filename in image_files}

        for future in as_completed(futures):
            image_path, image_hash, image_features = future.result()
            if image_hash and image_features is not None:
                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                    continue

                is_duplicate_found = False
                for stored_path, stored_features in features.items():
                    similarity = np.linalg.norm(image_features - stored_features)
                    if similarity < SIMILARITY_THRESHOLD:
                        duplicates.append((image_path, stored_path))
                        is_duplicate_found = True
                        break

                if not is_duplicate_found:
                    hashes[image_hash] = image_path
                    features[image_path] = image_features

    return duplicates
