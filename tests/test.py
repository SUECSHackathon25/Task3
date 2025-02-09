import numpy as np
from rank.main import get_all_graders, get_mean_grade_for_grader, with_mean_grade, with_preprocessing, with_strict_grader_coefficient

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
        result = get_mean_grade_for_grader(df)

        # Expected output
        expected_alice = 84.33
        expected_bob = 89

        # Check if the result matches the expected output
        self.assertAlmostEqual(result[result["Grader"] == "Alice"]["MeanGrade"].values[0], expected_alice, places=2)
        self.assertAlmostEqual(result[result["Grader"] == "Bob"]["MeanGrade"].values[0], expected_bob, places=2)


class TestWithPreprocessing(unittest.TestCase):
    def test_with_preprocessing(self):
        # Create a sample DataFrame
        data = {
            'Grader1': ['Alice', 'Bob', np.nan, 'Charlie', 'Bob'],
            'Grade1': [85, 0, np.nan, np.nan, 80],
            'Grader2': ['Bob', np.nan, 'Charlie', np.nan, 'Charlie'],
            'Grade2': [88, np.nan, 92, np.nan, np.nan],
            'Poster': ['Post1', "Post0", np.nan, 'Post2', 'Post3']
        }
        df = pd.DataFrame(data)

        # Call the function
        result = with_preprocessing(df)

        # Expected output
        expected_data = {
            'Grader1': ['Alice', 'Bob'],
            'Grade1': [85.0, 80.0],
            'Grader2': ['Bob', np.nan],
            'Grade2': [88.0, np.nan],
            'Poster': ['Post1', 'Post3']
        }
        expected_df = pd.DataFrame(expected_data)

        # Check if the result matches the expected output
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


class TestWithMeanGrade(unittest.TestCase):
    def test_with_mean_grade(self):
        # Create a sample DataFrame
        data = {
            'Grader1': ['Alice', 'Bob', np.nan, 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice'],
            'Grade1': [85, 90, np.nan, 92],
            'Grade2': [88, 85, 92, 90]
        }
        df = pd.DataFrame(data)

        # Call the function
        result = with_mean_grade(df)

        # Expected output
        expected_data = {
            'Grader1': ['Alice', 'Bob', np.nan, 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice'],
            'Grade1': [85, 90, np.nan, 92],
            'Grade2': [88, 85, 92, 90],
            'MeanGrade': [86.5, 87.5, 92.0, 91.0]
        }
        expected_df = pd.DataFrame(expected_data)

        # Check if the result matches the expected output
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)

class TestWithStrictGraderCoefficient(unittest.TestCase):
    def test_with_strict_grader_coefficient(self):
        # Create a sample DataFrame
        data = {
            'Grader1': ['Alice', 'Bob', np.nan, 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice'],
            'Grade1': [1, 3, np.nan, 5],
            'Grade2': [2, 7, 9, 4],
            'MeanGrade': [1.5, 5.0, 9.0, 4.5]
        }
        df = pd.DataFrame(data)

        # Call the function
        result = with_strict_grader_coefficient(df)

        # Expected output
        expected_data = {
            'Grader1': ['Alice', 'Bob', np.nan, 'Charlie'],
            'Grader2': ['Bob', 'Charlie', 'Charlie', 'Alice'],
            'Grade1': [1, 3, np.nan, 5],
            'Grade2': [2, 7, 9, 4],
            'MeanGrade': [1.5, 5.0, 9.0, 4.5],
            'StrictGraderCoefficient': [20 - 2.5 - 2.5, 20 - 2.5 - 7, 20 - 5.0 - 7, 20 - 7 -2.5]
        }
        expected_df = pd.DataFrame(expected_data)

        # Check if the result matches the expected output
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)

if __name__ == '__main__':
    unittest.main()