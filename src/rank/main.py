import pandas as pd
import numpy as np

import optparse

def get_all_posters(df: pd.DataFrame) -> np.ndarray:
    return df['Poster'].unique()

def get_all_graders(df: pd.DataFrame) -> np.ndarray:
    return df.filter(like='Grader').agg('unique')

def get_mean_grade_for_grader(df: pd.DataFrame, grader: str) -> pd.DataFrame:
    pass

def rank(df: pd.DataFrame) -> pd.DataFrame:
    pass
    

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="input_file", help="Input file path")
    parser.add_option("-o", "--output", dest="output_file", help="Output file path")
    (options, args) = parser.parse_args()

    if not options.input_file:
        print("Error: Input file path is required.")
        exit(1)

    if not options.output_file:
        print("Error: Output file path is required.")
        exit(1)

    # Read the input XLS file into a DataFrame
    # Columns: ["Poster", "Grader1", "Grade1", "Grader2", "Grade2"]
    df = pd.read_excel(options.input_file)

    df = rank(df)

    # Write the DataFrame to an output CSV file
    df.to_excel(options.output_file, index=False)