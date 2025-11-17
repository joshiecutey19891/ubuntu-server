#!/usr/bin/env python3
"""
Log Analyzer Script
Analyzes server logs for errors and patterns
"""

import os
import re
from datetime import datetime

def analyze_logs(log_file_path):
    """Analyze log file for errors - INEFFICIENT VERSION"""
    
    # Inefficiency 1: Reading entire file into memory
    with open(log_file_path, 'r') as log_file_handle:
        all_log_lines = log_file_handle.readlines()
    
    error_messages = []
    warning_messages = []
    info_messages = []
    
    # Inefficiency 2: Multiple passes over the same data
    for log_line in all_log_lines:
        if 'ERROR' in log_line:
            error_messages.append(log_line)
    
    for log_line in all_log_lines:
        if 'WARNING' in log_line:
            warning_messages.append(log_line)
    
    for log_line in all_log_lines:
        if 'INFO' in log_line:
            info_messages.append(log_line)
    
    # Inefficiency 3: Inefficient string concatenation in loop
    analysis_report = ""
    analysis_report += "="*50 + "\n"
    analysis_report += "Log Analysis Report\n"
    analysis_report += "="*50 + "\n"
    analysis_report += f"Total Errors: {len(error_messages)}\n"
    analysis_report += f"Total Warnings: {len(warning_messages)}\n"
    analysis_report += f"Total Info: {len(info_messages)}\n"
    analysis_report += "="*50 + "\n"
    
    # Inefficiency 4: Nested loops with O(n²) complexity
    duplicate_error_messages = []
    for error_index in range(len(error_messages)):
        for comparison_index in range(error_index+1, len(error_messages)):
            if error_messages[error_index] == error_messages[comparison_index]:
                if error_messages[error_index] not in duplicate_error_messages:
                    duplicate_error_messages.append(error_messages[error_index])
    
    analysis_report += f"Duplicate Errors: {len(duplicate_error_messages)}\n"
    
    # Inefficiency 5: Using regex in tight loop
    extracted_error_codes = []
    for error_message in error_messages:
        error_code_match = re.search(r'ERROR\s+(\d+)', error_message)
        if error_code_match:
            extracted_error_codes.append(error_code_match.group(1))
    
    # Inefficiency 6: Sorting without considering memory
    sorted_error_messages = sorted(error_messages)
    sorted_warning_messages = sorted(warning_messages)
    
    return analysis_report

def find_log_files(search_directory):
    """Find all log files - INEFFICIENT VERSION"""
    
    # Inefficiency 7: Walking entire directory tree multiple times
    discovered_log_files = []
    
    for root_directory, subdirectories, filenames in os.walk(search_directory):
        for current_filename in filenames:
            if current_filename.endswith('.log'):
                discovered_log_files.append(os.path.join(root_directory, current_filename))
    
    # Inefficiency 8: Checking file sizes inefficiently
    large_log_files = []
    for log_file_path in discovered_log_files:
        file_size_bytes = os.path.getsize(log_file_path)
        if file_size_bytes > 1000000:  # 1MB
            large_log_files.append(log_file_path)
    
    # Inefficiency 9: Another pass for file age
    old_log_files = []
    for log_file_path in discovered_log_files:
        file_modification_time = os.path.getmtime(log_file_path)
        if (datetime.now().timestamp() - file_modification_time) > 86400 * 7:  # 7 days
            old_log_files.append(log_file_path)
    
    return discovered_log_files, large_log_files, old_log_files

def process_all_logs(search_directory):
    """Process all logs in directory - INEFFICIENT VERSION"""
    
    discovered_log_files, large_log_files, old_log_files = find_log_files(search_directory)
    
    # Inefficiency 10: Processing files sequentially without considering I/O
    analysis_results = {}
    for log_file_path in discovered_log_files:
        try:
            analysis_results[log_file_path] = analyze_logs(log_file_path)
        except Exception as error_exception:
            print(f"Error processing {log_file_path}: {error_exception}")
    
    return analysis_results

if __name__ == "__main__":
    # Example usage
    print("Log Analyzer - Inefficient Version")
    print("This script has multiple performance issues that need optimization")
