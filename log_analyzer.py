#!/usr/bin/env python3
"""
Log Analyzer Script
Analyzes server logs for errors and patterns
"""

import os
import re
from datetime import datetime

def analyze_logs(log_file):
    """Analyze log file for errors - INEFFICIENT VERSION"""
    
    # Inefficiency 1: Reading entire file into memory
    with open(log_file, 'r') as f:
        all_lines = f.readlines()
    
    errors = []
    warnings = []
    info = []
    
    # Inefficiency 2: Multiple passes over the same data
    for line in all_lines:
        if 'ERROR' in line:
            errors.append(line)
    
    for line in all_lines:
        if 'WARNING' in line:
            warnings.append(line)
    
    for line in all_lines:
        if 'INFO' in line:
            info.append(line)
    
    # Inefficiency 3: Inefficient string concatenation in loop
    report = ""
    report += "="*50 + "\n"
    report += "Log Analysis Report\n"
    report += "="*50 + "\n"
    report += f"Total Errors: {len(errors)}\n"
    report += f"Total Warnings: {len(warnings)}\n"
    report += f"Total Info: {len(info)}\n"
    report += "="*50 + "\n"
    
    # Inefficiency 4: Nested loops with O(n²) complexity
    duplicate_errors = []
    for i in range(len(errors)):
        for j in range(i+1, len(errors)):
            if errors[i] == errors[j]:
                if errors[i] not in duplicate_errors:
                    duplicate_errors.append(errors[i])
    
    report += f"Duplicate Errors: {len(duplicate_errors)}\n"
    
    # Inefficiency 5: Using regex in tight loop
    error_codes = []
    for error in errors:
        match = re.search(r'ERROR\s+(\d+)', error)
        if match:
            error_codes.append(match.group(1))
    
    # Inefficiency 6: Sorting without considering memory
    sorted_errors = sorted(errors)
    sorted_warnings = sorted(warnings)
    
    return report

def find_log_files(directory):
    """Find all log files - INEFFICIENT VERSION"""
    
    # Inefficiency 7: Walking entire directory tree multiple times
    log_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.log'):
                log_files.append(os.path.join(root, file))
    
    # Inefficiency 8: Checking file sizes inefficiently
    large_logs = []
    for log_file in log_files:
        size = os.path.getsize(log_file)
        if size > 1000000:  # 1MB
            large_logs.append(log_file)
    
    # Inefficiency 9: Another pass for file age
    old_logs = []
    for log_file in log_files:
        mtime = os.path.getmtime(log_file)
        if (datetime.now().timestamp() - mtime) > 86400 * 7:  # 7 days
            old_logs.append(log_file)
    
    return log_files, large_logs, old_logs

def process_all_logs(directory):
    """Process all logs in directory - INEFFICIENT VERSION"""
    
    log_files, large_logs, old_logs = find_log_files(directory)
    
    # Inefficiency 10: Processing files sequentially without considering I/O
    results = {}
    for log_file in log_files:
        try:
            results[log_file] = analyze_logs(log_file)
        except Exception as e:
            print(f"Error processing {log_file}: {e}")
    
    return results

if __name__ == "__main__":
    # Example usage
    print("Log Analyzer - Inefficient Version")
    print("This script has multiple performance issues that need optimization")
