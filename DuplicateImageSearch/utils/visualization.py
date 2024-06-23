import os
from PIL import Image
import matplotlib.pyplot as plt


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
