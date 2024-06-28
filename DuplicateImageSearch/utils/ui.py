import os
from PIL import Image
import matplotlib.pyplot as plt


def visualize_duplicates(duplicates):
    """
    Visualizes duplicate images.

    :param duplicates: List of pairs of paths to duplicate images.
    :type duplicates: list
    :raises IOError: If an image file cannot be opened.
    :raises SyntaxError: If an image file contains a syntax error.
    """
    for duplicate in duplicates:
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        for ax, image_path in zip(axes, duplicate):
            try:
                image = Image.open(image_path)
                ax.imshow(image)
                ax.set_title(os.path.basename(image_path))
                ax.axis('off')
            except IOError as e:
                print(f"Could not open image file '{image_path}': {e}")
                print("Please check if the file exists and if you have the necessary permissions to open it. "
                      "If the problem persists, ensure the file is not corrupted.")
            except SyntaxError as e:
                print(f"Syntax error in image file '{image_path}': {e}")
                print("Please check the file for any corruption or format issues. "
                      "Try opening the file with an image viewer to confirm its integrity.")

        plt.show()
