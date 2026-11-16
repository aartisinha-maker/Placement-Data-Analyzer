"""
Test Suite: Placement Data Analyzer - Four Assignment Test Cases
================================================================
Implements and verifies the four required assignment test cases
using temporary in-memory Pandas DataFrames without modifying placement.csv.
"""

from pathlib import Path
import pandas as pd
from placement_analyzer import (
    TESTCASE4_PIE_PATH,
    load_and_clean_data,
    get_overall_summary,
    display_overall_summary,
    get_branch_analysis,
    display_branch_analysis,
    filter_students_by_package,
    display_filtered_students,
    generate_pie_chart
)


def run_test_case_1():
    print("\n" + "=" * 60)
    print("TEST CASE 1: Normal Input (3 Valid Records)")
    print("=" * 60)

    raw_data = pd.DataFrame([
        {'Student': 'Aman', 'Branch': 'CSE', 'Company': 'TCS', 'Package_LPA': 6},
        {'Student': 'Riya', 'Branch': 'CSE', 'Company': 'Infosys', 'Package_LPA': 8},
        {'Student': 'Karan', 'Branch': 'ECE', 'Company': 'Wipro', 'Package_LPA': 4}
    ])

    cleaned_df, skipped = load_and_clean_data(raw_data)
    summary = get_overall_summary(cleaned_df)
    display_overall_summary(summary, skipped)

    assert len(cleaned_df) == 3, f"Expected 3 valid rows, got {len(cleaned_df)}"
    assert summary['total_placed'] == 3, f"Expected 3 placed, got {summary['total_placed']}"
    assert summary['average_package'] == 6.00, f"Expected 6.00 LPA avg, got {summary['average_package']}"
    assert summary['highest_package'] == 8.00, f"Expected 8.00 LPA highest, got {summary['highest_package']}"
    assert summary['highest_students'][0]['student'] == 'Riya', "Expected highest student to be Riya"
    assert summary['highest_students'][0]['company'] == 'Infosys', "Expected highest company to be Infosys"
    print(">> TEST CASE 1 RESULT: PASSED (All requirements matched)")


def run_test_case_2():
    print("\n" + "=" * 60)
    print("TEST CASE 2: Boundary / Minimum Input (Single Record)")
    print("=" * 60)

    raw_data = pd.DataFrame([
        {'Student': 'Neha', 'Branch': 'CSE', 'Company': 'TCS', 'Package_LPA': 3.5}
    ])

    cleaned_df, skipped = load_and_clean_data(raw_data)
    summary = get_overall_summary(cleaned_df)
    display_overall_summary(summary, skipped)

    assert len(cleaned_df) == 1, f"Expected 1 valid row, got {len(cleaned_df)}"
    assert summary['total_placed'] == 1, f"Expected 1 placed, got {summary['total_placed']}"
    assert summary['average_package'] == 3.50, f"Expected 3.50 LPA avg, got {summary['average_package']}"
    assert summary['highest_package'] == 3.50, f"Expected 3.50 LPA highest, got {summary['highest_package']}"
    assert summary['highest_students'][0]['student'] == 'Neha', "Expected highest student to be Neha"
    assert summary['highest_students'][0]['company'] == 'TCS', "Expected highest company to be TCS"
    print(">> TEST CASE 2 RESULT: PASSED (Boundary test succeeded)")


def run_test_case_3():
    print("\n" + "=" * 60)
    print("TEST CASE 3: Invalid Input (Detection & Skipping)")
    print("=" * 60)

    raw_data = pd.DataFrame([
        {'Student': 'Aman', 'Branch': 'CSE', 'Company': 'TCS', 'Package_LPA': 'abc'},
        {'Student': 'Riya', 'Branch': 'CSE', 'Company': 'Infosys', 'Package_LPA': 8},
        {'Student': 'Karan', 'Branch': 'ECE', 'Company': 'Wipro', 'Package_LPA': -4}
    ])

    cleaned_df, skipped = load_and_clean_data(raw_data)
    summary = get_overall_summary(cleaned_df)
    display_overall_summary(summary, skipped)

    assert len(skipped) == 2, f"Expected 2 skipped records, got {len(skipped)}"
    assert "Row 1 skipped: invalid Package 'abc'." in skipped[0]
    assert "Row 3 skipped: Package must be positive." in skipped[1]
    assert len(cleaned_df) == 1, f"Expected 1 valid row, got {len(cleaned_df)}"
    assert summary['total_placed'] == 1, f"Expected 1 placed, got {summary['total_placed']}"
    assert summary['average_package'] == 8.00, f"Expected 8.00 LPA avg, got {summary['average_package']}"
    print(">> TEST CASE 3 RESULT: PASSED (Data cleaning and error skipping verified)")


