# Student Performance Analyzer

A beginner-friendly Python data-analysis project using **Python, Pandas, NumPy, SQLite, and Matplotlib**. It loads fictional student marks and attendance from CSV, cleans and validates records, calculates statistics, stores the cleaned data in SQLite, runs SQL queries, and saves charts plus a text report.

## Features

- Load student records from CSV using Pandas.
- Clean missing, duplicate, and out-of-range records.
- Calculate totals, percentages, median, averages, and performance categories.
- Store the cleaned dataset in a SQLite database.
- Use SQL to find top performers, subject averages, and attendance below 75%.
- Save three charts as PNG files.
- Generate a plain-text analysis report.

## Project structure

```text
Student-Performance-Analyzer/
├── data/students.csv
├── output/
├── analysis.py
├── database.py
├── visualization.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer recommended
- VS Code
- Python extension for VS Code

SQLite is included with Python; you do not need to install or run a separate database server.

## Run in VS Code

### 1. Open the folder

Extract this project ZIP and open the `Student-Performance-Analyzer` folder in VS Code.

### 2. Create a virtual environment

Open **Terminal → New Terminal** and run:

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

If activation works, install the packages:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Run the program

```powershell
python main.py
```

If `python` is not recognized, try:
```powershell
py main.py
```

### 4. Check the generated output

After a successful run, the program creates:

- `students.db` — SQLite database
- `output/cleaned_students.csv` — cleaned records plus calculated columns
- `output/subject_averages.png`
- `output/marks_distribution.png`
- `output/attendance_vs_marks.png`
- `output/analysis_report.txt`

The charts are saved to files; the program does not require a chart window to open.

## Dataset columns

| Column | Meaning |
|---|---|
| `student_id` | Unique whole-number ID |
| `name` | Student name |
| `math_marks` | Mathematics marks out of 100 |
| `science_marks` | Science marks out of 100 |
| `english_marks` | English marks out of 100 |
| `attendance` | Attendance percentage |

The included dataset contains fictional sample records. Replace or extend it with data you are permitted to use. Do not upload real students' personal or academic information without permission.

## Seven development phases

1. **Load and explore:** inspect CSV rows, columns, data types, and missing values.
2. **Clean data:** remove invalid rows and duplicate IDs; validate marks and attendance.
3. **Analyze:** calculate totals, percentages, averages, and median using Pandas/NumPy.
4. **Use SQL:** save records in SQLite and query rankings, subject averages, and low attendance.
5. **Visualize:** create subject-average, percentage-distribution, and attendance-vs-percentage charts.
6. **Report:** write summary statistics and SQL query results to a text report.
7. **Integrate and publish:** run everything from `main.py`, test it, and push the project to GitHub.

## Important interpretation note

A scatter plot can show whether attendance and marks move together in this dataset, but it does not prove that one causes the other. The pass threshold of 40% is an example setting, not a claim about any particular institution's rules.

## Future improvements

- Add unit tests with `pytest`.
- Add command-line options for the pass mark and attendance threshold.
- Add an optional machine-learning extension using scikit-learn only after the data pipeline is understood.
