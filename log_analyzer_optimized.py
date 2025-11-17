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

def analyze_logs(log_file):
    """Analyze log file for errors - OPTIMIZED VERSION"""
    
    errors = []
    warnings = []
    info = []
    error_codes = []
    
    # Optimization 1 & 2: Single pass, line-by-line processing (no memory load)
    try:
        with open(log_file, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                
                if 'ERROR' in line:
                    errors.append(line)
                    # Optimization 5: Use pre-compiled regex
                    match = ERROR_CODE_PATTERN.search(line)
                    if match:
                        error_codes.append(match.group(1))
                elif 'WARNING' in line:
                    warnings.append(line)
                elif 'INFO' in line:
                    info.append(line)
    except IOError as e:
        return f"Error reading file: {e}"
    
    # Optimization 3: Use StringIO or list+join for string building
    report_parts = [
        "=" * 50,
        "Log Analysis Report",
        "=" * 50,
        f"Total Errors: {len(errors)}",
        f"Total Warnings: {len(warnings)}",
        f"Total Info: {len(info)}",
        "=" * 50,
    ]
    
    # Optimization 4: Use Counter for duplicate detection (O(n) instead of O(n²))
    error_counter = Counter(errors)
    duplicate_count = sum(1 for count in error_counter.values() if count > 1)
    report_parts.append(f"Duplicate Error Types: {duplicate_count}")
    
    # Join all parts efficiently
    report = '\n'.join(report_parts)
    
    return report

def find_log_files(directory):
    """Find all log files - OPTIMIZED VERSION"""
    
    log_files = []
    large_logs = []
    old_logs = []
    
    cutoff_time = datetime.now().timestamp() - (86400 * 7)  # 7 days
    
    # Optimization 7, 8, 9: Single directory walk with all checks
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.log'):
                    filepath = os.path.join(root, file)
                    
                    # Get file stats once (combines size and mtime check)
                    try:
                        stat = os.stat(filepath)
                        log_files.append(filepath)
                        
                        if stat.st_size > 1000000:  # 1MB
                            large_logs.append(filepath)
                        
                        if stat.st_mtime < cutoff_time:
                            old_logs.append(filepath)
                    except OSError:
                        continue  # Skip files we can't access
    except OSError as e:
        print(f"Error walking directory: {e}")
    
    return log_files, large_logs, old_logs

def process_all_logs(directory):
    """Process all logs in directory - OPTIMIZED VERSION"""
    
    log_files, large_logs, old_logs = find_log_files(directory)
    
    # Optimization 10: Could add multiprocessing for truly parallel processing
    # For now, keeping sequential but with optimized individual processing
    results = {}
    for log_file in log_files:
        try:
            results[log_file] = analyze_logs(log_file)
        except Exception as e:
            results[log_file] = f"Error processing: {e}"
    
    return results

def analyze_logs_streaming(log_file, chunk_size=8192):
    """
    Alternative streaming version for very large files
    Processes file in chunks without storing all lines
    """
    error_count = 0
    warning_count = 0
    info_count = 0
    error_codes = []
    
    try:
        with open(log_file, 'r', buffering=chunk_size) as f:
            for line in f:
                if 'ERROR' in line:
                    error_count += 1
                    match = ERROR_CODE_PATTERN.search(line)
                    if match:
                        error_codes.append(match.group(1))
                elif 'WARNING' in line:
                    warning_count += 1
                elif 'INFO' in line:
                    info_count += 1
    except IOError as e:
        return f"Error reading file: {e}"
    
    report = (
        f"{'='*50}\n"
        f"Log Analysis Report (Streaming)\n"
        f"{'='*50}\n"
        f"Total Errors: {error_count}\n"
        f"Total Warnings: {warning_count}\n"
        f"Total Info: {info_count}\n"
        f"{'='*50}"
    )
    
    return report

if __name__ == "__main__":
    print("Log Analyzer - Optimized Version")
    print("Key optimizations:")
    print("- Single-pass file processing")
    print("- Line-by-line reading (no memory load)")
    print("- Pre-compiled regex patterns")
    print("- Efficient string building")
    print("- O(n) duplicate detection with Counter")
    print("- Single directory walk with combined checks")
