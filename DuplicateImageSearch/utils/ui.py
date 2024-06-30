import os
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class ImageNavigator:
    def __init__(self, duplicates):
        """
        Initializes the ImageNavigator with a list of duplicate image pairs and sets up the plot.

        :param duplicates:
        :param duplicates: List of pairs of paths to duplicate images.
        :type duplicates: list
        """
        self.duplicates = duplicates
        self.index = 0

        self.fig, self.axes = plt.subplots(1, 2, figsize=(10, 5))
        plt.subplots_adjust(bottom=0.2)

        axprev = plt.axes([0.3, 0.05, 0.1, 0.075])
        self.button_prev = Button(axprev, 'Previous')
        self.button_prev.on_clicked(self.prev_image)

        axnext = plt.axes([0.6, 0.05, 0.1, 0.075])
        self.button_next = Button(axnext, 'Next')
        self.button_next.on_clicked(self.next_image)

        self.update_images()

    def update_images(self):
        """
        Updates the displayed images to the current pair based on the index.
        Clears the axes and loads the images from the current pair.

        :raises IOError: If an image file cannot be opened.
        :raises SyntaxError: If an image file contains a syntax error.
        """
        for ax, image_path in zip(self.axes, self.duplicates[self.index]):
            ax.clear()
            try:
                image = Image.open(image_path)
                ax.imshow(image)
                ax.set_title(os.path.basename(image_path))
                ax.axis('off')
            except IOError as e:
                ax.set_title(f"Could not open: {os.path.basename(image_path)}")
                print(f"Could not open image file '{image_path}': {e}")
                print("Please check if the file exists and if you have the necessary permissions to open it. "
                      "If the problem persists, ensure the file is not corrupted.")
            except SyntaxError as e:
                ax.set_title(f"Syntax error: {os.path.basename(image_path)}")
                print(f"Syntax error in image file '{image_path}': {e}")
                print("Please check the file for any corruption or format issues. "
                      "Try opening the file with an image viewer to confirm its integrity.")
        self.fig.canvas.draw()

    def next_image(self, event):
        """
        Advances to the next pair of duplicate images and updates the display.

        :param event: The event triggered by clicking the "Next" button.
        :type event: matplotlib.backend_bases.Event
        """
        self.index = (self.index + 1) % len(self.duplicates)
        self.update_images()

    def prev_image(self, event):
        """
        Goes back to the previous pair of duplicate images and updates the display.

        :param event: The event triggered by clicking the "Previous" button.
        :type event: matplotlib.backend_bases.Event
        """
        self.index = (self.index - 1) % len(self.duplicates)
        self.update_images()


def visualize_duplicates(duplicates):
    """
    Visualizes duplicate images with navigation buttons.

    :param duplicates: List of pairs of paths to duplicate images.
    :type duplicates: list
    :raises ValueError: If the duplicates list is empty.
    """
    if not duplicates:
        raise ValueError("The duplicates list is empty. Please provide a list of duplicate image pairs.")

    navigator = ImageNavigator(duplicates)
    plt.show()
