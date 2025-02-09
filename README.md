# Task3

## Install Dependencies

With `pip`:

```bash
python -m venv .venv
pip install -r requirements.txt
```

or with `uv`:

```bash
uv sync
```

## Run

```bash
source .venv/bin/activate
src/rank/main.py -i <input.xlsx> -o <output.xlsx>
```

## Algorithm

Algorithm is simple:

1. Rank by the average grade
2. If the average grade is the same, rank by the strictness of the graders

The strictness of the grader is calculated as follows:

```
strictness = MAX_GRADE - AVG(All grades graded by the grader)
```

So if grader A gave 5 grades: 1, 3, 7, 9, 10,

then the strictness of grader A is 10 - (1 + 3 + 7 + 9 + 10) / 5 = 10 - 6 = 4

If there is only one grader, then the strictness of the missing grader is:

```
strictness = MAX_GRADE - AVG(All grades)
```

The strictness of multiple graders are added together to get a StrictGraderCoefficient for each student.

In our point of view, the grader's familiarity with the poster should not be considered as a factor in the ranking process. The familiarity factor is already considered in the grader assignment process. Therefore, we only consider graders' distribution of grades (strictness) in the ranking process as the secondary factor when the average grades are the same.

