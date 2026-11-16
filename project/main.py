"""
Placement Data Analyzer - Main Application Entry Point
======================================================
Interactive console application for campus placement data analytics.
"""

from placement_analyzer import run_menu, DEFAULT_CSV_PATH


def main():
    run_menu(DEFAULT_CSV_PATH)


if __name__ == "__main__":
    main()
