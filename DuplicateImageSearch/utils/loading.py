from PIL import Image


def load_image(image_path):
    """
    Loads an image from the specified path and verifies it.

    :param image_path: Path to the image.
    :type image_path: str
    :return: PIL Image object or None if the image could not be loaded.
    :rtype: Image or None
    :raises IOError: If the image file cannot be opened.
    :raises SyntaxError: If the image file contains a syntax error.
    """
    try:
        image = Image.open(image_path)
        image.verify()
        image = Image.open(image_path)
        return image
    except IOError as e:
        print(f"Could not open image file '{image_path}': {e}")
        print("Please check if you have the necessary permissions to open the file. "
              "Ensure the file is not corrupted and is a valid image format.")
        return None
    except SyntaxError as e:
        print(f"Syntax error in image file '{image_path}': {e}")
        print("Please ensure the image file is not corrupted. "
              "Try opening the file with a different image viewer to verify its integrity.")
        return None
    