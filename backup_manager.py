#!/usr/bin/env python3
"""
Backup Manager Script
Manages server backups - INEFFICIENT VERSION
"""

import os
import shutil
import hashlib
from datetime import datetime

class BackupManager:
    """Manages server backups with inefficient implementations"""
    
    def __init__(self, source_dir, backup_dir):
        self.source_dir = source_dir
        self.backup_dir = backup_dir
    
    def calculate_checksum(self, filepath):
        """Calculate MD5 checksum - INEFFICIENT"""
        
        # Inefficiency 1: Reading entire file into memory
        with open(filepath, 'rb') as f:
            data = f.read()
            return hashlib.md5(data).hexdigest()
    
    def compare_files(self, file1, file2):
        """Compare two files - INEFFICIENT"""
        
        # Inefficiency 2: Byte-by-byte comparison without buffering
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            byte1 = f1.read(1)
            byte2 = f2.read(1)
            
            while byte1 and byte2:
                if byte1 != byte2:
                    return False
                byte1 = f1.read(1)
                byte2 = f2.read(1)
            
            return byte1 == byte2
    
    def find_duplicates(self, directory):
        """Find duplicate files - INEFFICIENT"""
        
        # Inefficiency 3: Storing all file contents in memory
        files_dict = {}
        
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Inefficiency 4: Multiple passes for same operation
                size = os.path.getsize(filepath)
                checksum = self.calculate_checksum(filepath)
                
                if checksum not in files_dict:
                    files_dict[checksum] = []
                files_dict[checksum].append(filepath)
        
        # Inefficiency 5: Creating new lists unnecessarily
        duplicates = []
        for checksum, paths in files_dict.items():
            if len(paths) > 1:
                for path in paths:
                    duplicates.append(path)
        
        return duplicates
    
    def backup_directory(self, incremental=False):
        """Backup directory - INEFFICIENT"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        
        if not incremental:
            # Inefficiency 6: Full copy without checking if files changed
            shutil.copytree(self.source_dir, backup_path)
        else:
            # Inefficiency 7: Inefficient incremental backup
            os.makedirs(backup_path, exist_ok=True)
            
            for root, dirs, files in os.walk(self.source_dir):
                for filename in files:
                    src_file = os.path.join(root, filename)
                    rel_path = os.path.relpath(src_file, self.source_dir)
                    dst_file = os.path.join(backup_path, rel_path)
                    
                    # Inefficiency 8: Creating directory for each file
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Inefficiency 9: Copying without checking modification time
                    shutil.copy2(src_file, dst_file)
    
    def cleanup_old_backups(self, keep_days=7):
        """Remove old backups - INEFFICIENT"""
        
        # Inefficiency 10: Multiple directory scans
        all_backups = []
        for item in os.listdir(self.backup_dir):
            full_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(full_path):
                all_backups.append(full_path)
        
        # Inefficiency 11: Sorting with custom comparison
        backup_times = []
        for backup in all_backups:
            mtime = os.path.getmtime(backup)
            backup_times.append((mtime, backup))
        
        backup_times.sort()
        
        # Inefficiency 12: Calculating cutoff in loop
        cutoff = datetime.now().timestamp() - (keep_days * 86400)
        
        for mtime, backup in backup_times:
            if mtime < cutoff:
                # Inefficiency 13: Recursive deletion without error handling
                shutil.rmtree(backup)
    
    def generate_report(self):
        """Generate backup report - INEFFICIENT"""
        
        # Inefficiency 14: String concatenation in loop
        report = ""
        report += "Backup Report\n"
        report += "=" * 50 + "\n"
        
        # Inefficiency 15: Multiple scans of same directory
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.backup_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                total_size += os.path.getsize(filepath)
                file_count += 1
        
        report += f"Total Files: {file_count}\n"
        report += f"Total Size: {total_size} bytes\n"
        
        # Another pass for backups count
        backup_count = 0
        for item in os.listdir(self.backup_dir):
            if os.path.isdir(os.path.join(self.backup_dir, item)):
                backup_count += 1
        
        report += f"Number of Backups: {backup_count}\n"
        
        return report

if __name__ == "__main__":
    print("Backup Manager - Inefficient Version")
    print("This script has multiple performance issues that need optimization")
