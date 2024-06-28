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
    except (IOError, SyntaxError) as e:
        print(f"Could not open or verify image file {image_path}: {e}")
        return None
    