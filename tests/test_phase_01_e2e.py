"""
Test Phase 1: End-to-End Tests
Complete workflow tests for Developer Agent
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


class TestEndToEnd:
    """End-to-end test suite for Developer Agent."""
    
    @pytest.fixture
    def agent(self):
        """Create a Developer Agent instance for testing."""
        return DeveloperAgent()
    
    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            
            # Set up git config
            subprocess.run(['git', 'config', '--global', 'user.email', 'test@example.com'], 
                         capture_output=True)
            subprocess.run(['git', 'config', '--global', 'user.name', 'Test User'], 
                         capture_output=True)
            
            yield tmpdir
            os.chdir(original_dir)
    
    def test_hello_world_project(self, agent, temp_workspace):
        """Complete Hello World project creation."""
        # Create project
        result = agent.create_project("hello_world")
        assert result['success'] == True
        
        # Change to project directory
        os.chdir("hello_world")
        
        # Initialize git
        git_result = agent.git_init()
        assert git_result['success'] == True
        
        # Write main program
        main_code = """#!/usr/bin/env python3
\"\"\"
Hello World Program
Created by Developer Agent
\"\"\"

def main():
    \"\"\"Main function.\"\"\"
    print('Hello, World!')
    print('This project was created by the Developer Agent')
    return 0

if __name__ == '__main__':
    exit(main())
"""
        write_result = agent.write_code("src/main.py", main_code)
        assert write_result['success'] == True
        
        # Create a test file
        test_code = """import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import main

def test_main():
    \"\"\"Test the main function.\"\"\"
    result = main()
    assert result == 0

if __name__ == '__main__':
    test_main()
    print('Tests passed!')
"""
        test_result = agent.write_code("tests/test_main.py", test_code)
        assert test_result['success'] == True
        
        # Update README
        readme_content = """# Hello World Project

A simple Hello World project created by the Developer Agent.

## Features
- Clean project structure
- Automated testing
- Git version control

## Usage
```bash
python src/main.py
```

## Testing
```bash
python tests/test_main.py
```

## Created By
Developer Agent - Autonomous AI Software Engineer
"""
        readme_result = agent.write_code("README.md", readme_content)
        assert readme_result['success'] == True
        
        # Commit everything
        commit_result = agent.git_commit(
            "Initial project setup with Hello World implementation",
            ["src/main.py", "tests/test_main.py", "README.md", ".gitignore"]
        )
        assert commit_result['success'] == True
        
        # Verify all components exist
        assert os.path.exists("src/main.py")
        assert os.path.exists("tests/test_main.py")
        assert os.path.exists("README.md")
        assert os.path.exists(".git")
        assert os.path.exists(".gitignore")
        
        # Test that the main program runs
        result = subprocess.run(
            ['python', 'src/main.py'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Hello, World!" in result.stdout
    
    def test_multi_file_project(self, agent, temp_workspace):
        """Test creating a project with multiple interconnected files."""
        # Initialize git first
        agent.git_init()
        
        # Create a calculator module
        calc_code = """\"\"\"Calculator module.\"\"\"

def add(a, b):
    \"\"\"Add two numbers.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtract b from a.\"\"\"
    return a - b

def multiply(a, b):
    \"\"\"Multiply two numbers.\"\"\"
    return a * b

def divide(a, b):
    \"\"\"Divide a by b.\"\"\"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
"""
        agent.write_code("calculator.py", calc_code)
        
        # Create a main program using the calculator
        main_code = """\"\"\"Main program using calculator module.\"\"\"

from calculator import add, subtract, multiply, divide

def main():
    \"\"\"Demonstrate calculator functions.\"\"\"
    print("Calculator Demo")
    print("-" * 20)
    
    a, b = 10, 5
    
    print(f"{a} + {b} = {add(a, b)}")
    print(f"{a} - {b} = {subtract(a, b)}")
    print(f"{a} * {b} = {multiply(a, b)}")
    print(f"{a} / {b} = {divide(a, b)}")
    
    return 0

if __name__ == '__main__':
    exit(main())
"""
        agent.write_code("main.py", main_code)
        
        # Create tests
        test_code = """\"\"\"Tests for calculator module.\"\"\"

import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    
    with pytest.raises(ValueError):
        divide(5, 0)
"""
        agent.write_code("test_calculator.py", test_code)
        
        # Commit all files
        result = agent.git_commit(
            "Add calculator module with tests",
            ["calculator.py", "main.py", "test_calculator.py"]
        )
        assert result['success'] == True
        
        # Verify the program works
        result = subprocess.run(
            ['python', 'main.py'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Calculator Demo" in result.stdout
        assert "10 + 5 = 15" in result.stdout
    
    def test_error_recovery(self, agent, temp_workspace):
        """Test agent's ability to recover from errors."""
        # Try to write invalid Python
        bad_code = "def broken(\n    print('unclosed"
        result = agent.write_code("broken.py", bad_code)
        assert result['success'] == False
        
        # Now write valid code to same file
        good_code = "def working():\n    print('fixed')"
        result = agent.write_code("broken.py", good_code)
        assert result['success'] == True
        
        # Verify the file contains the good code
        with open("broken.py", 'r') as f:
            content = f.read()
        assert content == good_code
    
    def test_memory_persistence(self, agent, temp_workspace):
        """Test agent's memory system."""
        # Ensure memory directory exists
        agent.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Save some information
        agent.save_memory("project_name", "test_project")
        agent.save_memory("version", "1.0.0")
        agent.save_memory("tasks_completed", ["init", "setup", "test"])
        
        # Load it back
        project = agent.load_memory("project_name")
        assert project == "test_project"
        
        version = agent.load_memory("version")
        assert version == "1.0.0"
        
        tasks = agent.load_memory("tasks_completed")
        assert len(tasks) == 3
        assert "init" in tasks
        
        # Load all memory
        all_memory = agent.load_memory()
        assert "project_name" in all_memory
        assert "version" in all_memory
        assert "last_updated" in all_memory
    
    def test_session_logging(self, agent, temp_workspace):
        """Test that agent logs all actions."""
        # Perform various actions
        agent.write_code("test1.py", "print('1')")
        agent.read_file("test1.py")
        agent.write_code("test2.py", "print('2')")
        agent.git_init()
        agent.git_add(["test1.py", "test2.py"])
        
        # Get session summary
        summary = agent.get_session_summary()
        
        assert summary['total_actions'] >= 5
        assert summary['files_written'] == 2
        assert summary['files_read'] == 1
        assert summary['git_operations'] >= 2
        
        # Verify log file exists
        log_file = Path("memory/dev/agent_log.jsonl")
        assert log_file.exists()
        
        # Read and verify log entries
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        assert len(lines) >= 5
        
        # Each line should be valid JSON
        import json
        for line in lines:
            entry = json.loads(line)
            assert 'timestamp' in entry
            assert 'action' in entry
            assert 'details' in entry


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])