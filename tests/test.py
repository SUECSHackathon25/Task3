import numpy as np
from rank.main import get_all_graders, get_mean_grade_for_grader

import pandas as pd
import unittest

class TestGetAllGraders(unittest.TestCase):
    def test_get_all_graders(self):
        # Create a sample DataFrame
        data = {
            'Grader1': ['Alice', 'Bob', 'Alice', 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice']
        }
        df = pd.DataFrame(data)

        # Call the function
        result = get_all_graders(df)

        # Expected output
        expected = ['Alice', 'Bob', 'Charlie']

        # Check if the result matches the expected output
        self.assertTrue(np.array_equal(result, expected))

class TestGetMeanGradeForGrader(unittest.TestCase):
    def test_get_mean_grade_for_grader(self):
        # Create a sample DataFrame
        data = {
            'Grader1': ['Alice', 'Bob', 'Alice', 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice'],
            'Grade1': [85, 90, 78, 92],
            'Grade2': [88, 85, 92, 90]
        }
        df = pd.DataFrame(data)

        # Call the function for Grader1
        result_alice = get_mean_grade_for_grader(df, 'Alice')
        result_bob = get_mean_grade_for_grader(df, 'Bob')

        # Expected output
        expected_alice = 81.5
        expected_bob = 87.5

        # Check if the result matches the expected output
        self.assertAlmostEqual(result_alice, expected_alice, places=2)
        self.assertAlmostEqual(result_bob, expected_bob, places=2)

if __name__ == '__main__':
    unittest.main()