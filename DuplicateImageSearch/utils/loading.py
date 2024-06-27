from PIL import Image


def load_image(image_path):
    try:
        image = Image.open(image_path)
        image.verify()
        image = Image.open(image_path)
        return image
    except (IOError, SyntaxError) as e:
        print(f"Could not open or verify image file {image_path}: {e}")
        return None
    