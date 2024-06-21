import os
import numpy as np
import imagehash
from PIL import Image
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from keras.applications import EfficientNetB0
from keras.applications.efficientnet import preprocess_input
from keras.preprocessing import image
from keras.models import Model

base_model = EfficientNetB0(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('top_dropout').output)


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


def extract_features(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    image_array = image.img_to_array(img)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    features = model.predict(image_array)
    return features.flatten()


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
                else:
                    hashes[image_hash] = image_path

                for stored_path, stored_features in features.items():
                    similarity = np.linalg.norm(image_features - stored_features)
                    if similarity < 0.5:
                        duplicates.append((image_path, stored_path))
                        break

                features[image_path] = image_features
    return duplicates


def visualize_duplicates(duplicates):
    for duplicate in duplicates:
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for ax, image_path in zip(axes, duplicate):
            try:
                image = Image.open(image_path)
                ax.imshow(image)
                ax.set_title(os.path.basename(image_path))
                ax.axis('off')
            except (IOError, SyntaxError) as e:
                print(f"Could not open image file {image_path}: {e}")

        plt.show()


def main():
    folder_path = 'Dataset\Lilly'
    duplicates = find_duplicate_images(folder_path)

    if duplicates:
        print("Found duplicate images:")
        for duplicate in duplicates:
            print(f"Duplicate: {duplicate[0]} and {duplicate[1]}")
        visualize_duplicates(duplicates)
    else:
        print("No duplicate images found.")


if __name__ == '__main__':
    main()
