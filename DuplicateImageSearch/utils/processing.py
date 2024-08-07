import numpy as np
import imagehash
from keras.applications import EfficientNetB0
from keras.applications.efficientnet import preprocess_input
from keras.preprocessing import image
from keras.models import Model
from utils.loading import load_image

TARGET_SIZE = (224, 224)

base_model = EfficientNetB0(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('top_dropout').output)


def extract_image_features(image_path):
    """
    Extracts features from an image using EfficientNetB0.

    :param image_path: Path to the image.
    :type image_path: str
    :return: Feature vector of the image.
    :rtype: np.ndarray
    """
    img = image.load_img(image_path, target_size=TARGET_SIZE)
    image_array = image.img_to_array(img)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    features = model.predict(image_array)
    return features.flatten()


def process_image(image_path):
    """
    Processes an image and extracts its hash and features.

    :param image_path: Path to the image.
    :type image_path: str
    :return: Image path, image hash, image features.
    :rtype: tuple
    """
    image = load_image(image_path)
    if image is not None:
        image_hash = imagehash.phash(image)
        image_features = extract_image_features(image_path)
        return image_path, image_hash, image_features
    return image_path, None, None
