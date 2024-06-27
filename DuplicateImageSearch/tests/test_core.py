import unittest
import os
import tempfile
from PIL import Image
from utils.core import find_duplicate_images


class TestCore(unittest.TestCase):

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

    def test_find_duplicate_images(self):
        duplicates = find_duplicate_images(self.test_dir.name)
        self.assertEqual(len(duplicates), 1)
        expected_pairs = {(self.image1_path, self.image2_path), (self.image2_path, self.image1_path)}
        self.assertLessEqual(set(duplicates), expected_pairs)

    def test_find_no_duplicates(self):
        duplicates = find_duplicate_images(self.test_dir.name)
        self.assertEqual(len(duplicates), 1)
        expected_pairs = {(self.image1_path, self.image2_path), (self.image2_path, self.image1_path)}
        self.assertLessEqual(set(duplicates), expected_pairs)
        self.assertNotIn((self.image3_path, self.image1_path), duplicates)
        self.assertNotIn((self.image3_path, self.image2_path), duplicates)


if __name__ == '__main__':
    unittest.main()
    