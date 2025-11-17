#!/usr/bin/env python3
"""
Optimized Backup Manager Script
Manages server backups efficiently
"""

import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import filecmp

class BackupManagerOptimized:
    """Manages server backups with optimized implementations"""
    
    def __init__(self, source_directory, backup_directory):
        self.source_dir_path = Path(source_directory)
        self.backup_dir_path = Path(backup_directory)
        self.backup_dir_path.mkdir(parents=True, exist_ok=True)
    
    def calculate_checksum(self, file_path, read_chunk_size=8192):
        """Calculate MD5 checksum - OPTIMIZED"""
        
        # Optimization 1: Read file in chunks instead of all at once
        md5_hash_calculator = hashlib.md5()
        try:
            with open(file_path, 'rb') as file_handle:
                while data_chunk := file_handle.read(read_chunk_size):
                    md5_hash_calculator.update(data_chunk)
            return md5_hash_calculator.hexdigest()
        except IOError:
            return None
    
    def compare_files(self, first_file_path, second_file_path):
        """Compare two files - OPTIMIZED"""
        
        # Optimization 2: Use filecmp module which is optimized for this
        # Also checks size and mtime first before reading content
        return filecmp.cmp(first_file_path, second_file_path, shallow=False)
    
    def find_duplicates(self, search_directory):
        """Find duplicate files - OPTIMIZED"""
        
        # Optimization 3, 4: Group by size first, then checksum
        file_size_to_paths_map = {}
        
        for file_path_object in Path(search_directory).rglob('*'):
            if file_path_object.is_file():
                try:
                    file_size_bytes = file_path_object.stat().st_size
                    if file_size_bytes not in file_size_to_paths_map:
                        file_size_to_paths_map[file_size_bytes] = []
                    file_size_to_paths_map[file_size_bytes].append(file_path_object)
                except OSError:
                    continue
        
        # Only calculate checksums for files with same size
        checksum_to_paths_map = {}
        for file_size_bytes, file_paths in file_size_to_paths_map.items():
            if len(file_paths) > 1:  # Only process potential duplicates
                for file_path_object in file_paths:
                    file_checksum = self.calculate_checksum(file_path_object)
                    if file_checksum:
                        if file_checksum not in checksum_to_paths_map:
                            checksum_to_paths_map[file_checksum] = []
                        checksum_to_paths_map[file_checksum].append(file_path_object)
        
        # Optimization 5: Return dict of lists instead of flat list
        duplicate_files_dict = {checksum: paths for checksum, paths in checksum_to_paths_map.items() if len(paths) > 1}
        return duplicate_files_dict
    
    def backup_directory(self, is_incremental_backup=False):
        """Backup directory - OPTIMIZED"""
        
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_backup_path = self.backup_dir_path / f"backup_{backup_timestamp}"
        
        if not is_incremental_backup:
            # Optimization 6: Check if source changed since last backup
            most_recent_backup = self.get_latest_backup()
            if most_recent_backup and self.directories_identical(self.source_dir_path, most_recent_backup):
                print(f"No changes detected, skipping backup")
                return None
            
            shutil.copytree(self.source_dir_path, target_backup_path, 
                          ignore=shutil.ignore_patterns('*.tmp', '__pycache__', '.git'))
        else:
            # Optimization 7, 8, 9: Efficient incremental backup
            target_backup_path.mkdir(parents=True, exist_ok=True)
            
            # Track created directories to avoid repeated makedirs
            already_created_directories = set()
            
            for source_path_object in self.source_dir_path.rglob('*'):
                if source_path_object.is_file():
                    relative_file_path = source_path_object.relative_to(self.source_dir_path)
                    destination_path_object = target_backup_path / relative_file_path
                    
                    # Create parent directory only if not already created
                    destination_parent_directory = destination_path_object.parent
                    if destination_parent_directory not in already_created_directories:
                        destination_parent_directory.mkdir(parents=True, exist_ok=True)
                        already_created_directories.add(destination_parent_directory)
                    
                    # Check if file needs copying (based on mtime)
                    should_copy_file = True
                    if destination_path_object.exists():
                        source_modification_time = source_path_object.stat().st_mtime
                        destination_modification_time = destination_path_object.stat().st_mtime
                        should_copy_file = source_modification_time > destination_modification_time
                    
                    if should_copy_file:
                        shutil.copy2(source_path_object, destination_path_object)
        
        return target_backup_path
    
    def get_latest_backup(self):
        """Get the most recent backup directory"""
        backup_directories = [directory for directory in self.backup_dir_path.iterdir() 
                  if directory.is_dir() and directory.name.startswith('backup_')]
        if backup_directories:
            return max(backup_directories, key=lambda directory: directory.stat().st_mtime)
        return None
    
    def directories_identical(self, first_directory, second_directory):
        """Check if two directories have identical content"""
        directory_comparison = filecmp.dircmp(first_directory, second_directory)
        if directory_comparison.left_only or directory_comparison.right_only or directory_comparison.diff_files:
            return False
        for common_subdirectory in directory_comparison.common_dirs:
            if not self.directories_identical(
                Path(first_directory) / common_subdirectory, Path(second_directory) / common_subdirectory):
                return False
        return True
    
    def cleanup_old_backups(self, retention_days=7):
        """Remove old backups - OPTIMIZED"""
        
        # Optimization 10, 11, 12: Calculate cutoff once, use scandir
        age_cutoff_timestamp = datetime.now().timestamp() - (retention_days * 86400)
        
        try:
            # Use scandir for efficient directory iteration
            for directory_entry in os.scandir(self.backup_dir_path):
                if directory_entry.is_dir() and directory_entry.name.startswith('backup_'):
                    try:
                        if directory_entry.stat().st_mtime < age_cutoff_timestamp:
                            # Optimization 13: Add error handling
                            shutil.rmtree(directory_entry.path, ignore_errors=False)
                            print(f"Removed old backup: {directory_entry.name}")
                    except (OSError, PermissionError) as file_error:
                        print(f"Error removing {directory_entry.name}: {file_error}")
        except OSError as directory_error:
            print(f"Error scanning backup directory: {directory_error}")
    
    def generate_report(self):
        """Generate backup report - OPTIMIZED"""
        
        # Optimization 14, 15: Single walk with efficient string building
        total_size_bytes = 0
        total_file_count = 0
        backup_directory_count = 0
        
        # Count backups and collect stats in one pass
        try:
            for directory_entry in os.scandir(self.backup_dir_path):
                if directory_entry.is_dir() and directory_entry.name.startswith('backup_'):
                    backup_directory_count += 1
                    
                    # Walk each backup directory
                    for root_directory, subdirectories, filenames in os.walk(directory_entry.path):
                        for current_filename in filenames:
                            try:
                                file_path = os.path.join(root_directory, current_filename)
                                total_size_bytes += os.path.getsize(file_path)
                                total_file_count += 1
                            except OSError:
                                continue
        except OSError as directory_error:
            return f"Error generating report: {directory_error}"
        
        # Use f-string for efficient formatting
        backup_report = (
            f"Backup Report\n"
            f"{'='*50}\n"
            f"Total Files: {total_file_count}\n"
            f"Total Size: {total_size_bytes:,} bytes ({total_size_bytes / (1024**3):.2f} GB)\n"
            f"Number of Backups: {backup_directory_count}\n"
        )
        
        return backup_report
    
    def verify_backup_integrity(self, backup_path_to_verify):
        """Verify backup integrity by comparing checksums"""
        integrity_mismatches = []
        
        for source_path_object in self.source_dir_path.rglob('*'):
            if source_path_object.is_file():
                relative_file_path = source_path_object.relative_to(self.source_dir_path)
                backed_up_file_path = Path(backup_path_to_verify) / relative_file_path
                
                if not backed_up_file_path.exists():
                    integrity_mismatches.append(f"Missing: {relative_file_path}")
                elif not self.compare_files(source_path_object, backed_up_file_path):
                    integrity_mismatches.append(f"Mismatch: {relative_file_path}")
        
        return integrity_mismatches

if __name__ == "__main__":
    print("Backup Manager - Optimized Version")
    print("\nKey optimizations:")
    print("- Chunked file reading for checksums")
    print("- Size comparison before checksum calculation")
    print("- Efficient directory scanning with os.scandir()")
    print("- Modification time checks before copying")
    print("- Single-pass statistics collection")
    print("- Proper error handling")
    print("- Use of pathlib for cleaner path operations")
