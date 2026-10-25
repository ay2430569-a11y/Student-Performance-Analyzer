"""Run the Student Performance Analyzer."""
from analysis import load_and_clean_data, build_summary, write_report
from database import save_students, get_top_students, get_subject_averages, get_low_attendance
from visualization import create_charts


def main():
    print("\nSTUDENT PERFORMANCE ANALYZER")
    print("-" * 32)

    try:
        students = load_and_clean_data()
        print(f"Loaded and cleaned {len(students)} student records.")

        # Save the cleaned records to SQLite.
        save_students(students)
        print("Records saved to the SQLite database.")

        # Analyze the records.
        summary = build_summary(students)
        top_students = get_top_students(limit=5)
        subject_averages = get_subject_averages()
        low_attendance = get_low_attendance(threshold=75)

        # Create visual charts and a text report.
        chart_paths = create_charts(students)
        report_path = write_report(
            students, summary, top_students, subject_averages, low_attendance
        )

        print("\nSUMMARY")
        print("-" * 32)
        print(f"Total students: {summary['student_count']}")
        print(f"Class average: {summary['class_average']}%")
        print(f"Median percentage: {summary['median_percentage']}%")
        print(f"Highest percentage: {summary['highest_percentage']}%")
        print(f"Lowest percentage: {summary['lowest_percentage']}%")
        print(f"Students at or above 40%: {summary['pass_count']}")
        print(f"Students below 40%: {summary['needs_improvement_count']}")

        print("\nSUBJECT AVERAGES (SQL)")
        for subject, average in zip(
            ["Mathematics", "Science", "English"], subject_averages
        ):
            print(f"{subject}: {average}")

        print("\nTOP 5 STUDENTS (SQL)")
        for rank, (student_id, name, percentage, attendance) in enumerate(
            top_students, start=1
        ):
            print(
                f"{rank}. {name} (ID {student_id}) - "
                f"{percentage:.2f}% | Attendance {attendance:.1f}%"
            )

        print("\nOUTPUT FILES")
        for path in chart_paths:
            print(f"- {path.relative_to(path.parents[1])}")
        print(f"- {report_path.relative_to(report_path.parents[1])}")
        print("- output/cleaned_students.csv")
        print("\nDone! Open the output folder to view the charts and report.")

    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
