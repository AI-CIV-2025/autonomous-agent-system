"""
Developer Agent - Phase 1 Implementation
Autonomous developer agent for code writing and project management
"""

import os
import sys
import yaml
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import ast
import traceback


class DeveloperAgent:
    """
    Autonomous Developer Agent for software engineering tasks.
    Handles file operations, code writing, and git management.
    """
    
    def __init__(self, config_path: str = "src/configs/developer_agent.yaml"):
        """Initialize the Developer Agent with configuration."""
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.memory_path = Path(self.config['memory']['location'])
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.session_log = []
        self.backup_dir = Path("memory/dev/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def load_config(self) -> Dict:
        """Load agent configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def log_action(self, action: str, details: Dict[str, Any]) -> None:
        """Log agent actions for debugging and memory."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'details': details
        }
        self.session_log.append(log_entry)
        
        # Also write to persistent log
        log_file = self.memory_path / "agent_log.jsonl"
        # Ensure the directory exists before writing
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def verify_syntax_python(self, code: str) -> Tuple[bool, Optional[str]]:
        """Verify Python syntax before writing."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def verify_file_allowed(self, filepath: Path) -> Tuple[bool, str]:
        """Check if file type is allowed based on configuration."""
        extension = filepath.suffix
        allowed_extensions = self.config['constraints']['allowed_extensions']
        
        if extension not in allowed_extensions:
            return False, f"File extension {extension} not allowed"
        
        return True, "File type allowed"
    
    def create_backup(self, filepath: Path) -> Optional[Path]:
        """Create a backup of a file before modifying it."""
        if not filepath.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
        backup_path = self.backup_dir / backup_name
        
        try:
            shutil.copy2(filepath, backup_path)
            self.log_action("backup_created", {
                'original': str(filepath),
                'backup': str(backup_path)
            })
            return backup_path
        except Exception as e:
            self.log_action("backup_failed", {
                'file': str(filepath),
                'error': str(e)
            })
            return None
    
    def write_code(self, filepath: str, content: str) -> Dict[str, Any]:
        """Write code to a file with verification."""
        filepath = Path(filepath)
        
        # Verify file type is allowed
        allowed, message = self.verify_file_allowed(filepath)
        if not allowed:
            error_msg = f"Cannot write to {filepath}: {message}"
            self.log_action("write_rejected", {'file': str(filepath), 'reason': message})
            return {'success': False, 'error': error_msg}
        
        # Verify syntax for Python files
        if filepath.suffix == '.py':
            valid, error = self.verify_syntax_python(content)
            if not valid:
                error_msg = f"Syntax error in Python code: {error}"
                self.log_action("syntax_error", {'file': str(filepath), 'error': error})
                return {'success': False, 'error': error_msg}
        
        # Check file size constraint
        if len(content.encode('utf-8')) > self.config['constraints']['max_file_size']:
            error_msg = f"File size exceeds maximum allowed ({self.config['constraints']['max_file_size']} bytes)"
            self.log_action("size_exceeded", {'file': str(filepath), 'size': len(content)})
            return {'success': False, 'error': error_msg}
        
        # Create parent directories if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Create backup if file exists
        if filepath.exists() and self.config['behavior']['create_backups']:
            self.create_backup(filepath)
        
        # Write the file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_action("file_written", {
                'file': str(filepath),
                'size': len(content),
                'lines': len(content.splitlines())
            })
            
            return {
                'success': True,
                'file': str(filepath),
                'size': len(content),
                'message': f"Successfully wrote {filepath}"
            }
        
        except Exception as e:
            error_msg = f"Failed to write file: {str(e)}"
            self.log_action("write_failed", {'file': str(filepath), 'error': str(e)})
            return {'success': False, 'error': error_msg}
    
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """Read a file's content."""
        filepath = Path(filepath)
        
        if not filepath.exists():
            return {
                'success': False,
                'error': f"File not found: {filepath}"
            }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.log_action("file_read", {
                'file': str(filepath),
                'size': len(content)
            })
            
            return {
                'success': True,
                'content': content,
                'file': str(filepath)
            }
        
        except Exception as e:
            self.log_action("read_failed", {'file': str(filepath), 'error': str(e)})
            return {
                'success': False,
                'error': f"Failed to read file: {str(e)}"
            }
    
    def edit_file(self, filepath: str, old_content: str, new_content: str) -> Dict[str, Any]:
        """Edit a file by replacing old content with new content."""
        filepath = Path(filepath)
        
        # Always read before edit per configuration
        if self.config['behavior']['always_read_before_edit']:
            read_result = self.read_file(str(filepath))
            if not read_result['success']:
                return read_result
            
            current_content = read_result['content']
            if old_content not in current_content:
                return {
                    'success': False,
                    'error': "Old content not found in file"
                }
            
            # Replace the content
            modified_content = current_content.replace(old_content, new_content, 1)
            
            # Write the modified content
            return self.write_code(str(filepath), modified_content)
        
        return {
            'success': False,
            'error': "Read before edit is required by configuration"
        }
    
    def git_init(self) -> Dict[str, Any]:
        """Initialize a git repository."""
        try:
            result = subprocess.run(
                ['git', 'init'],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.log_action("git_init", {'output': result.stdout})
            
            return {
                'success': True,
                'message': "Git repository initialized",
                'output': result.stdout
            }
        
        except subprocess.CalledProcessError as e:
            self.log_action("git_init_failed", {'error': e.stderr})
            return {
                'success': False,
                'error': f"Git init failed: {e.stderr}"
            }
    
    def git_add(self, files: List[str]) -> Dict[str, Any]:
        """Add files to git staging area."""
        try:
            for file in files:
                result = subprocess.run(
                    ['git', 'add', file],
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            self.log_action("git_add", {'files': files})
            
            return {
                'success': True,
                'message': f"Added {len(files)} files to git",
                'files': files
            }
        
        except subprocess.CalledProcessError as e:
            self.log_action("git_add_failed", {'error': e.stderr})
            return {
                'success': False,
                'error': f"Git add failed: {e.stderr}"
            }
    
    def git_commit(self, message: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Commit changes to git repository."""
        try:
            # Add files if specified
            if files:
                add_result = self.git_add(files)
                if not add_result['success']:
                    return add_result
            
            # Create commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.log_action("git_commit", {
                'message': message,
                'output': result.stdout
            })
            
            return {
                'success': True,
                'message': f"Committed with message: {message}",
                'output': result.stdout
            }
        
        except subprocess.CalledProcessError as e:
            # Check if it's just "nothing to commit"
            if "nothing to commit" in e.stdout:
                return {
                    'success': True,
                    'message': "Nothing to commit, working tree clean",
                    'output': e.stdout
                }
            
            self.log_action("git_commit_failed", {'error': e.stderr})
            return {
                'success': False,
                'error': f"Git commit failed: {e.stderr}"
            }
    
    def git_status(self) -> Dict[str, Any]:
        """Get git repository status."""
        try:
            result = subprocess.run(
                ['git', 'status'],
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                'success': True,
                'output': result.stdout
            }
        
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f"Git status failed: {e.stderr}"
            }
    
    def create_project(self, project_name: str) -> Dict[str, Any]:
        """Create a new project with basic structure."""
        project_path = Path(project_name)
        
        try:
            # Create project directory
            project_path.mkdir(exist_ok=True)
            
            # Create basic structure
            (project_path / "src").mkdir(exist_ok=True)
            (project_path / "tests").mkdir(exist_ok=True)
            (project_path / "docs").mkdir(exist_ok=True)
            
            # Create README
            readme_content = f"# {project_name}\n\nProject created by Developer Agent\n"
            self.write_code(str(project_path / "README.md"), readme_content)
            
            # Create .gitignore
            gitignore_content = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
"""
            self.write_code(str(project_path / ".gitignore"), gitignore_content)
            
            self.log_action("project_created", {'name': project_name})
            
            return {
                'success': True,
                'message': f"Project {project_name} created successfully",
                'path': str(project_path)
            }
        
        except Exception as e:
            self.log_action("project_creation_failed", {
                'name': project_name,
                'error': str(e)
            })
            return {
                'success': False,
                'error': f"Failed to create project: {str(e)}"
            }
    
    def save_memory(self, key: str, value: Any) -> None:
        """Save information to agent memory."""
        memory_file = self.memory_path / "memory.json"
        
        # Load existing memory
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                memory = json.load(f)
        else:
            memory = {}
        
        # Update memory
        memory[key] = value
        memory['last_updated'] = datetime.now().isoformat()
        
        # Save memory
        with open(memory_file, 'w') as f:
            json.dump(memory, f, indent=2)
        
        self.log_action("memory_saved", {'key': key})
    
    def load_memory(self, key: Optional[str] = None) -> Any:
        """Load information from agent memory."""
        memory_file = self.memory_path / "memory.json"
        
        if not memory_file.exists():
            return {} if key is None else None
        
        with open(memory_file, 'r') as f:
            memory = json.load(f)
        
        if key is None:
            return memory
        
        return memory.get(key)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            'total_actions': len(self.session_log),
            'files_written': len([a for a in self.session_log if a['action'] == 'file_written']),
            'files_read': len([a for a in self.session_log if a['action'] == 'file_read']),
            'git_operations': len([a for a in self.session_log if a['action'].startswith('git_')]),
            'errors': len([a for a in self.session_log if 'failed' in a['action']]),
            'session_log': self.session_log[-10:]  # Last 10 actions
        }


def main():
    """Main entry point for testing the Developer Agent."""
    print("Developer Agent - Phase 1 Implementation")
    print("-" * 40)
    
    # Initialize agent
    agent = DeveloperAgent()
    print(f"✓ Agent initialized with config from {agent.config_path}")
    
    # Display configuration
    print(f"✓ Agent name: {agent.config['agent']['name']}")
    print(f"✓ Role: {agent.config['agent']['role']}")
    print(f"✓ Memory location: {agent.memory_path}")
    
    # Test basic functionality
    print("\nRunning self-test...")
    
    # Test 1: Write a simple Python file
    test_code = """def hello_world():
    print("Hello from Developer Agent!")
    return True
"""
    result = agent.write_code("test_hello.py", test_code)
    if result['success']:
        print("✓ Test 1: File writing successful")
    else:
        print(f"✗ Test 1 failed: {result['error']}")
    
    # Test 2: Read the file back
    result = agent.read_file("test_hello.py")
    if result['success']:
        print("✓ Test 2: File reading successful")
    else:
        print(f"✗ Test 2 failed: {result['error']}")
    
    # Test 3: Git status check
    result = agent.git_status()
    if result['success']:
        print("✓ Test 3: Git status check successful")
    else:
        print(f"✗ Test 3 failed: {result['error']}")
    
    # Display session summary
    summary = agent.get_session_summary()
    print(f"\nSession Summary:")
    print(f"  Total actions: {summary['total_actions']}")
    print(f"  Files written: {summary['files_written']}")
    print(f"  Files read: {summary['files_read']}")
    print(f"  Errors: {summary['errors']}")
    
    # Clean up test file
    try:
        os.remove("test_hello.py")
    except:
        pass
    
    print("\n✓ Developer Agent is ready!")


if __name__ == "__main__":
    main()