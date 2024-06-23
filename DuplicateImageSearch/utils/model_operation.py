import numpy as np
from keras.applications import EfficientNetB0
from keras.applications.efficientnet import preprocess_input
from keras.preprocessing import image
from keras.models import Model

base_model = EfficientNetB0(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('top_dropout').output)


def extract_features(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    image_array = image.img_to_array(img)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    features = model.predict(image_array)
    return features.flatten()
