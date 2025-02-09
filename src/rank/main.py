import pandas as pd
import numpy as np

import optparse

GRADER_COUNT = 2
MAX_GRADE = 10


def get_all_graders(df: pd.DataFrame) -> np.ndarray:
    return df.filter(like="Grader").dropna().agg("unique")


def get_mean_grade_for_grader(df: pd.DataFrame) -> pd.DataFrame:
    grader_list = []
    avg_grade_list = []
    for grader in get_all_graders(df):
        avg_grade = pd.concat(
            [
                df[df[f"Grader{i}"] == grader][f"Grade{i}"]
                for i in range(1, GRADER_COUNT + 1)
            ]
        ).mean()
        grader_list.append(grader)
        avg_grade_list.append(avg_grade)
    return pd.DataFrame(
        {
            "Grader": grader_list,
            "MeanGrade": avg_grade_list,
        }
    )


def calc_mean_grades(row: pd.Series) -> float:
    sum = 0
    count = 0
    for i in range(1, GRADER_COUNT + 1):
        if not np.isnan(row[f"Grade{i}"]):
            sum += row[f"Grade{i}"]
            count += 1
    return sum / count


def with_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    for i in range(1, GRADER_COUNT + 1):
        df.loc[df[f"Grade{i}"].isna(), f"Grader{i}"] = np.nan
        df.loc[df[f"Grade{i}"] == 0, f"Grader{i}"] = np.nan
        df.loc[df[f"Grader{i}"].isna(), f"Grade{i}"] = np.nan
    df = df.dropna(subset=["Poster"], how="all")
    df = df.dropna(subset=[f"Grader{i}" for i in range(1, GRADER_COUNT + 1)], how="all")
    for i in range(1, GRADER_COUNT + 1):
        df[f"Grade{i}"] = df[f"Grade{i}"].astype(float)
    return df


def with_mean_grade(df: pd.DataFrame) -> pd.DataFrame:
    df["MeanGrade"] = df.apply(calc_mean_grades, axis=1)
    return df


def with_strict_grader_coefficient(df: pd.DataFrame) -> pd.DataFrame:
    grader_df = get_mean_grade_for_grader(df)
    df["StrictGraderCoefficient"] = MAX_GRADE * GRADER_COUNT - sum(
        [
            df[f"Grader{i}"]
            .map(grader_df.set_index("Grader")["MeanGrade"])
            .fillna(df["MeanGrade"].mean())
            for i in range(1, GRADER_COUNT + 1)
        ]
    )
    return df


def rank(df: pd.DataFrame) -> pd.DataFrame:
    df = with_preprocessing(df)
    df = with_mean_grade(df)
    df = with_strict_grader_coefficient(df)
    df = df.sort_values(by=["MeanGrade", "StrictGraderCoefficient"], ascending=False)
    return df


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

    if not options.output_file.endswith(".xlsx"):
        options.output_file += ".xlsx"
    if options.output_file.endswith(".csv"):
        df.to_csv(options.output_file, index=False)
    if options.output_file.endswith(".xlsx") or options.output_file.endswith(".xls"):
        df.to_excel(options.output_file, index=False)
