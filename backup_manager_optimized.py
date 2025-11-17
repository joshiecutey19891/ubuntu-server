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
    
    def __init__(self, source_dir, backup_dir):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_checksum(self, filepath, chunk_size=8192):
        """Calculate MD5 checksum - OPTIMIZED"""
        
        # Optimization 1: Read file in chunks instead of all at once
        md5_hash = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5_hash.update(chunk)
            return md5_hash.hexdigest()
        except IOError:
            return None
    
    def compare_files(self, file1, file2):
        """Compare two files - OPTIMIZED"""
        
        # Optimization 2: Use filecmp module which is optimized for this
        # Also checks size and mtime first before reading content
        return filecmp.cmp(file1, file2, shallow=False)
    
    def find_duplicates(self, directory):
        """Find duplicate files - OPTIMIZED"""
        
        # Optimization 3, 4: Group by size first, then checksum
        size_map = {}
        
        for filepath in Path(directory).rglob('*'):
            if filepath.is_file():
                try:
                    size = filepath.stat().st_size
                    if size not in size_map:
                        size_map[size] = []
                    size_map[size].append(filepath)
                except OSError:
                    continue
        
        # Only calculate checksums for files with same size
        checksum_map = {}
        for size, files in size_map.items():
            if len(files) > 1:  # Only process potential duplicates
                for filepath in files:
                    checksum = self.calculate_checksum(filepath)
                    if checksum:
                        if checksum not in checksum_map:
                            checksum_map[checksum] = []
                        checksum_map[checksum].append(filepath)
        
        # Optimization 5: Return dict of lists instead of flat list
        duplicates = {k: v for k, v in checksum_map.items() if len(v) > 1}
        return duplicates
    
    def backup_directory(self, incremental=False):
        """Backup directory - OPTIMIZED"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        
        if not incremental:
            # Optimization 6: Check if source changed since last backup
            latest_backup = self.get_latest_backup()
            if latest_backup and self.directories_identical(self.source_dir, latest_backup):
                print(f"No changes detected, skipping backup")
                return None
            
            shutil.copytree(self.source_dir, backup_path, 
                          ignore=shutil.ignore_patterns('*.tmp', '__pycache__', '.git'))
        else:
            # Optimization 7, 8, 9: Efficient incremental backup
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Track created directories to avoid repeated makedirs
            created_dirs = set()
            
            for src_path in self.source_dir.rglob('*'):
                if src_path.is_file():
                    rel_path = src_path.relative_to(self.source_dir)
                    dst_path = backup_path / rel_path
                    
                    # Create parent directory only if not already created
                    dst_parent = dst_path.parent
                    if dst_parent not in created_dirs:
                        dst_parent.mkdir(parents=True, exist_ok=True)
                        created_dirs.add(dst_parent)
                    
                    # Check if file needs copying (based on mtime)
                    should_copy = True
                    if dst_path.exists():
                        src_mtime = src_path.stat().st_mtime
                        dst_mtime = dst_path.stat().st_mtime
                        should_copy = src_mtime > dst_mtime
                    
                    if should_copy:
                        shutil.copy2(src_path, dst_path)
        
        return backup_path
    
    def get_latest_backup(self):
        """Get the most recent backup directory"""
        backups = [d for d in self.backup_dir.iterdir() 
                  if d.is_dir() and d.name.startswith('backup_')]
        if backups:
            return max(backups, key=lambda d: d.stat().st_mtime)
        return None
    
    def directories_identical(self, dir1, dir2):
        """Check if two directories have identical content"""
        cmp = filecmp.dircmp(dir1, dir2)
        if cmp.left_only or cmp.right_only or cmp.diff_files:
            return False
        for subdir in cmp.common_dirs:
            if not self.directories_identical(
                Path(dir1) / subdir, Path(dir2) / subdir):
                return False
        return True
    
    def cleanup_old_backups(self, keep_days=7):
        """Remove old backups - OPTIMIZED"""
        
        # Optimization 10, 11, 12: Calculate cutoff once, use scandir
        cutoff = datetime.now().timestamp() - (keep_days * 86400)
        
        try:
            # Use scandir for efficient directory iteration
            for entry in os.scandir(self.backup_dir):
                if entry.is_dir() and entry.name.startswith('backup_'):
                    try:
                        if entry.stat().st_mtime < cutoff:
                            # Optimization 13: Add error handling
                            shutil.rmtree(entry.path, ignore_errors=False)
                            print(f"Removed old backup: {entry.name}")
                    except (OSError, PermissionError) as e:
                        print(f"Error removing {entry.name}: {e}")
        except OSError as e:
            print(f"Error scanning backup directory: {e}")
    
    def generate_report(self):
        """Generate backup report - OPTIMIZED"""
        
        # Optimization 14, 15: Single walk with efficient string building
        total_size = 0
        file_count = 0
        backup_count = 0
        
        # Count backups and collect stats in one pass
        try:
            for entry in os.scandir(self.backup_dir):
                if entry.is_dir() and entry.name.startswith('backup_'):
                    backup_count += 1
                    
                    # Walk each backup directory
                    for root, dirs, files in os.walk(entry.path):
                        for filename in files:
                            try:
                                filepath = os.path.join(root, filename)
                                total_size += os.path.getsize(filepath)
                                file_count += 1
                            except OSError:
                                continue
        except OSError as e:
            return f"Error generating report: {e}"
        
        # Use f-string for efficient formatting
        report = (
            f"Backup Report\n"
            f"{'='*50}\n"
            f"Total Files: {file_count}\n"
            f"Total Size: {total_size:,} bytes ({total_size / (1024**3):.2f} GB)\n"
            f"Number of Backups: {backup_count}\n"
        )
        
        return report
    
    def verify_backup_integrity(self, backup_path):
        """Verify backup integrity by comparing checksums"""
        mismatches = []
        
        for src_path in self.source_dir.rglob('*'):
            if src_path.is_file():
                rel_path = src_path.relative_to(self.source_dir)
                backup_file = Path(backup_path) / rel_path
                
                if not backup_file.exists():
                    mismatches.append(f"Missing: {rel_path}")
                elif not self.compare_files(src_path, backup_file):
                    mismatches.append(f"Mismatch: {rel_path}")
        
        return mismatches

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
