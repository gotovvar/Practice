import os
import imagehash
from PIL import Image
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_image(image_path):
    try:
        image = Image.open(image_path)
        image.verify()
        image = Image.open(image_path)
        image_hash = imagehash.phash(image)
        return image_path, image_hash
    except (IOError, SyntaxError) as e:
        print(f"Could not open or verify image file {image_path}: {e}")
        return image_path, None


def find_duplicate_images(folder):
    hashes = {}
    duplicates = []

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, os.path.join(folder, filename)): filename
                   for filename in os.listdir(folder) if
                   filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))}

        for future in as_completed(futures):
            image_path, image_hash = future.result()
            if image_hash:
                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                else:
                    hashes[image_hash] = image_path

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
