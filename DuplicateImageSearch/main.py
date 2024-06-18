import os
import imagehash
from PIL import Image
import matplotlib.pyplot as plt


def find_duplicate_images(folder):
    hashes = {}
    duplicates = []

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(folder, filename)
            try:
                image = Image.open(image_path)
                image.verify()
                image = Image.open(image_path)
                image_hash = imagehash.phash(image)

                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                else:
                    hashes[image_hash] = image_path
            except (IOError, SyntaxError) as e:
                print(f"Could not open image file {image_path}: {e}")

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
