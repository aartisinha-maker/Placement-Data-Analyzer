# Placement Data Analyzer

A Python console-based data analytics application developed to process, clean, analyze, and visualize campus placement records using **Pandas** and **Matplotlib**.

---

## 1. Project Introduction

The **Placement Data Analyzer** is an end-to-end data analysis tool designed for college placement cells and academic evaluators. It reads campus placement records from a CSV file, performs comprehensive data cleaning to detect corrupted or missing data, computes key statistical metrics, performs branch-wise grouping, filters records based on student salary packages (LPA), and generates visual charts.

This application is strictly built as a console-based Python project following all college assignment specifications without external web frameworks.

---

## 2. Project Objectives

- **Automated Data Validation & Cleaning**: Ingest raw placement data, validate mandatory columns, remove duplicate records, detect non-numeric inputs, and reject non-positive (zero or negative) package entries without modifying the underlying CSV file.
- **Placement Performance Summary**: Compute total placed candidates, calculate overall average package in LPA, and identify the highest package along with the student name and offering company.
- **Branch-wise Categorization**: Group records by engineering branches using Pandas `groupby()` to determine branch placement counts and branch average salaries.
- **Dynamic Threshold Filtering**: Allow users to query and filter students with salary packages strictly higher than any user-defined threshold.
- **Visual Analytics**: Produce publication-quality Matplotlib charts (Bar chart for placement numbers per branch, Pie chart for branch placement distribution) and save them as PNG files.
- **Robust Exception Handling**: Ensure the application never crashes when presented with invalid user input, malformed CSV records, or boundary scenarios.

---

## 3. Technologies Used

