"""
Placement Data Analyzer
=======================
Console application for campus placement data analytics using Pandas and Matplotlib.
Columns required: Student, Branch, Company, Package_LPA
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# File paths and configuration
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = BASE_DIR / "placement.csv"
DEFAULT_BAR_CHART_PATH = BASE_DIR / "branch_placements_bar.png"
DEFAULT_PIE_CHART_PATH = BASE_DIR / "branch_distribution_pie.png"
TESTCASE4_PIE_PATH = BASE_DIR / "testcase4_branch_pie.png"
REQUIRED_COLUMNS = ['Student', 'Branch', 'Company', 'Package_LPA']
CHART_COLORS = ['#2E86AB', '#F24236', '#F5EE9E', '#47A992', '#564256', '#F68E5F', '#A3C4BC', '#845EC2']


def load_and_clean_data(source):
    """Load CSV or DataFrame, validate columns, and clean invalid records."""
    if isinstance(source, pd.DataFrame):
        raw_df = source.copy()
    elif isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: '{path}'")
        raw_df = pd.read_csv(path)
    else:
        raise TypeError("Source must be a file path string/Path or a pandas DataFrame.")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in raw_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}. Expected: {REQUIRED_COLUMNS}")

    valid_rows, skipped_reasons, seen = [], [], set()

    for idx, row in raw_df.iterrows():
        row_num = idx + 1
        student, branch = row['Student'], row['Branch']
        company, pkg_val = row['Company'], row['Package_LPA']

        # Detect missing values
        if pd.isna(student) or str(student).strip() == "":
            skipped_reasons.append(f"Row {row_num} skipped: Missing student name.")
            continue
        if pd.isna(branch) or str(branch).strip() == "":
            skipped_reasons.append(f"Row {row_num} skipped: Missing branch for student '{student}'.")
            continue
        if pd.isna(company) or str(company).strip() == "":
            skipped_reasons.append(f"Row {row_num} skipped: Missing company for student '{student}'.")
            continue
        if pd.isna(pkg_val) or str(pkg_val).strip() == "":
            skipped_reasons.append(f"Row {row_num} skipped: Missing package value.")
            continue

        # Detect duplicates
        key = (str(student).strip().lower(), str(branch).strip().lower(),
               str(company).strip().lower(), str(pkg_val).strip())
        if key in seen:
            skipped_reasons.append(f"Row {row_num} skipped: Duplicate record for student '{student}'.")
            continue

        # Validate numeric package
        try:
            pkg_numeric = float(pkg_val)
        except (ValueError, TypeError):
            skipped_reasons.append(f"Row {row_num} skipped: invalid Package '{pkg_val}'.")
            continue

        # Reject zero and negative package values
        if pkg_numeric <= 0:
            skipped_reasons.append(f"Row {row_num} skipped: Package must be positive.")
            continue

        seen.add(key)
        valid_rows.append({
            'Student': str(student).strip(),
            'Branch': str(branch).strip(),
            'Company': str(company).strip(),
            'Package_LPA': round(pkg_numeric, 2)
        })

    return pd.DataFrame(valid_rows), skipped_reasons


def get_overall_summary(df):
    """Compute total placed, average package, and highest package with student/company."""
    if df is None or df.empty:
        return {'total_placed': 0, 'average_package': 0.0, 'highest_package': 0.0, 'highest_students': []}

    avg_pkg = round(float(df['Package_LPA'].mean()), 2)
    max_pkg = round(float(df['Package_LPA'].max()), 2)
    highest_records = df[df['Package_LPA'] == max_pkg]
    highest_students = [
        {'student': r['Student'], 'company': r['Company']} for _, r in highest_records.iterrows()
    ]
    return {
        'total_placed': len(df),
        'average_package': avg_pkg,
        'highest_package': max_pkg,
        'highest_students': highest_students
    }


def display_overall_summary(summary, skipped_reasons=None):
    """Print overall placement summary."""
    print("\n" + "=" * 45)
    print("         OVERALL PLACEMENT SUMMARY")
    print("=" * 45)
    if skipped_reasons:
        print("\nData Cleaning Notices:")
        for reason in skipped_reasons:
            print(f"  [SKIPPED] {reason}")
        print(f"Valid records: {summary['total_placed']}")

    print(f"Total placed: {summary['total_placed']}")
    print(f"Average package: {summary['average_package']:.2f} LPA")
    if summary['total_placed'] > 0:
        details = ", ".join(f"{s['student']}, {s['company']}" for s in summary['highest_students'])
        print(f"Highest: {summary['highest_package']:.2f} LPA ({details})")
    else:
        print("Highest: N/A (No valid records)")
    print("=" * 45)


def get_branch_analysis(df):
    """Calculate branch-wise placement counts and averages using groupby()."""
    if df is None or df.empty:
        return pd.DataFrame(columns=['Branch', 'Placements', 'Average_Package_LPA'])

    grp = df.groupby('Branch')['Package_LPA']
    return pd.DataFrame({
        'Placements': grp.count(),
        'Average_Package_LPA': grp.mean().round(2)
    }).reset_index()


def display_branch_analysis(analysis_df):
    """Print branch-wise analysis."""
    print("\n" + "-" * 45)
    print("         BRANCH-WISE PLACEMENT ANALYSIS")
    print("-" * 45)
    if analysis_df.empty:
        print("No placement data available for branch analysis.")
        return

    print("Placements:")
    for _, row in analysis_df.iterrows():
        print(f"  {row['Branch']}: {int(row['Placements'])}")

    print("\nAverage package:")
    for _, row in analysis_df.iterrows():
        print(f"  {row['Branch']}: {row['Average_Package_LPA']:.2f} LPA")
    print("-" * 45)


def filter_students_by_package(df, min_package):
    """Return students whose package is strictly greater than min_package."""
    if df is None or df.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    return df[df['Package_LPA'] > min_package].copy()


def display_filtered_students(filtered_df, min_package):
    """Print table of filtered students."""
    print(f"\n--- Students with Package strictly greater than {min_package:.2f} LPA ---")
    if filtered_df.empty:
        print(f"No students found with package greater than {min_package:.2f} LPA.")
        return

    print(f"{'Student':<20} {'Branch':<10} {'Company':<20} {'Package (LPA)':<15}")
    print("-" * 65)
    for _, r in filtered_df.iterrows():
        print(f"{r['Student']:<20} {r['Branch']:<10} {r['Company']:<20} {r['Package_LPA']:<15.2f}")
    print("-" * 65)


def _get_branch_counts(df):
    """Helper to extract non-empty branch lists and counts."""
    if df is None or df.empty or 'Branch' not in df.columns:
        return None, None
    valid = df[df['Branch'].notna() & (df['Branch'].astype(str).str.strip() != "")]
    if valid.empty:
        return None, None
    counts = valid['Branch'].value_counts()
    return counts.index.tolist(), counts.values.tolist()


def generate_bar_chart(df, save_path=None, show=False, close=True):
    """Generate and save branch-wise placement bar chart."""
    branches, counts = _get_branch_counts(df)
    if not branches:
        print("[WARNING] Cannot generate bar chart: No valid placement records found.")
        return None

    target = Path(save_path) if save_path else DEFAULT_BAR_CHART_PATH
    colors = CHART_COLORS[:len(branches)] if len(branches) <= len(CHART_COLORS) else '#2E86AB'

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(branches, counts, color=colors, edgecolor='black', linewidth=1.2, width=0.55)
    ax.set_title('Branch-wise Placement Counts', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Branch', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('Number of Placed Students', fontsize=12, fontweight='bold', labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_ylim(0, max(counts) * 1.18 if counts else 1)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{int(h)}', xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

    plt.tight_layout()
    fig.savefig(target, dpi=150, bbox_inches='tight')

    try:
        fig.canvas.manager.set_window_title("Branch-wise Placement Counts")
    except Exception:
        pass

    if show and sys.stdin.isatty():
        try:
            plt.show()
        except Exception:
            pass
        finally:
            if close:
                plt.close(fig)
    elif close:
        plt.close(fig)

    return str(target)


def generate_pie_chart(df, save_path=None, title='Branch-wise Placement Distribution', show=False, close=True):
    """Generate and save branch-wise placement pie chart."""
    branches, counts = _get_branch_counts(df)
    if not branches:
        print("[WARNING] Cannot generate pie chart: No valid placement records found.")
        return None

    target = Path(save_path) if save_path else DEFAULT_PIE_CHART_PATH
    colors = CHART_COLORS[:len(branches)] if len(branches) <= len(CHART_COLORS) else None

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _, autotexts = ax.pie(
        counts, labels=branches, autopct='%1.1f%%', startangle=140,
        colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},
        textprops={'fontsize': 11, 'fontweight': 'bold'}, pctdistance=0.75
    )
    for at in autotexts:
        at.set_color('black')
        at.set_fontsize(10)
        at.set_fontweight('bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    labels = [f"{b}: {c} ({c / sum(counts) * 100:.1f}%)" for b, c in zip(branches, counts)]
    ax.legend(wedges, labels, title="Branches", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

    plt.tight_layout()
    fig.savefig(target, dpi=150, bbox_inches='tight')

    try:
        fig.canvas.manager.set_window_title(title)
    except Exception:
        pass

    if show and sys.stdin.isatty():
        try:
            plt.show()
        except Exception:
            pass
        finally:
            if close:
                plt.close(fig)
    elif close:
        plt.close(fig)

    return str(target)


def generate_and_save_charts(df, bar_path=None, pie_path=None, show=True):
    """Generate and save both bar and pie charts, reusing the respective functions."""
    if df is None or df.empty:
        print("[WARNING] Cannot generate charts: No placement records found.")
        return []

    target_bar = Path(bar_path) if bar_path else DEFAULT_BAR_CHART_PATH
    target_pie = Path(pie_path) if pie_path else DEFAULT_PIE_CHART_PATH

    # Reuse generate_bar_chart and generate_pie_chart without duplicate plotting code
    saved_bar = generate_bar_chart(df, save_path=target_bar, show=False, close=not show)
    saved_pie = generate_pie_chart(df, save_path=target_pie, show=False, close=not show)
    saved_files = [f for f in [saved_bar, saved_pie] if f]

    if show and saved_files:
        try:
            if sys.stdin.isatty():
                plt.show()
        except Exception:
            pass
        finally:
            plt.close('all')

    return saved_files


def run_menu(csv_file=None):
    """Run interactive console menu for Placement Data Analyzer."""
    target_csv = Path(csv_file) if csv_file else DEFAULT_CSV_PATH
    print(f"\nStarting Placement Data Analyzer...\nTarget dataset: {target_csv.name}")

    try:
        cleaned_df, skipped = load_and_clean_data(target_csv)
        print(f"Data loaded successfully! Total valid records: {len(cleaned_df)}")
        if skipped:
            print(f"Note: {len(skipped)} invalid record(s) were skipped during cleaning.")
    except Exception as e:
        print(f"[ERROR] Failed to load dataset '{target_csv}': {e}")
        return

    def pause():
        try:
            input("Press Enter to return to the main menu...")
        except (EOFError, KeyboardInterrupt):
            pass

    while True:
        print("\n" + "=" * 40)
        print("       PLACEMENT DATA ANALYZER          ")
        print("=" * 40)
        print("\n1. Overall Placement Summary")
        print("2. Branch-wise Analysis and Package Filter")
        print("3. Generate and Display Charts")
        print("4. Exit")

        try:
            choice = input("\nEnter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Placement Data Analyzer. Thank you!")
            break

        if choice == '1':
            display_overall_summary(get_overall_summary(cleaned_df), skipped)
            print()
            pause()

        elif choice == '2':
            display_branch_analysis(get_branch_analysis(cleaned_df))
            print("\n--- Package Filter ---")
            try:
                pkg_input = input("Enter minimum package threshold to filter (LPA) [Press Enter to skip]: ").strip()
            except (EOFError, KeyboardInterrupt):
                pkg_input = ""

            if pkg_input:
                try:
                    min_pkg = float(pkg_input)
                    if min_pkg < 0:
                        print("Threshold cannot be negative. Please enter a valid non-negative number.")
                    else:
                        display_filtered_students(filter_students_by_package(cleaned_df, min_pkg), min_pkg)
                except ValueError:
                    print("Invalid input. Please enter a numeric package value (e.g., 7.0).")

            print()
            pause()

        elif choice == '3':
            print("\nGenerating placement visualization charts...")
            generate_and_save_charts(cleaned_df, show=True)
            print("\nCharts generated successfully!")
            pause()

        elif choice == '4':
            print("\nExiting Placement Data Analyzer. Thank you!")
            break

        else:
            print("Invalid choice! Please select a valid option (1, 2, 3, or 4).")


if __name__ == "__main__":
    run_menu(DEFAULT_CSV_PATH)
