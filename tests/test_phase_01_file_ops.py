"""
Test Phase 1: File Operations
Tests for Developer Agent file handling capabilities
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.developer import DeveloperAgent


class TestFileOperations:
    """Test suite for file operations."""
    
    @pytest.fixture
    def agent(self):
        """Create a Developer Agent instance for testing."""
        return DeveloperAgent()
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            yield tmpdir
            os.chdir(original_dir)
    
    def test_create_file(self, agent, temp_dir):
        """Test that agent can create a new file."""
        test_content = "print('Hello from test')"
        result = agent.write_code("test.py", test_content)
        
        assert result['success'] == True
        assert os.path.exists("test.py")
        
        with open("test.py", 'r') as f:
            content = f.read()
        assert content == test_content
    
    def test_read_file(self, agent, temp_dir):
        """Test that agent can read an existing file."""
        # Create a file first
        test_content = "Test content for reading"
        with open("test_read.txt", 'w') as f:
            f.write(test_content)
        
        # Read it using the agent
        result = agent.read_file("test_read.txt")
        
        assert result['success'] == True
        assert result['content'] == test_content
    
    def test_edit_file(self, agent, temp_dir):
        """Test that agent can edit an existing file."""
        # Create initial file
        initial_content = "print('Hello')\nprint('World')"
        agent.write_code("test_edit.py", initial_content)
        
        # Edit the file
        result = agent.edit_file(
            "test_edit.py",
            "print('Hello')",
            "print('Goodbye')"
        )
        
        assert result['success'] == True
        
        # Verify the edit
        with open("test_edit.py", 'r') as f:
            content = f.read()
        assert "print('Goodbye')" in content
        assert "print('World')" in content
    
    def test_backup_creation(self, agent, temp_dir):
        """Test that backups are created before editing."""
        # Create initial file
        initial_content = "Original content"
        agent.write_code("test_backup.txt", initial_content)
        
        # Modify the file (should create backup)
        new_content = "Modified content"
        agent.write_code("test_backup.txt", new_content)
        
        # Check that backup was created
        backup_dir = Path("memory/dev/backups")
        assert backup_dir.exists()
        
        backups = list(backup_dir.glob("test_backup_*.txt"))
        assert len(backups) > 0
    
    def test_invalid_file_type(self, agent, temp_dir):
        """Test rejection of invalid file types."""
        result = agent.write_code("test.exe", "binary content")
        
        assert result['success'] == False
        assert "not allowed" in result['error']
        assert not os.path.exists("test.exe")
    
    def test_file_size_limit(self, agent, temp_dir):
        """Test file size limits."""
        # Create content larger than limit
        large_content = "x" * (agent.config['constraints']['max_file_size'] + 1000)
        result = agent.write_code("large.txt", large_content)
        
        assert result['success'] == False
        assert "exceeds maximum" in result['error']
    
    def test_python_syntax_verification(self, agent, temp_dir):
        """Test Python syntax checking before write."""
        # Test with invalid Python syntax
        bad_code = "def test(\n    print('unclosed'"
        result = agent.write_code("bad.py", bad_code)
        
        assert result['success'] == False
        assert "Syntax error" in result['error']
        assert not os.path.exists("bad.py")
        
        # Test with valid Python syntax
        good_code = "def test():\n    print('valid')"
        result = agent.write_code("good.py", good_code)
        
        assert result['success'] == True
        assert os.path.exists("good.py")
    
    def test_create_nested_directories(self, agent, temp_dir):
        """Test creation of nested directory structure."""
        result = agent.write_code("deep/nested/path/file.txt", "nested content")
        
        assert result['success'] == True
        assert os.path.exists("deep/nested/path/file.txt")
    
    def test_read_nonexistent_file(self, agent, temp_dir):
        """Test reading a file that doesn't exist."""
        result = agent.read_file("nonexistent.txt")
        
        assert result['success'] == False
        assert "not found" in result['error']
    
    def test_edit_with_missing_content(self, agent, temp_dir):
        """Test editing when old content doesn't exist."""
        # Create a file
        agent.write_code("test.txt", "Original text")
        
        # Try to edit with non-existent old content
        result = agent.edit_file(
            "test.txt",
            "This doesn't exist",
            "New text"
        )
        
        assert result['success'] == False
        assert "not found in file" in result['error']


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])