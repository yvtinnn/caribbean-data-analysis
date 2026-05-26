#!/usr/bin/env python3
"""
Caribbean Cybersecurity Risk Assessment - Main Orchestrator

This script runs the complete analysis pipeline:
1. Data Collection & Risk Calculation
2. Visualization Generation (static + interactive)
3. PDF Report Generation

Usage:
    python run_analysis.py           # Run all steps
    python run_analysis.py --data   # Data collection only
    python run_analysis.py --viz    # Visualizations only
    python run_analysis.py --report # Report generation only
"""

import argparse
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))


def run_data_collection():
    """Step 1: Collect data and calculate risk index"""
    print("\n" + "=" * 70)
    print("  STEP 1: DATA COLLECTION & RISK CALCULATION")
    print("=" * 70)
    from scripts import data_collection
    return data_collection


def run_visualizations():
    """Step 2: Generate all visualizations"""
    print("\n" + "=" * 70)
    print("  STEP 2: VISUALIZATION GENERATION")
    print("=" * 70)
    from scripts import visualizations
    return visualizations


def run_report():
    """Step 3: Generate PDF report"""
    print("\n" + "=" * 70)
    print("  STEP 3: PDF REPORT GENERATION")
    print("=" * 70)
    from scripts import report_generator
    return report_generator


def main():
    parser = argparse.ArgumentParser(
        description='Caribbean Cybersecurity Risk Assessment Pipeline'
    )
    parser.add_argument(
        '--step', '-s',
        choices=['data', 'viz', 'report', 'all'],
        default='all',
        help='Which step to run (default: all)'
    )
    parser.add_argument(
        '--skip-update',
        action='store_true',
        help='Skip data update (use existing CSV files)'
    )
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  CARIBBEAN CYBERSECURITY RISK ASSESSMENT")
    print("  Complete Analysis Pipeline")
    print("=" * 70)

    success = True

    if args.step in ['data', 'all']:
        try:
            from scripts import data_collection
            print("  Module loaded successfully")
        except ImportError as e:
            print(f"  ERROR: Could not load data_collection: {e}")
            success = False

    if args.step in ['viz', 'all']:
        try:
            from scripts import visualizations
            print("  Module loaded successfully")
        except ImportError as e:
            print(f"  ERROR: Could not load visualizations: {e}")
            success = False

    if args.step in ['report', 'all']:
        try:
            from scripts import report_generator
            print("  Module loaded successfully")
        except ImportError as e:
            print(f"  ERROR: Could not load report_generator: {e}")
            success = False

    if success:
        print("\n" + "=" * 70)
        print("  PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\n  Output files:")
        print("    - Visualizations: visualizations/")
        print("    - Report: report/Caribbean_Cybersecurity_Risk_Assessment_Jamaica.pdf")
        print("    - Interactive Map: visualizations/07_risk_choropleth_map.html")
        print("    - Forecast Data: data/processed/attack_forecast.csv")
    else:
        print("\n" + "=" * 70)
        print("  PIPELINE COMPLETED WITH ERRORS")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
