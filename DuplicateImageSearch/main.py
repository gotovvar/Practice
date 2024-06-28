from utils.core import find_duplicate_images
from utils.ui import visualize_duplicates

FOLDER_PATH = 'dataset/Lilly'


def main():
    duplicates = find_duplicate_images(FOLDER_PATH)

    if duplicates:
        print("Found duplicate images:")
        for duplicate in duplicates:
            print(f"Duplicate: {duplicate[0]} and {duplicate[1]}")
        visualize_duplicates(duplicates)
    else:
        print("No duplicate images found.")


if __name__ == '__main__':
    main()
