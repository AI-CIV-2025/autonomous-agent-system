# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 YOUR MISSION: BUILD THE AUTONOMOUS MULTI-AGENT SYSTEM

You are the PRIMARY BUILDER of this autonomous multi-agent system. Your objective is to implement each phase methodically, test thoroughly, and create a self-evolving AI organization that can recursively improve itself.

### 📔 FIRST STEP - READ YOUR DEV JOURNALS!
**Before doing ANYTHING else:**
1. Navigate to `/docs/dev_journals/`
2. Read the most recent 2 entries (or ALL if this is your first session)
3. These journals are YOUR MEMORY from previous sessions
4. They contain critical context, configurations, and progress notes

## Project Overview

This repository contains the implementation of an autonomous multi-agent system that evolves from a single developer automation tool into a complex organization of specialized agents. You will build this system phase by phase, using Claude Code with MCP (Model Context Protocol) support.

## 📁 Project Structure

```
/ClaudeCode_Agents/
├── CLAUDE.md                      # This file - your mission guide
├── phases/                        # Phase implementation docs
│   ├── phase_01_developer.md     # Phase 1: Developer Foundation
│   ├── phase_02_planner.md       # Phase 2: Planning & Decomposition
│   ├── phase_03_reviewer.md      # Phase 3: Code Review & QA
│   ├── phase_04_memory.md        # Phase 4: Persistent Memory
│   ├── phase_05_reasoning.md     # Phase 5: Sequential Thinking
│   ├── phase_06_research.md      # Phase 6: Research Assistant
│   ├── phase_07_crypto.md        # Phase 7: Crypto Analyst Swarm
│   ├── phase_08_marketing.md     # Phase 8: Marketing Team
│   ├── phase_09_orchestration.md # Phase 9: Unified Orchestration
│   └── phase_10_evolution.md     # Phase 10: Self-Improvement
├── src/                          # Source code
│   ├── agents/                   # Agent implementations
│   ├── configs/                  # Agent configurations
│   ├── prompts/                  # Agent prompts
│   └── tools/                    # MCP tools and utilities
├── memory/                       # Persistent memory storage
│   ├── dev/                      # Development team memory
│   ├── research/                 # Research team memory
│   ├── marketing/                # Marketing team memory
│   └── global/                   # Global project memory
├── tests/                        # Test scenarios
└── docs/                         # Documentation
    └── dev_journals/             # Development journals (YOUR MEMORY!)
```

## 🚀 Build Process

### 📔 CRITICAL: Development Journal Protocol

**BEFORE STARTING ANY WORK:**
1. **ALWAYS read the most recent 2 dev journal entries** in `/docs/dev_journals/`
2. **If this is your first session, READ ALL dev journals** to understand progress
3. **Dev journals are your memory between sessions** - they contain critical context

**Location**: `/docs/dev_journals/[date]_[phase]_[description].md`

### Phase Execution Protocol

For EACH phase, you MUST:

1. **Read the phase document** in `/phases/phase_XX_*.md`
2. **Check dev journals** for any previous work on this phase
3. **Execute all pre-build tasks** (research, setup, planning)
4. **Implement the code** following the task list
5. **Run comprehensive tests** to verify functionality
6. **Update memory** with lessons learned
7. **WRITE DEV JOURNAL ENTRY** before ending session
8. **Mark phase complete** and proceed to next

### ⚠️ END OF PHASE REQUIREMENT
**EVERY PHASE MUST END WITH A DEV JOURNAL ENTRY**
- This is NOT optional
- Include what worked, what didn't, and specific configurations
- This is your handoff to your future self
- Assume context will be cleared after writing

### Critical Success Factors

- ✅ Each agent must have clear, tested functionality
- ✅ Inter-agent communication must be verified
- ✅ Memory persistence must be validated
- ✅ Error handling must be robust
- ✅ Each phase builds on previous phases
- ✅ System must be able to self-modify by Phase 10

## 🛠️ Development Commands

### Initialize Project
```bash
git init
mkdir -p src/agents src/configs src/prompts src/tools
mkdir -p memory/dev memory/research memory/marketing memory/global
mkdir -p tests docs/dev_journal
```

### Test Agent Communication
```bash
# Test patterns will be defined in each phase document
python tests/test_phase_XX.py
```

