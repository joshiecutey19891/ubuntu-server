#!/usr/bin/env python3
"""
Unit tests for optimized scripts
"""

import unittest
import tempfile
import os
from pathlib import Path
from log_analyzer_optimized import analyze_logs, find_log_files
from backup_manager_optimized import BackupManagerOptimized


class TestLogAnalyzer(unittest.TestCase):
    """Test cases for log analyzer"""
    
    def setUp(self):
        """Create test log file"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False)
        self.test_file.write("2024-01-01 10:00:00 INFO: Test message 1\n")
        self.test_file.write("2024-01-01 10:00:01 ERROR 500: Test error\n")
        self.test_file.write("2024-01-01 10:00:02 WARNING: Test warning\n")
        self.test_file.write("2024-01-01 10:00:03 INFO: Test message 2\n")
        self.test_file.write("2024-01-01 10:00:04 ERROR 404: Another error\n")
        self.test_file.close()
    
    def tearDown(self):
        """Clean up test file"""
        os.unlink(self.test_file.name)
    
    def test_analyze_logs_counts(self):
        """Test that log analysis counts messages correctly"""
        result = analyze_logs(self.test_file.name)
        self.assertIn("Total Errors: 2", result)
        self.assertIn("Total Warnings: 1", result)
        self.assertIn("Total Info: 2", result)
    
    def test_analyze_logs_report_format(self):
        """Test that report has correct format"""
        result = analyze_logs(self.test_file.name)
        self.assertIn("Log Analysis Report", result)
        self.assertIn("="*50, result)
    
    def test_find_log_files(self):
        """Test log file discovery"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test log files
            log1 = Path(tmpdir) / "test1.log"
            log2 = Path(tmpdir) / "test2.log"
            log1.write_text("test")
            log2.write_text("test")
            
            log_files, large_logs, old_logs = find_log_files(tmpdir)
            self.assertEqual(len(log_files), 2)


class TestBackupManager(unittest.TestCase):
    """Test cases for backup manager"""
    
    def setUp(self):
        """Create test directories"""
        self.tmpdir = tempfile.mkdtemp()
        self.source = Path(self.tmpdir) / "source"
        self.backup = Path(self.tmpdir) / "backup"
        self.source.mkdir()
        
        # Create test files
        (self.source / "file1.txt").write_text("Content 1")
        (self.source / "file2.txt").write_text("Content 2")
        
        self.bm = BackupManagerOptimized(self.source, self.backup)
    
    def tearDown(self):
        """Clean up test directories"""
        import shutil
        shutil.rmtree(self.tmpdir)
    
    def test_backup_creation(self):
        """Test that backup is created successfully"""
        result = self.bm.backup_directory()
        self.assertIsNotNone(result)
        self.assertTrue(result.exists())
        
        # Check files were copied
        backed_up_files = list(result.rglob("*.txt"))
        self.assertEqual(len(backed_up_files), 2)
    
    def test_checksum_calculation(self):
        """Test checksum calculation with chunking"""
        test_file = self.source / "file1.txt"
        checksum = self.bm.calculate_checksum(test_file)
        self.assertIsNotNone(checksum)
        self.assertEqual(len(checksum), 32)  # MD5 is 32 hex chars
    
    def test_report_generation(self):
        """Test backup report generation"""
        self.bm.backup_directory()
        report = self.bm.generate_report()
        self.assertIn("Backup Report", report)
        self.assertIn("Total Files:", report)
        self.assertIn("Number of Backups:", report)
    
    def test_file_comparison(self):
        """Test file comparison"""
        file1 = self.source / "file1.txt"
        file2 = self.source / "file2.txt"
        
        # Same file should match itself
        self.assertTrue(self.bm.compare_files(file1, file1))
        
        # Different files should not match
        self.assertFalse(self.bm.compare_files(file1, file2))
    
    def test_find_duplicates(self):
        """Test duplicate file detection"""
        # Create a duplicate
        (self.source / "file3.txt").write_text("Content 1")
        
        duplicates = self.bm.find_duplicates(self.source)
        # Should find at least one set of duplicates
        self.assertGreater(len(duplicates), 0)


class TestPerformanceOptimizations(unittest.TestCase):
    """Test that optimizations don't break functionality"""
    
    def test_large_log_file_memory_efficiency(self):
        """Test that large log files don't cause memory issues"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            # Write 10,000 lines
            for i in range(10000):
                f.write(f"2024-01-01 10:00:{i:02d} INFO: Message {i}\n")
                if i % 100 == 0:
                    f.write(f"2024-01-01 10:00:{i:02d} ERROR 500: Error {i}\n")
            f.flush()
            
            # Should process without issues
            result = analyze_logs(f.name)
            self.assertIn("Total Errors:", result)
            self.assertIn("Total Info:", result)
            
            os.unlink(f.name)
    
    def test_many_files_backup(self):
        """Test backup with many files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            backup = Path(tmpdir) / "backup"
            source.mkdir()
            
            # Create 100 files
            for i in range(100):
                (source / f"file{i}.txt").write_text(f"Content {i}")
            
            bm = BackupManagerOptimized(source, backup)
            result = bm.backup_directory()
            
            # Verify all files were backed up
            backed_up = len(list(result.rglob("*.txt")))
            self.assertEqual(backed_up, 100)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
