"""Load, clean, and analyze student performance data."""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "students.csv"
OUTPUT_DIR = BASE_DIR / "output"

REQUIRED_COLUMNS = [
    "student_id", "name", "math_marks", "science_marks",
    "english_marks", "attendance"
]
MARK_COLUMNS = ["math_marks", "science_marks", "english_marks"]


def load_and_clean_data():
    """Load the CSV, validate records, and save a cleaned copy."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Make sure data/students.csv exists."
        )

    dataframe = pd.read_csv(DATA_PATH)
    missing_columns = [column for column in REQUIRED_COLUMNS
                       if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {missing_columns}")

    dataframe = dataframe[REQUIRED_COLUMNS].copy()
    dataframe["name"] = dataframe["name"].astype("string").str.strip()

    numeric_columns = ["student_id", *MARK_COLUMNS, "attendance"]
    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    # Remove rows with missing values or invalid numeric entries.
    dataframe = dataframe.dropna(subset=REQUIRED_COLUMNS)
    dataframe = dataframe[dataframe["name"].str.len() > 0]

    # IDs must be whole numbers; remove duplicate IDs, keeping the first.
    dataframe = dataframe[dataframe["student_id"] % 1 == 0]
    dataframe = dataframe.drop_duplicates(subset=["student_id"], keep="first")

    # Marks and attendance must be in the inclusive range 0 to 100.
    valid_range = pd.Series(True, index=dataframe.index)
    for column in [*MARK_COLUMNS, "attendance"]:
        valid_range &= dataframe[column].between(0, 100)
    dataframe = dataframe[valid_range].copy()

    dataframe["student_id"] = dataframe["student_id"].astype(int)
    dataframe[MARK_COLUMNS + ["attendance"]] = (
        dataframe[MARK_COLUMNS + ["attendance"]].astype(float)
    )

    if dataframe.empty:
        raise ValueError(
            "No valid student records remain after cleaning. "
            "Check the values in data/students.csv."
        )

    # Total is out of 300; percentage is therefore average marks out of 100.
    dataframe["total_marks"] = dataframe[MARK_COLUMNS].sum(axis=1)
    dataframe["percentage"] = (dataframe["total_marks"] / 3).round(2)
    dataframe["performance"] = np.where(
        dataframe["percentage"] >= 40, "Pass", "Needs Improvement"
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    dataframe.to_csv(OUTPUT_DIR / "cleaned_students.csv", index=False)
    return dataframe


def build_summary(dataframe):
    """Create summary statistics with Pandas and NumPy."""
    subject_averages = dataframe[MARK_COLUMNS].mean().round(2)
    percentages = dataframe["percentage"].to_numpy()

    return {
        "student_count": int(len(dataframe)),
        "class_average": round(float(np.mean(percentages)), 2),
        "median_percentage": round(float(np.median(percentages)), 2),
        "highest_percentage": round(float(np.max(percentages)), 2),
        "lowest_percentage": round(float(np.min(percentages)), 2),
        "pass_count": int((dataframe["percentage"] >= 40).sum()),
        "needs_improvement_count": int((dataframe["percentage"] < 40).sum()),
        "subject_averages": subject_averages.to_dict(),
    }


def write_report(dataframe, summary, top_students, sql_subject_averages,
                 low_attendance):
    """Write a plain-text report from the computed results."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "analysis_report.txt"

    lines = [
        "STUDENT PERFORMANCE ANALYZER",
        "=" * 32,
        "",
        f"Valid student records: {summary['student_count']}",
        f"Class average percentage: {summary['class_average']}%",
        f"Median percentage: {summary['median_percentage']}%",
        f"Highest percentage: {summary['highest_percentage']}%",
        f"Lowest percentage: {summary['lowest_percentage']}%",
        f"Students at or above 40%: {summary['pass_count']}",
        f"Students below 40%: {summary['needs_improvement_count']}",
        "",
        "SUBJECT AVERAGES (calculated with SQL)",
        "-" * 38,
        f"Mathematics: {sql_subject_averages[0]}",
        f"Science:     {sql_subject_averages[1]}",
        f"English:     {sql_subject_averages[2]}",
        "",
        "TOP 5 STUDENTS (SQL ranking)",
        "-" * 28,
    ]

    for rank, (student_id, name, percentage, attendance) in enumerate(top_students, start=1):
        lines.append(
            f"{rank}. {name} (ID {student_id}) - "
            f"{percentage:.2f}% | Attendance: {attendance:.1f}%"
        )

    lines.extend(["", "ATTENDANCE BELOW 75%", "-" * 20])
    if low_attendance:
        for student_id, name, attendance in low_attendance:
            lines.append(f"{name} (ID {student_id}) - {attendance:.1f}%")
    else:
        lines.append("No students below 75% attendance.")

    lines.extend([
        "",
        "NOTES",
        "-" * 5,
        "This report describes the supplied sample dataset only.",
        "Attendance and marks may be related, but this report does not prove causation.",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
