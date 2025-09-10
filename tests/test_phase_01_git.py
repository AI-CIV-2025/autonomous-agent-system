"""
Test Phase 1: Git Operations
Tests for Developer Agent git management capabilities
"""

import os
import sys
import pytest
import tempfile
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.developer import DeveloperAgent


class TestGitOperations:
    """Test suite for git operations."""
    
    @pytest.fixture
    def agent(self):
        """Create a Developer Agent instance for testing."""
        return DeveloperAgent()
    
    @pytest.fixture
    def temp_git_dir(self):
        """Create a temporary directory with git initialized."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            # Initialize git repo
            subprocess.run(['git', 'init'], capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], capture_output=True)
            
            yield tmpdir
            os.chdir(original_dir)
    
    def test_git_init(self, agent):
        """Test git repository initialization."""
        # Create a temp directory for this specific test
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            result = agent.git_init()
            
            assert result['success'] == True
            assert os.path.exists(".git")
            assert "Initialized" in result['output'] or os.path.isdir(".git")
            
            os.chdir(original_dir)
    
    def test_git_add_single_file(self, agent, temp_git_dir):
        """Test adding a single file to git."""
        # Create a file
        agent.write_code("test.py", "print('test')")
        
        # Add it to git
        result = agent.git_add(["test.py"])
        
        assert result['success'] == True
        assert "test.py" in result['files']
        
        # Verify it's staged
        status = subprocess.run(['git', 'status', '--short'], 
                              capture_output=True, text=True)
        assert "A  test.py" in status.stdout or "test.py" in status.stdout
    
    def test_git_add_multiple_files(self, agent, temp_git_dir):
        """Test adding multiple files to git."""
        # Create multiple files
        agent.write_code("file1.py", "print('1')")
        agent.write_code("file2.py", "print('2')")
        agent.write_code("file3.py", "print('3')")
        
        # Add them to git
        result = agent.git_add(["file1.py", "file2.py", "file3.py"])
        
        assert result['success'] == True
        assert len(result['files']) == 3
    
    def test_git_commit(self, agent, temp_git_dir):
        """Test git commit functionality."""
        # Create and add a file
        agent.write_code("README.md", "# Test Project")
        
        # Commit with files parameter
        result = agent.git_commit("Initial commit", ["README.md"])
        
        assert result['success'] == True
        assert "Initial commit" in result['message']
        
        # Verify commit exists
        log = subprocess.run(['git', 'log', '--oneline'], 
                           capture_output=True, text=True)
        assert "Initial commit" in log.stdout
    
    def test_git_commit_empty(self, agent, temp_git_dir):
        """Test git commit with nothing to commit."""
        # Try to commit without any changes
        result = agent.git_commit("Empty commit")
        
        assert result['success'] == True
        assert "nothing to commit" in result['message'].lower() or "nothing to commit" in result.get('output', '').lower()
    
    def test_git_status(self, agent, temp_git_dir):
        """Test git status command."""
        result = agent.git_status()
        
        assert result['success'] == True
        assert "branch" in result['output'].lower() or "on branch" in result['output'].lower()
    
    def test_git_workflow(self, agent, temp_git_dir):
        """Test complete git workflow."""
        # Create multiple files
        agent.write_code("main.py", "def main():\n    pass")
        agent.write_code("utils.py", "def helper():\n    pass")
        agent.write_code("README.md", "# My Project")
        
        # Add and commit them
        result = agent.git_commit(
            "Add initial project files",
            ["main.py", "utils.py", "README.md"]
        )
        
        assert result['success'] == True
        
        # Modify a file
        agent.edit_file("main.py", "pass", "print('Hello, World!')")
        
        # Commit the change
        result = agent.git_commit("Update main function", ["main.py"])
        
        assert result['success'] == True
        
        # Check git log
        log = subprocess.run(['git', 'log', '--oneline'], 
                           capture_output=True, text=True)
        assert "Update main function" in log.stdout
        assert "Add initial project files" in log.stdout
    
    def test_git_add_nonexistent_file(self, agent, temp_git_dir):
        """Test adding a non-existent file to git."""
        result = agent.git_add(["nonexistent.txt"])
        
        assert result['success'] == False
        assert "failed" in result['error'].lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])