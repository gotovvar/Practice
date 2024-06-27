import unittest
from utils.ui import visualize_duplicates
import os
import tempfile
from PIL import Image


class TestUI(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.image1_path = os.path.join(self.test_dir.name, 'image1.png')
        self.image2_path = os.path.join(self.test_dir.name, 'image2.png')
        self.create_test_image(self.image1_path, 'red')
        self.create_test_image(self.image2_path, 'red')

    def tearDown(self):
        self.test_dir.cleanup()

    @staticmethod
    def create_test_image(path, color):
        image = Image.new('RGB', (100, 100), color=color)
        image.save(path)

    def test_visualize_duplicates(self):
        duplicates = [(self.image1_path, self.image2_path)]
        try:
            visualize_duplicates(duplicates)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"visualize_duplicates raised an exception: {e}")

    def test_visualize_no_duplicates(self):
        duplicates = []
        try:
            visualize_duplicates(duplicates)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"visualize_duplicates raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
