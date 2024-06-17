import os
import imagehash
from PIL import Image


def find_duplicate_images(folder):
    hashes = {}
    duplicates = []

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(folder, filename)
            try:
                image = Image.open(image_path)
                image_hash = imagehash.phash(image)

                if image_hash in hashes:
                    duplicates.append((image_path, hashes[image_hash]))
                else:
                    hashes[image_hash] = image_path
            except IOError:
                print(f"Could not open image file {image_path}")

    return duplicates


def main():
    folder_path = 'Dataset\Lilly'
    duplicates = find_duplicate_images(folder_path)

    if duplicates:
        print("Found duplicate images:")
        for duplicate in duplicates:
            print(f"Duplicate: {duplicate[0]} and {duplicate[1]}")
    else:
        print("No duplicate images found.")


if __name__ == '__main__':
    main()