### Memory Operations
```bash
# Check memory state
ls -la memory/
# View agent logs
cat memory/global/agent_interactions.log
```

## Architecture Overview

The system follows a phased approach with 10 distinct phases:

1. **Phase 1**: Developer Automation Foundation - Single Developer Agent
2. **Phase 2**: Planning & Task Decomposition - Planner (Meta-Agent) + Developer
3. **Phase 3**: Code Review & Quality Assurance - Add Reviewer Agent
4. **Phase 4**: Persistent Memory Integration - Basic Memory MCP
5. **Phase 5**: Enhanced Reasoning - Sequential Thinking MCP
6. **Phase 6**: Research Assistant Capabilities - Add Researcher Agent
7. **Phase 7**: Crypto Research Analyst Swarm - Specialized crypto analysis team
8. **Phase 8**: Social Media Marketing Team - Content creation pipeline
9. **Phase 9**: Unified Multi-Team Orchestration - Chief Meta-Agent coordination
10. **Phase 10**: Continuous Self-Improvement - Self-evaluation and scaling

## Key Agent Roles

### Core Management
- **Chief Meta-Agent**: Top-level coordinator managing all teams
- **Team Leads**: Dev Lead, Research Lead, Marketing Lead

### Development Team
- **Developer Agent**: Writes and modifies code
- **Reviewer Agent**: Reviews code for quality and errors

### Research Team
- **Researcher Agent**: Gathers information from web/documentation
- **Crypto Swarm** (Phase 7):
  - Market Analyst: Quantitative data analysis
  - News Analyst: Sentiment and news monitoring
  - Technical Analyst: Chart and pattern analysis
  - Crypto Research Coordinator: Synthesizes findings

### Marketing Team
- **Content Strategist**: Plans content strategy
- **Content Writer**: Creates actual content
- **Editor**: Reviews and refines content
- **Social Media Manager**: Schedules and posts

### Self-Improvement
- **Self-Evaluator (Critic)**: Analyzes system performance
- **Improver Agent**: Implements system improvements

## Required MCP Servers

- **Filesystem MCP**: File reading/writing operations
- **Git MCP**: Version control operations
- **Basic Memory MCP**: Persistent knowledge storage
- **Sequential Thinking MCP**: Advanced reasoning capabilities
- **Fetch MCP**: Web content retrieval

## Common Development Tasks

### Setting Up the Project
1. Initialize git repository
2. Configure MCP servers in Claude settings
3. Set up memory directory structure
4. Create initial agent configuration

### Adding New Agents
1. Update configuration YAML/JSON with new agent definition
2. Define agent role, connections, and allowed tools
3. Create specific prompt engineering for the agent
4. Test agent integration with existing team

### Memory Management
- Store team-specific data in designated folders: `/memory/dev`, `/memory/research`, `/memory/marketing`
- Maintain global project information in `/memory/global`
- Use memory for cross-team communication and knowledge persistence

## Coordination Models

- **Phase 1-2**: Single agent → Hierarchical (Planner-Developer)
- **Phase 3-6**: Centralized with sequential workflow
- **Phase 7**: Hybrid swarm with internal coordinator
- **Phase 8**: Linear pipeline (Strategist → Writer → Editor)
- **Phase 9-10**: Multi-level hierarchical with Chief at top

## Fault Tolerance Patterns

- **Feedback Loops**: Agents report failures back for re-planning
- **Redundancy**: Multiple agents can catch issues others miss
- **Memory Checkpointing**: Save state for recovery
- **Testing Integration**: Validate changes before committing
- **Safe Mode**: Test configuration changes before applying

## Implementation Guidance

When implementing phases:
1. Start with Phase 1 and build incrementally
2. Test each phase thoroughly before moving to the next
3. Use memory to maintain continuity between phases
4. Document all agent interactions and decisions
5. Implement proper error handling at each level

## Key Design Principles

- **Single Responsibility**: Each agent focuses on specific tasks
- **Modularity**: Agents can be added/removed with minimal impact
- **Scalability**: System can grow by adding new teams/agents
- **Self-Improvement**: System can analyze and improve itself
- **Fault Tolerance**: Multiple layers of error detection and recovery