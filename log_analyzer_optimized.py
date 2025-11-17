#!/usr/bin/env python3
"""
Optimized Log Analyzer Script
Analyzes server logs for errors and patterns efficiently
"""

import os
import re
from datetime import datetime
from collections import Counter, defaultdict
from io import StringIO

# Optimization 5: Compile regex once outside functions
ERROR_CODE_PATTERN = re.compile(r'ERROR\s+(\d+)')

def analyze_logs(log_file_path):
    """Analyze log file for errors - OPTIMIZED VERSION"""
    
    error_messages = []
    warning_messages = []
    info_messages = []
    extracted_error_codes = []
    
    # Optimization 1 & 2: Single pass, line-by-line processing (no memory load)
    try:
        with open(log_file_path, 'r') as log_file_handle:
            for log_line in log_file_handle:
                log_line = log_line.rstrip('\n')
                
                if 'ERROR' in log_line:
                    error_messages.append(log_line)
                    # Optimization 5: Use pre-compiled regex
                    error_code_match = ERROR_CODE_PATTERN.search(log_line)
                    if error_code_match:
                        extracted_error_codes.append(error_code_match.group(1))
                elif 'WARNING' in log_line:
                    warning_messages.append(log_line)
                elif 'INFO' in log_line:
                    info_messages.append(log_line)
    except IOError as io_error:
        return f"Error reading file: {io_error}"
    
    # Optimization 3: Use StringIO or list+join for string building
    report_sections = [
        "=" * 50,
        "Log Analysis Report",
        "=" * 50,
        f"Total Errors: {len(error_messages)}",
        f"Total Warnings: {len(warning_messages)}",
        f"Total Info: {len(info_messages)}",
        "=" * 50,
    ]
    
    # Optimization 4: Use Counter for duplicate detection (O(n) instead of O(n²))
    error_frequency_counter = Counter(error_messages)
    duplicate_error_type_count = sum(1 for frequency in error_frequency_counter.values() if frequency > 1)
    report_sections.append(f"Duplicate Error Types: {duplicate_error_type_count}")
    
    # Join all parts efficiently
    analysis_report = '\n'.join(report_sections)
    
    return analysis_report

def find_log_files(search_directory):
    """Find all log files - OPTIMIZED VERSION"""
    
    discovered_log_files = []
    large_log_files = []
    old_log_files = []
    
    age_cutoff_timestamp = datetime.now().timestamp() - (86400 * 7)  # 7 days
    
    # Optimization 7, 8, 9: Single directory walk with all checks
    try:
        for root_directory, subdirectories, filenames in os.walk(search_directory):
            for current_filename in filenames:
                if current_filename.endswith('.log'):
                    log_file_path = os.path.join(root_directory, current_filename)
                    
                    # Get file stats once (combines size and mtime check)
                    try:
                        file_statistics = os.stat(log_file_path)
                        discovered_log_files.append(log_file_path)
                        
                        if file_statistics.st_size > 1000000:  # 1MB
                            large_log_files.append(log_file_path)
                        
                        if file_statistics.st_mtime < age_cutoff_timestamp:
                            old_log_files.append(log_file_path)
                    except OSError:
                        continue  # Skip files we can't access
    except OSError as os_error:
        print(f"Error walking directory: {os_error}")
    
    return discovered_log_files, large_log_files, old_log_files

def process_all_logs(search_directory):
    """Process all logs in directory - OPTIMIZED VERSION"""
    
    discovered_log_files, large_log_files, old_log_files = find_log_files(search_directory)
    
    # Optimization 10: Could add multiprocessing for truly parallel processing
    # For now, keeping sequential but with optimized individual processing
    analysis_results = {}
    for log_file_path in discovered_log_files:
        try:
            analysis_results[log_file_path] = analyze_logs(log_file_path)
        except Exception as processing_exception:
            analysis_results[log_file_path] = f"Error processing: {processing_exception}"
    
    return analysis_results

def analyze_logs_streaming(log_file_path, read_chunk_size=8192):
    """
    Alternative streaming version for very large files
    Processes file in chunks without storing all lines
    """
    error_message_count = 0
    warning_message_count = 0
    info_message_count = 0
    extracted_error_codes = []
    
    try:
        with open(log_file_path, 'r', buffering=read_chunk_size) as log_file_handle:
            for log_line in log_file_handle:
                if 'ERROR' in log_line:
                    error_message_count += 1
                    error_code_match = ERROR_CODE_PATTERN.search(log_line)
                    if error_code_match:
                        extracted_error_codes.append(error_code_match.group(1))
                elif 'WARNING' in log_line:
                    warning_message_count += 1
                elif 'INFO' in log_line:
                    info_message_count += 1
    except IOError as io_error:
        return f"Error reading file: {io_error}"
    
    streaming_analysis_report = (
        f"{'='*50}\n"
        f"Log Analysis Report (Streaming)\n"
        f"{'='*50}\n"
        f"Total Errors: {error_message_count}\n"
        f"Total Warnings: {warning_message_count}\n"
        f"Total Info: {info_message_count}\n"
        f"{'='*50}"
    )
    
    return streaming_analysis_report

if __name__ == "__main__":
    print("Log Analyzer - Optimized Version")
    print("Key optimizations:")
    print("- Single-pass file processing")
    print("- Line-by-line reading (no memory load)")
    print("- Pre-compiled regex patterns")
    print("- Efficient string building")
    print("- O(n) duplicate detection with Counter")
    print("- Single directory walk with combined checks")