def run_test_case_4():
    print("\n" + "=" * 60)
    print("TEST CASE 4: Branch-wise Analysis, Filtering (>7 LPA) & Charts")
    print("=" * 60)

    raw_data = pd.DataFrame([
        {'Student': 'Aman', 'Branch': 'CSE', 'Company': 'TCS', 'Package_LPA': 6},
        {'Student': 'Riya', 'Branch': 'CSE', 'Company': 'Infosys', 'Package_LPA': 8},
        {'Student': 'Karan', 'Branch': 'ECE', 'Company': 'Wipro', 'Package_LPA': 4},
        {'Student': 'Ravi', 'Branch': 'ECE', 'Company': 'Accenture', 'Package_LPA': 12}
    ])

    cleaned_df, skipped = load_and_clean_data(raw_data)

    # 1. Branch-wise Analysis
    analysis_df = get_branch_analysis(cleaned_df)
    display_branch_analysis(analysis_df)

    branch_dict = analysis_df.set_index('Branch').to_dict(orient='index')
    assert branch_dict['CSE']['Placements'] == 2, f"Expected 2 CSE placements, got {branch_dict['CSE']['Placements']}"
    assert branch_dict['ECE']['Placements'] == 2, f"Expected 2 ECE placements, got {branch_dict['ECE']['Placements']}"
    assert branch_dict['CSE']['Average_Package_LPA'] == 7.00, f"Expected 7.00 LPA CSE avg, got {branch_dict['CSE']['Average_Package_LPA']}"
    assert branch_dict['ECE']['Average_Package_LPA'] == 8.00, f"Expected 8.00 LPA ECE avg, got {branch_dict['ECE']['Average_Package_LPA']}"

    # 2. Package Filtering strictly > 7.0 LPA
    min_package = 7.0
    filtered_df = filter_students_by_package(cleaned_df, min_package)
    display_filtered_students(filtered_df, min_package)

    filtered_students = filtered_df['Student'].tolist()
    assert len(filtered_df) == 2, f"Expected 2 students above 7 LPA, got {len(filtered_df)}"
    assert 'Riya' in filtered_students, "Expected Riya in >7 LPA filter"
    assert 'Ravi' in filtered_students, "Expected Ravi in >7 LPA filter"
    assert 'Aman' not in filtered_students, "Aman (6 LPA) should NOT be present"
    assert 'Karan' not in filtered_students, "Karan (4 LPA) should NOT be present"

    # 3. Branch-wise Pie Chart generation (using in-memory DataFrame)
    saved_pie = generate_pie_chart(
        cleaned_df,
        save_path=TESTCASE4_PIE_PATH,
        title="Test Case 4: Branch-wise Placement Distribution",
        show=False
    )

    assert saved_pie is not None, "Failed to generate Test Case 4 pie chart"
    assert Path(saved_pie).exists() and Path(saved_pie).stat().st_size > 0, "Saved pie chart file is invalid"

    branch_counts = cleaned_df['Branch'].value_counts()
    total_count = len(cleaned_df)
    assert (branch_counts['CSE'] / total_count) * 100 == 50.0, "Expected CSE 50.0%"
    assert (branch_counts['ECE'] / total_count) * 100 == 50.0, "Expected ECE 50.0%"

    print(f"[SAVED] Test Case 4 Pie chart saved successfully to '{saved_pie}' (CSE: 50%, ECE: 50%).")
    print(">> TEST CASE 4 RESULT: PASSED (Branch analysis, filtering, and chart verified)")


def run_all_tests():
    print("=" * 60)
    print(" RUNNING COLLEGE ASSIGNMENT 4 TEST CASES VERIFICATION")
    print("=" * 60)
    run_test_case_1()
    run_test_case_2()
    run_test_case_3()
    run_test_case_4()
    print("\n" + "=" * 60)
    print(" ALL 4 TEST CASES COMPLETED AND PASSED WITH 100% SUCCESS!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
