import unittest
import os
import tempfile
from PIL import Image
from utils.loading import load_image


class TestLoading(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.image_path = os.path.join(self.test_dir.name, 'image.png')
        self.create_test_image(self.image_path, 'red')

    def tearDown(self):
        self.test_dir.cleanup()

    @staticmethod
    def create_test_image(path, color):
        image = Image.new('RGB', (100, 100), color=color)
        image.save(path)

    def test_load_image(self):
        image = load_image(self.image_path)
        self.assertIsNotNone(image)

    def test_load_corrupt_image(self):
        corrupt_image_path = os.path.join(self.test_dir.name, 'corrupt_image.png')
        with open(corrupt_image_path, 'wb') as f:
            f.write(b'not an image')
        image = load_image(corrupt_image_path)
        self.assertIsNone(image)


if __name__ == '__main__':
    unittest.main()
