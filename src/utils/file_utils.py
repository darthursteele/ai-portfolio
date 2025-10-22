"""
File utilities for AI Portfolio project.
"""

import os
import json
import csv
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, TextIO
from datetime import datetime

from ..config.settings import Settings
from .logging_utils import get_logger


class FileUtils:
    """Utility class for file operations."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize file utilities.
        
        Args:
            settings: Application settings
        """
        self.settings = settings or Settings()
        self.logger = get_logger("file_utils")
    
    @staticmethod
    def ensure_directory(directory: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if it doesn't.
        
        Args:
            directory: Directory path
            
        Returns:
            Path object for the directory
        """
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    @staticmethod
    def safe_filename(filename: str, max_length: int = 255) -> str:
        """
        Create a safe filename by removing/replacing invalid characters.
        
        Args:
            filename: Original filename
            max_length: Maximum filename length
            
        Returns:
            Safe filename
        """
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        safe_name = filename
        
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Remove multiple consecutive underscores
        while '__' in safe_name:
            safe_name = safe_name.replace('__', '_')
        
        # Trim to max length
        if len(safe_name) > max_length:
            name, ext = os.path.splitext(safe_name)
            max_name_length = max_length - len(ext)
            safe_name = name[:max_name_length] + ext
        
        return safe_name.strip('_')
    
    @staticmethod
    def get_file_hash(filepath: Union[str, Path], algorithm: str = 'md5') -> str:
        """
        Calculate hash of a file.
        
        Args:
            filepath: Path to file
            algorithm: Hashing algorithm ('md5', 'sha1', 'sha256')
            
        Returns:
            File hash as hexadecimal string
        """
        hash_func = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def validate_file_type(self, filepath: Union[str, Path]) -> bool:
        """
        Validate if file type is allowed.
        
        Args:
            filepath: Path to file
            
        Returns:
            True if file type is allowed
        """
        file_path = Path(filepath)
        extension = file_path.suffix.lower().lstrip('.')
        
        return extension in self.settings.allowed_file_types
    
    def validate_file_size(self, filepath: Union[str, Path]) -> bool:
        """
        Validate if file size is within limits.
        
        Args:
            filepath: Path to file
            
        Returns:
            True if file size is within limits
        """
        file_size = Path(filepath).stat().st_size
        return file_size <= self.settings.max_file_size
    
    def read_text_file(self, filepath: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Read text file content.
        
        Args:
            filepath: Path to file
            encoding: File encoding
            
        Returns:
            File content as string
        """
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            
            self.logger.debug(f"Read text file: {filepath}")
            return content
            
        except Exception as e:
            self.logger.error(f"Error reading file {filepath}: {e}")
            raise
    
    def write_text_file(
        self,
        content: str,
        filepath: Union[str, Path],
        encoding: str = 'utf-8',
        ensure_dir: bool = True
    ) -> None:
        """
        Write content to text file.
        
        Args:
            content: Content to write
            filepath: Path to file
            encoding: File encoding
            ensure_dir: Whether to create directory if it doesn't exist
        """
        file_path = Path(filepath)
        
        if ensure_dir:
            self.ensure_directory(file_path.parent)
        
        try:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self.logger.debug(f"Wrote text file: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error writing file {filepath}: {e}")
            raise
    
    def read_json_file(self, filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.debug(f"Read JSON file: {filepath}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error reading JSON file {filepath}: {e}")
            raise
    
    def write_json_file(
        self,
        data: Dict[str, Any],
        filepath: Union[str, Path],
        indent: int = 2,
        ensure_dir: bool = True
    ) -> None:
        """
        Write data to JSON file.
        
        Args:
            data: Data to write
            filepath: Path to file
            indent: JSON indentation
            ensure_dir: Whether to create directory if it doesn't exist
        """
        file_path = Path(filepath)
        
        if ensure_dir:
            self.ensure_directory(file_path.parent)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=str)
            
            self.logger.debug(f"Wrote JSON file: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error writing JSON file {filepath}: {e}")
            raise
    
    def read_csv_file(
        self,
        filepath: Union[str, Path],
        delimiter: str = ',',
        has_header: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Read CSV file.
        
        Args:
            filepath: Path to CSV file
            delimiter: CSV delimiter
            has_header: Whether CSV has header row
            
        Returns:
            List of dictionaries representing rows
        """
        try:
            rows = []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                if has_header:
                    reader = csv.DictReader(f, delimiter=delimiter)
                    rows = list(reader)
                else:
                    reader = csv.reader(f, delimiter=delimiter)
                    rows = [{"col_" + str(i): value for i, value in enumerate(row)} 
                           for row in reader]
            
            self.logger.debug(f"Read CSV file: {filepath}")
            return rows
            
        except Exception as e:
            self.logger.error(f"Error reading CSV file {filepath}: {e}")
            raise
    
    def write_csv_file(
        self,
        data: List[Dict[str, Any]],
        filepath: Union[str, Path],
        delimiter: str = ',',
        ensure_dir: bool = True
    ) -> None:
        """
        Write data to CSV file.
        
        Args:
            data: List of dictionaries to write
            filepath: Path to file
            delimiter: CSV delimiter
            ensure_dir: Whether to create directory if it doesn't exist
        """
        if not data:
            raise ValueError("No data to write")
        
        file_path = Path(filepath)
        
        if ensure_dir:
            self.ensure_directory(file_path.parent)
        
        try:
            fieldnames = data[0].keys()
            
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.debug(f"Wrote CSV file: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file {filepath}: {e}")
            raise
    
    def backup_file(self, filepath: Union[str, Path], backup_dir: Optional[str] = None) -> Path:
        """
        Create a backup of a file.
        
        Args:
            filepath: Path to file to backup
            backup_dir: Directory to store backup (defaults to backups/)
            
        Returns:
            Path to backup file
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if backup_dir is None:
            backup_dir = Path("backups")
        else:
            backup_dir = Path(backup_dir)
        
        self.ensure_directory(backup_dir)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        # Copy file
        import shutil
        shutil.copy2(file_path, backup_path)
        
        self.logger.info(f"Created backup: {backup_path}")
        return backup_path
    
    def cleanup_old_files(
        self,
        directory: Union[str, Path],
        max_age_days: int,
        pattern: str = "*",
        dry_run: bool = False
    ) -> List[Path]:
        """
        Clean up old files in a directory.
        
        Args:
            directory: Directory to clean
            max_age_days: Maximum file age in days
            pattern: File pattern to match
            dry_run: If True, only return files that would be deleted
            
        Returns:
            List of files that were (or would be) deleted
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return []
        
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)
        deleted_files = []
        
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                file_mtime = file_path.stat().st_mtime
                
                if file_mtime < cutoff_time:
                    deleted_files.append(file_path)
                    
                    if not dry_run:
                        try:
                            file_path.unlink()
                            self.logger.debug(f"Deleted old file: {file_path}")
                        except Exception as e:
                            self.logger.error(f"Error deleting file {file_path}: {e}")
        
        if dry_run:
            self.logger.info(f"Would delete {len(deleted_files)} old files")
        else:
            self.logger.info(f"Deleted {len(deleted_files)} old files")
        
        return deleted_files
    
    @staticmethod
    def get_file_info(filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Get comprehensive file information.
        
        Args:
            filepath: Path to file
            
        Returns:
            Dictionary with file information
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = file_path.stat()
        
        return {
            "name": file_path.name,
            "stem": file_path.stem,
            "suffix": file_path.suffix,
            "size": stat.st_size,
            "size_human": FileUtils._format_bytes(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir(),
            "absolute_path": str(file_path.absolute()),
            "parent": str(file_path.parent)
        }
    
    @staticmethod
    def _format_bytes(bytes_size: int) -> str:
        """Format bytes size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"