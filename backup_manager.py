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
    
    def __init__(self, source_directory, backup_directory):
        self.source_dir_path = source_directory
        self.backup_dir_path = backup_directory
    
    def calculate_checksum(self, file_path):
        """Calculate MD5 checksum - INEFFICIENT"""
        
        # Inefficiency 1: Reading entire file into memory
        with open(file_path, 'rb') as file_handle:
            file_data = file_handle.read()
            return hashlib.md5(file_data).hexdigest()
    
    def compare_files(self, first_file_path, second_file_path):
        """Compare two files - INEFFICIENT"""
        
        # Inefficiency 2: Byte-by-byte comparison without buffering
        with open(first_file_path, 'rb') as first_file_handle, open(second_file_path, 'rb') as second_file_handle:
            first_byte = first_file_handle.read(1)
            second_byte = second_file_handle.read(1)
            
            while first_byte and second_byte:
                if first_byte != second_byte:
                    return False
                first_byte = first_file_handle.read(1)
                second_byte = second_file_handle.read(1)
            
            return first_byte == second_byte
    
    def find_duplicates(self, search_directory):
        """Find duplicate files - INEFFICIENT"""
        
        # Inefficiency 3: Storing all file contents in memory
        checksum_to_files_dict = {}
        
        for root_directory, subdirectories, filenames in os.walk(search_directory):
            for current_filename in filenames:
                file_path = os.path.join(root_directory, current_filename)
                
                # Inefficiency 4: Multiple passes for same operation
                file_size_bytes = os.path.getsize(file_path)
                file_checksum = self.calculate_checksum(file_path)
                
                if file_checksum not in checksum_to_files_dict:
                    checksum_to_files_dict[file_checksum] = []
                checksum_to_files_dict[file_checksum].append(file_path)
        
        # Inefficiency 5: Creating new lists unnecessarily
        duplicate_file_paths = []
        for file_checksum, file_paths in checksum_to_files_dict.items():
            if len(file_paths) > 1:
                for file_path in file_paths:
                    duplicate_file_paths.append(file_path)
        
        return duplicate_file_paths
    
    def backup_directory(self, is_incremental_backup=False):
        """Backup directory - INEFFICIENT"""
        
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_backup_path = os.path.join(self.backup_dir_path, f"backup_{backup_timestamp}")
        
        if not is_incremental_backup:
            # Inefficiency 6: Full copy without checking if files changed
            shutil.copytree(self.source_dir_path, target_backup_path)
        else:
            # Inefficiency 7: Inefficient incremental backup
            os.makedirs(target_backup_path, exist_ok=True)
            
            for root_directory, subdirectories, filenames in os.walk(self.source_dir_path):
                for current_filename in filenames:
                    source_file_path = os.path.join(root_directory, current_filename)
                    relative_file_path = os.path.relpath(source_file_path, self.source_dir_path)
                    destination_file_path = os.path.join(target_backup_path, relative_file_path)
                    
                    # Inefficiency 8: Creating directory for each file
                    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
                    
                    # Inefficiency 9: Copying without checking modification time
                    shutil.copy2(source_file_path, destination_file_path)
    
    def cleanup_old_backups(self, retention_days=7):
        """Remove old backups - INEFFICIENT"""
        
        # Inefficiency 10: Multiple directory scans
        all_backup_paths = []
        for directory_item in os.listdir(self.backup_dir_path):
            full_directory_path = os.path.join(self.backup_dir_path, directory_item)
            if os.path.isdir(full_directory_path):
                all_backup_paths.append(full_directory_path)
        
        # Inefficiency 11: Sorting with custom comparison
        backup_modification_times = []
        for backup_path in all_backup_paths:
            modification_timestamp = os.path.getmtime(backup_path)
            backup_modification_times.append((modification_timestamp, backup_path))
        
        backup_modification_times.sort()
        
        # Inefficiency 12: Calculating cutoff in loop
        age_cutoff_timestamp = datetime.now().timestamp() - (retention_days * 86400)
        
        for modification_timestamp, backup_path in backup_modification_times:
            if modification_timestamp < age_cutoff_timestamp:
                # Inefficiency 13: Recursive deletion without error handling
                shutil.rmtree(backup_path)
    
    def generate_report(self):
        """Generate backup report - INEFFICIENT"""
        
        # Inefficiency 14: String concatenation in loop
        backup_report = ""
        backup_report += "Backup Report\n"
        backup_report += "=" * 50 + "\n"
        
        # Inefficiency 15: Multiple scans of same directory
        total_size_bytes = 0
        total_file_count = 0
        
        for root_directory, subdirectories, filenames in os.walk(self.backup_dir_path):
            for current_filename in filenames:
                file_path = os.path.join(root_directory, current_filename)
                total_size_bytes += os.path.getsize(file_path)
                total_file_count += 1
        
        backup_report += f"Total Files: {total_file_count}\n"
        backup_report += f"Total Size: {total_size_bytes} bytes\n"
        
        # Another pass for backups count
        backup_directory_count = 0
        for directory_item in os.listdir(self.backup_dir_path):
            if os.path.isdir(os.path.join(self.backup_dir_path, directory_item)):
                backup_directory_count += 1
        
        backup_report += f"Number of Backups: {backup_directory_count}\n"
        
        return backup_report

if __name__ == "__main__":
    print("Backup Manager - Inefficient Version")
    print("This script has multiple performance issues that need optimization")