- **Language**: Python 3 (Python 3.10+)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/) (`read_csv`, `groupby`, series aggregations, DataFrame filtering)
- **Data Visualization**: [Matplotlib](https://matplotlib.org/) (`pyplot` bar charts, pie charts, custom labels, figure export)

---

## 4. Key Features

1. **Safe CSV Loading & Cleaning**:
   - Reads `placement.csv` using Pandas.
   - Enforces required columns: `Student, Branch, Company, Package_LPA`.
   - Flags and skips rows with missing attributes, duplicate records, non-numeric strings, or packages $\le 0$.
   - Retains 1-based data row numbers for transparent error reporting.
   - Strictly read-only: never modifies or overwrites the original CSV dataset.

2. **Overall Placement Summary**:
   - Total number of placed students.
   - Overall average salary package in LPA (rounded to 2 decimal places).
   - Maximum package offered, including the recipient student and recruiting company.

3. **Branch-wise Analysis**:
   - Calculates total student placements per branch using Pandas `groupby('Branch')`.
   - Computes branch-specific average packages.

4. **Package Filtering**:
   - User inputs a minimum package threshold in LPA.
   - Filters and displays students earning **strictly greater** than the entered package.
   - Outputs student name, branch, company, and package.

5. **Graphical Visualizations**:
   - **Bar Chart**: Visualizes placement counts across branches with exact count annotations on each bar.
   - **Pie Chart**: Visualizes the proportional distribution (%) of placed students across branches with legend and percentage markers.
   - Both charts are saved as high-resolution PNG files (`branch_placements_bar.png` and `branch_distribution_pie.png`).

6. **Interactive Console Menu**:
   ```
   ========================================
          PLACEMENT DATA ANALYZER          
   ========================================

   1. Overall Placement Summary
   2. Branch-wise Analysis and Package Filter
   3. Generate and Display Charts
   4. Exit

   Enter your choice:
   ```
   - Each option returns cleanly to the main menu upon pressing Enter.
   - The application does not terminate until option 4 is selected.

---

## 5. CSV Dataset Structure

The project processes a CSV file named `placement.csv` containing the following four columns:

| Column Header | Data Type | Description |
| :--- | :--- | :--- |
| `Student` | String | Full name of the candidate |
| `Branch` | String | Academic department (e.g., CSE, ECE, IT, ME, EE, Civil) |
| `Company` | String | Name of the hiring company |
| `Package_LPA` | Float | Annual compensation in Lakhs Per Annum (LPA) |

*Sample Data:*
```csv
Student,Branch,Company,Package_LPA
Aman,CSE,TCS,6
Riya,CSE,Infosys,8
Karan,ECE,Wipro,4
```

---

## 6. Installation & Setup

### Prerequisites
Ensure Python 3 is installed on your computer.

### Installing Dependencies
Open your command terminal (Command Prompt, PowerShell, or Bash) in the project directory and install the required libraries:

```bash
pip install pandas matplotlib
```

---

## 7. Execution Instructions

### Running the Interactive Application
To launch the console-based Placement Data Analyzer, execute:

```bash
python main.py
```

### Running the Four Assignment Test Cases
To run automated verification of all four college assignment test cases using in-memory DataFrames without modifying `placement.csv`:

```bash
python test_cases.py
```

---

## 8. Explanation of the Four Required Test Cases

Per the college assignment guidelines, the test cases verify different data scenarios using temporary in-memory DataFrames:

### Test Case 1: Normal Input
* **Scenario**: Standard dataset with three valid records.
  ```text
  Aman,CSE,TCS,6
  Riya,CSE,Infosys,8
  Karan,ECE,Wipro,4
  ```
* **Objective**: Verifies baseline metric calculations.
* **Calculation**:
  - Total Placed: 3 students
  - Average Package: $\frac{6 + 8 + 4}{3} = 6.00\text{ LPA}$
  - Highest Package: $8.00\text{ LPA}$ (Riya, Infosys)
* **Status**: **PASSED**

---

### Test Case 2: Boundary / Minimum Input
* **Scenario**: Minimal valid dataset containing exactly one record.
  ```text
  Neha,CSE,TCS,3.5
  ```
* **Objective**: Validates that division by 1, single-element aggregations, and edge cases do not crash the application.
* **Calculation**:
  - Total Placed: 1 student
  - Average Package: $3.50\text{ LPA}$
  - Highest Package: $3.50\text{ LPA}$ (Neha, TCS)
* **Status**: **PASSED**

---

### Test Case 3: Invalid Input & Data Cleaning
* **Scenario**: Dataset containing corrupted and negative package entries.
  ```text
  Aman,CSE,TCS,abc
  Riya,CSE,Infosys,8
  Karan,ECE,Wipro,-4
  ```
* **Objective**: Tests data validation, safe conversion using error catching, and row-level logging.
* **Expected Cleaning Output**:
  - `Row 1 skipped: invalid Package 'abc'.`
  - `Row 3 skipped: Package must be positive.`
  - Valid records retained: 1 (Riya, CSE, Infosys, 8.00 LPA)
  - Average Package: $8.00\text{ LPA}$
* **Status**: **PASSED**

---

### Test Case 4: Branch-wise Analysis, Filtering, and Visualization
* **Scenario**: Multi-branch dataset with four records.
  ```text
  Aman,CSE,TCS,6
  Riya,CSE,Infosys,8
  Karan,ECE,Wipro,4
  Ravi,ECE,Accenture,12
  ```
* **Objective**: Verifies branch grouping, branch averages, strict package threshold filtering (`> 7 LPA`), and pie chart rendering.
* **Calculations**:
  - **Placements Count**:
    - CSE: 2 (Aman, Riya)
    - ECE: 2 (Karan, Ravi)
  - **Average Package**:
    - CSE Average: $\frac{6 + 8}{2} = 7.00\text{ LPA}$
    - ECE Average: $\frac{4 + 12}{2} = 8.00\text{ LPA}$
  - **Filter > 7.0 LPA (Strict Inequality)**:
    - Riya ($8.00\text{ LPA}$)
    - Ravi ($12.00\text{ LPA}$)
    *(Aman at 6 and Karan at 4 are excluded)*
  - **Chart**: Generated and saved `testcase4_branch_pie.png`.
* **Status**: **PASSED**

---

## 9. Project File Structure

```text
D:\project
│
├── placement.csv                               # Main campus placement dataset (100 records)
├── main.py                                     # Interactive console menu entry point
├── placement_analyzer.py                       # Core analysis engine & modular functions
├── test_cases.py                               # Automated test suite for the 4 assignment test cases
├── README.md                                   # Comprehensive project documentation
│
├── branch_placements_bar.png                   # Output: Branch placement counts (Bar chart)
├── branch_distribution_pie.png                 # Output: Branch placement share (Pie chart)
├── testcase4_branch_pie.png                    # Output: Pie chart from Test Case 4
│
├── generate_report.py                          # Automated PDF report generation script (ReportLab)
└── Placement_Data_Analyzer_Project_Report.pdf  # Comprehensive academic project report (PDF)
```

---

## 10. Module Guide (Viva / Project Evaluation Preparation)

When presenting this project to your college evaluator, explain each function as follows:

1. **`load_and_clean_data(source)`**:
   - Takes either a CSV filepath or an in-memory DataFrame.
   - Checks if required columns (`Student`, `Branch`, `Company`, `Package_LPA`) exist.
   - Uses row iteration to detect nulls, duplicate keys, non-numeric package strings (`to_numeric` / `float()` error handling), and values $\le 0$.
   - Collects diagnostic messages explaining skipped rows while keeping the original file intact.

2. **`get_overall_summary(df)`**:
   - Computes summary statistics using vectorized Pandas functions (`len`, `mean()`, `max()`).
   - Identifies the maximum value in `Package_LPA` and extracts the student name and recruiting company.

3. **`get_branch_analysis(df)`**:
   - Uses Pandas `df.groupby('Branch')['Package_LPA']`.
   - Aggregates using `.count()` for placement totals and `.mean()` for branch averages.

4. **`filter_students_by_package(df, min_package)`**:
   - Uses boolean indexing: `df[df['Package_LPA'] > min_package]`.
   - Ensures strict inequality ($>$ rather than $\ge$) per assignment guidelines.

5. **`generate_and_save_charts(df, ...)`**:
   - Uses `matplotlib.pyplot` to generate a customized bar chart and pie chart.
   - Configures titles, labels, legends, colors, and percentages.
   - Saves figures as high-resolution PNG files via `fig.savefig()`.

6. **`run_menu(csv_file)`**:
   - Houses the interactive `while` loop that powers the console menu.
   - Wraps inputs in `try-except` blocks to handle non-numeric inputs, EOF, or abrupt exits gracefully.
