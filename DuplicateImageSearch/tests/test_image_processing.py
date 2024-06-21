import unittest
import os
import tempfile
from PIL import Image
from main import find_duplicate_images, visualize_duplicates, process_image, extract_features
import numpy as np


class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.image1_path = os.path.join(self.test_dir.name, 'image1.png')
        self.image2_path = os.path.join(self.test_dir.name, 'image2.png')
        self.image3_path = os.path.join(self.test_dir.name, 'image3.jpg')
        self.create_test_image(self.image1_path, 'red')
        self.create_test_image(self.image2_path, 'red')
        self.create_test_image(self.image3_path, 'black')

    def tearDown(self):
        self.test_dir.cleanup()

    @staticmethod
    def create_test_image(path, color):
        image = Image.new('RGB', (100, 100), color=color)
        image.save(path)

    def test_process_image(self):
        image_path, image_hash, image_features = process_image(self.image1_path)
        self.assertIsNotNone(image_hash)
        self.assertIsNotNone(image_features)
        self.assertEqual(image_path, self.image1_path)

    def test_process_corrupt_image(self):
        corrupt_image_path = os.path.join(self.test_dir.name, 'corrupt_image.png')
        with open(corrupt_image_path, 'wb') as f:
            f.write(b'not an image')
        image_path, image_hash, image_features = process_image(corrupt_image_path)
        self.assertIsNone(image_hash)
        self.assertIsNone(image_features)
        self.assertEqual(image_path, corrupt_image_path)

    def test_find_duplicate_images(self):
        duplicates = find_duplicate_images(self.test_dir.name)
        self.assertEqual(len(duplicates), 1)
        expected_pairs = {(self.image1_path, self.image2_path), (self.image2_path, self.image1_path)}
        self.assertLessEqual(set(duplicates), expected_pairs)

    def test_find_no_duplicates(self):
        duplicates = find_duplicate_images(self.test_dir.name)
        self.assertEqual(len(duplicates), 1)  # Only 1 duplicate pair expected
        expected_pairs = {(self.image1_path, self.image2_path), (self.image2_path, self.image1_path)}
        self.assertLessEqual(set(duplicates), expected_pairs)
        self.assertNotIn((self.image3_path, self.image1_path), duplicates)
        self.assertNotIn((self.image3_path, self.image2_path), duplicates)

    def test_visualize_duplicates(self):
        duplicates = [(self.image1_path, self.image2_path)]
        try:
            visualize_duplicates(duplicates)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"visualize_duplicates вызвало исключение: {e}")

    def test_visualize_no_duplicates(self):
        duplicates = []
        try:
            visualize_duplicates(duplicates)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"visualize_duplicates вызвало исключение: {e}")

    def test_extract_features(self):
        features1 = extract_features(self.image1_path)
        features2 = extract_features(self.image2_path)
        features3 = extract_features(self.image3_path)
        self.assertIsInstance(features1, np.ndarray)
        self.assertIsInstance(features2, np.ndarray)
        self.assertIsInstance(features3, np.ndarray)
        self.assertGreater(len(features1), 0)
        self.assertGreater(len(features2), 0)
        self.assertGreater(len(features3), 0)

    def test_feature_similarity(self):
        features1 = extract_features(self.image1_path)
        features2 = extract_features(self.image2_path)
        features3 = extract_features(self.image3_path)
        similarity1_2 = np.linalg.norm(features1 - features2)
        similarity1_3 = np.linalg.norm(features1 - features3)
        self.assertLess(similarity1_2, 0.5)
        self.assertGreater(similarity1_3, 0.5)


if __name__ == '__main__':
    unittest.main()
