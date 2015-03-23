pass_module = __import__('pass')
import unittest, shutil, os

class TestPassHelperFunctions(unittest.TestCase):

    def make_test_file(self, new_file_path):
        dirname = os.path.dirname(new_file_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if not os.path.exists(new_file_path):
            open(new_file_path, 'a').close()

    def setUp(self):
        test_files = ['testing/top1', 'testing/top2', 'testing/mid/mid', 'testing/mid/bottom/bottom']

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.top_directory = os.path.join(current_dir, 'testing')
        self.test_file_dirs = sorted([os.path.join(current_dir, test_file) for test_file in test_files])

        for filename in self.test_file_dirs:
            self.make_test_file(filename)

    def test_extract_pw_keys(self):
        results = sorted(pass_module.extract_pw_keys(self.top_directory))
        self.assertEqual(self.test_file_dirs, results)

    def tearDown(self):
        shutil.rmtree(self.top_directory)

if __name__ == '__main__':
    unittest.main()
