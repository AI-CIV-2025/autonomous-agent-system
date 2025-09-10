# Autonomous Multi-Agent System 🤖

[![GitHub](https://img.shields.io/github/license/AI-CIV-2025/autonomous-agent-system)](https://github.com/AI-CIV-2025/autonomous-agent-system)
[![Phase](https://img.shields.io/badge/Phase-1%20Complete-success)](https://github.com/AI-CIV-2025/autonomous-agent-system)
[![Tests](https://img.shields.io/badge/Tests-91%25%20Passing-green)](https://github.com/AI-CIV-2025/autonomous-agent-system)

An evolving multi-agent AI system that progresses from a single developer agent to a complex, self-improving organization of specialized agents.

## 🎯 Project Vision

This project implements a 10-phase evolution of an autonomous AI agent system:
- **Phase 1-3**: Foundation with Developer, Planner, and Reviewer agents
- **Phase 4-6**: Enhanced with Memory, Reasoning, and Research capabilities  
- **Phase 7-8**: Specialized teams for Crypto Analysis and Marketing
- **Phase 9-10**: Unified orchestration and self-improvement

## 🚀 Current Status

✅ **Phase 1 Complete**: Developer Agent Foundation
- Autonomous code writing and editing
- Git repository management
- File operations with safety checks
- Python syntax verification
- Memory persistence system

## 📁 Project Structure

```
ClaudeCode_Agents/
├── src/
│   ├── agents/          # Agent implementations
│   │   └── developer.py # Phase 1 Developer Agent
│   ├── configs/         # Agent configurations
│   │   └── developer_agent.yaml
│   ├── prompts/         # Agent prompt templates
│   │   └── developer_prompt.md
│   └── tools/           # MCP tools and utilities
├── memory/              # Persistent memory storage
│   ├── dev/            # Development team memory
│   ├── research/       # Research team memory
│   ├── marketing/      # Marketing team memory
│   └── global/         # Global project memory
├── tests/              # Test scenarios
│   ├── test_phase_01_file_ops.py
│   ├── test_phase_01_git.py
│   └── test_phase_01_e2e.py
├── phases/             # Phase implementation guides
│   ├── phase_01_developer.md
│   ├── phase_02_planner.md
│   └── ... (8 more phases)
├── docs/
│   └── dev_journals/   # Development journals
└── CLAUDE.md          # Instructions for Claude Code

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AI-CIV-2025/autonomous-agent-system.git
cd autonomous-agent-system
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Using the Developer Agent

```python
from src.agents.developer import DeveloperAgent

# Initialize the agent
agent = DeveloperAgent()

# Write code
agent.write_code("hello.py", "print('Hello, World!')")

# Read files
result = agent.read_file("hello.py")
print(result['content'])

# Git operations
agent.git_init()
agent.git_commit("Initial commit", ["hello.py"])

# Create a project
agent.create_project("my_project")
```

### Running Tests

```bash
# Run all Phase 1 tests
pytest tests/test_phase_01_*.py -v

# Run specific test suite
pytest tests/test_phase_01_file_ops.py -v
```

### Quick Test
```bash
# Test the Developer Agent
python src/agents/developer.py
```

## 📊 Agent Capabilities

### Developer Agent (Phase 1)
- ✅ File creation and editing
- ✅ Python syntax verification
- ✅ Git repository management
- ✅ Project scaffolding
- ✅ Memory persistence
- ✅ Error handling and recovery
- ✅ Backup creation

## 🗺️ Roadmap

### Phase 2: Planning & Task Decomposition
- [ ] Implement Planner Agent
- [ ] Task breakdown capabilities
- [ ] Inter-agent communication

### Phase 3: Code Review & QA
- [ ] Implement Reviewer Agent
- [ ] Automated code review
- [ ] Quality assurance checks

### Phase 4: Persistent Memory
- [ ] Basic Memory MCP integration
- [ ] Cross-session context retention
- [ ] Knowledge base building

### Phase 5: Enhanced Reasoning
- [ ] Sequential Thinking MCP
- [ ] Complex problem solving
- [ ] Decision tree navigation

### Phase 6: Research Capabilities
- [ ] Researcher Agent
- [ ] Web content retrieval
- [ ] Documentation analysis

### Phase 7: Crypto Analyst Swarm
- [ ] Market Analyst
- [ ] News Analyst
- [ ] Technical Analyst
- [ ] Swarm Coordinator

### Phase 8: Marketing Team
- [ ] Content Strategist
- [ ] Content Writer
- [ ] Editor
- [ ] Social Media Manager

### Phase 9: Unified Orchestration
- [ ] Chief Meta-Agent
- [ ] Team coordination
- [ ] Resource allocation

### Phase 10: Self-Improvement
- [ ] Self-Evaluator (Critic)
- [ ] Improver Agent
- [ ] Recursive enhancement

## 📝 Development Guidelines

### For Claude Code
1. Always read `CLAUDE.md` first
2. Check dev journals in `docs/dev_journals/`
3. Follow phase documentation in `phases/`
4. Write comprehensive dev journal entries after each phase

### For Contributors
1. Follow existing code patterns
2. Add tests for new features
3. Update documentation
4. Maintain backward compatibility

## 🧪 Testing

The project includes comprehensive test suites:
- **File Operations**: Tests for file creation, reading, editing
- **Git Operations**: Tests for repository management
- **End-to-End**: Complete workflow validation
- **Error Handling**: Resilience and recovery tests

## 📚 Documentation

- `CLAUDE.md`: Primary instructions for Claude Code
- `phases/*.md`: Detailed implementation guides for each phase
- `docs/dev_journals/`: Development history and context
- Agent prompts in `src/prompts/`
- Configuration files in `src/configs/`

## 🤝 Contributing

This project is designed to be built primarily by Claude Code, but contributions are welcome:
1. Read the phase documentation
2. Follow the existing patterns
3. Add comprehensive tests
4. Document your changes

## 📄 License

[License information to be added]

## 🙏 Acknowledgments

Built with Claude Code - Anthropic's AI coding assistant

---

*This is an evolving project. Each phase builds upon the previous, creating an increasingly sophisticated multi-agent system capable of self-improvement.*