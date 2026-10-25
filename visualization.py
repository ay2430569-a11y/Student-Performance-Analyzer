"""Create charts for the Student Performance Analyzer."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Save charts without requiring a GUI window.
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
MARK_COLUMNS = ["math_marks", "science_marks", "english_marks"]
SUBJECT_NAMES = ["Mathematics", "Science", "English"]


def create_charts(dataframe):
    """Save three charts as PNG files in the output directory."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 1. Average marks for each subject.
    averages = dataframe[MARK_COLUMNS].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(SUBJECT_NAMES, averages.values)
    ax.set_title("Average Marks by Subject")
    ax.set_ylabel("Average marks (out of 100)")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "subject_averages.png", dpi=150)
    plt.close(fig)

    # 2. Distribution of student percentages.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(dataframe["percentage"], bins=10, edgecolor="black")
    ax.set_title("Distribution of Student Percentages")
    ax.set_xlabel("Percentage")
    ax.set_ylabel("Number of students")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "marks_distribution.png", dpi=150)
    plt.close(fig)

    # 3. Attendance versus percentage. This shows association, not causation.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(dataframe["attendance"], dataframe["percentage"])
    ax.set_title("Attendance vs Student Percentage")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Percentage (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "attendance_vs_marks.png", dpi=150)
    plt.close(fig)

    return [
        OUTPUT_DIR / "subject_averages.png",
        OUTPUT_DIR / "marks_distribution.png",
        OUTPUT_DIR / "attendance_vs_marks.png",
    ]
