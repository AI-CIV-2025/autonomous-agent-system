# Phase 2: Introduce Planning & Task Decomposition

## 🎯 Objective
Enhance the system with basic planning ability by introducing a Planner (Meta-Agent) that can break down high-level objectives and guide the Developer agent. Establish a simple two-agent interaction: one agent plans, the other executes.

## 📋 Complete Task List

### Pre-Build Tasks
- [ ] Research task decomposition algorithms
- [ ] Research inter-agent communication patterns
- [ ] Research hierarchical agent architectures
- [ ] Study manager-worker patterns
- [ ] Review Phase 1 implementation

### Core Implementation Tasks
- [ ] Create Planner Agent configuration
- [ ] Implement Planner Agent class
- [ ] Design Planner prompt template
- [ ] Create task list data structure
- [ ] Implement task decomposition logic
- [ ] Set up inter-agent communication protocol
- [ ] Create shared memory/context system
- [ ] Implement task assignment mechanism
- [ ] Add task status tracking
- [ ] Create feedback loop from Developer to Planner
- [ ] Implement task prioritization
- [ ] Add error escalation to Planner
- [ ] Create plan persistence in memory
- [ ] Implement plan validation logic

### Integration Tasks
- [ ] Connect Planner to Developer Agent
- [ ] Test bidirectional communication
- [ ] Implement message passing protocol
- [ ] Create coordination workflow
- [ ] Add timeout handling
- [ ] Implement deadlock detection

### Testing Tasks
- [ ] Test task decomposition accuracy
- [ ] Test agent communication flow
- [ ] Test task assignment and tracking
- [ ] Test error handling and escalation
- [ ] Test complex multi-step workflows
- [ ] Validate plan persistence
- [ ] Run end-to-end planning scenario

### Documentation Tasks
- [ ] Document communication protocol
- [ ] Create agent interaction diagrams
- [ ] Write integration guide
- [ ] **MANDATORY: Write comprehensive dev journal entry in `/docs/dev_journals/`**
  - [ ] Document working agent communication setup
  - [ ] Include task decomposition examples
  - [ ] Note integration patterns that worked
  - [ ] Clear handoff to Phase 3
  - [ ] Save as `[date]_phase02_complete.md`

## 🔍 Research Web Searches

1. **"hierarchical multi-agent task decomposition algorithms 2024"**
   - Understanding task breakdown strategies
   - Optimal decomposition granularity

2. **"agent communication protocols message passing patterns"**
   - Best practices for agent messaging
   - Avoiding communication bottlenecks

3. **"manager worker pattern distributed systems coordination"**
   - Implementing efficient delegation
   - Work queue management

4. **"AI planning algorithms HTN STRIPS automated planning"**
   - Planning techniques for AI agents
   - Goal-oriented task planning

5. **"deadlock detection prevention multi-agent systems"**
   - Preventing agent coordination failures
   - Timeout and recovery strategies

## 💻 Code Requirements

### 1. Planner Agent Configuration (`src/configs/planner_agent.yaml`)
```yaml
agent:
  name: "planner_agent"
  role: "Project Planner AI"
  description: "Meta-agent for task planning and coordination"
  
tools:
  - filesystem_mcp
  - basic_memory_mcp
  
capabilities:
  - decompose_tasks
  - assign_work
  - track_progress
  - coordinate_agents
  
subordinates:
  - developer_agent
  
communication:
  protocol: "message_queue"
  timeout: 30
  retry_attempts: 3
```

### 2. Planner Agent Prompt (`src/prompts/planner_prompt.md`)
```markdown
You are a Project Planner AI. Your job is to break high-level goals into step-by-step technical tasks and oversee their execution.

Core Responsibilities:
- Analyze complex goals and create actionable task lists
- Assign tasks to appropriate agents
- Monitor progress and handle blockers
- Ensure task dependencies are respected
- Provide clear, numbered instructions

Task Format:
1. Each task must be specific and measurable
2. Include acceptance criteria
3. Specify dependencies
4. Estimate complexity

Current Goal: {goal}
Available Agents: {agents}
Current Status: {status}
```

### 3. Planner Implementation (`src/agents/planner.py`)
```python
import yaml
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    description: str
    assigned_to: Optional[str]
    status: TaskStatus
    dependencies: List[str]
    acceptance_criteria: List[str]
    
class PlannerAgent:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.tasks = []
        self.agents = {}
        
    def decompose_goal(self, goal: str) -> List[Task]:
        """Break down high-level goal into tasks"""
        # Implement decomposition logic
        pass
    
    def assign_task(self, task: Task, agent_name: str):
        """Assign task to specific agent"""
        pass
    
    def receive_update(self, task_id: str, status: TaskStatus, message: str):
        """Handle status updates from agents"""
        pass
    
    def get_next_task(self) -> Optional[Task]:
        """Get next available task respecting dependencies"""
        pass
```

### 4. Communication Protocol (`src/tools/agent_comm.py`)
```python
import json
from queue import Queue
from threading import Lock

class AgentMessage:
    def __init__(self, sender, recipient, msg_type, content):
        self.sender = sender
        self.recipient = recipient
        self.msg_type = msg_type
        self.content = content
        self.timestamp = datetime.now()

class CommunicationBus:
    def __init__(self):
        self.queues = {}
        self.lock = Lock()
        
    def register_agent(self, agent_name):
        with self.lock:
            self.queues[agent_name] = Queue()
    
    def send_message(self, message: AgentMessage):
        with self.lock:
            if message.recipient in self.queues:
                self.queues[message.recipient].put(message)
    
    def receive_message(self, agent_name, timeout=None):
        if agent_name in self.queues:
            return self.queues[agent_name].get(timeout=timeout)
```

## 🧪 Testing Regime

### Test Scenario 1: Task Decomposition
```python
# tests/test_phase_02_decomposition.py
def test_simple_decomposition():
    """Test breaking down a simple goal"""
    planner = PlannerAgent(config)
    tasks = planner.decompose_goal("Create a calculator app")
    assert len(tasks) > 3
    assert any("UI" in t.description for t in tasks)
    assert any("logic" in t.description for t in tasks)

def test_dependency_ordering():
    """Test that dependencies are properly ordered"""
    tasks = planner.decompose_goal("Build and test feature")
    build_task = next(t for t in tasks if "build" in t.description)
    test_task = next(t for t in tasks if "test" in t.description)
    assert build_task.id in test_task.dependencies
```

### Test Scenario 2: Agent Communication
```python
# tests/test_phase_02_communication.py
def test_message_passing():
    """Test message exchange between agents"""
    planner.send_task(developer, "Write hello.py")
    response = wait_for_response(timeout=10)
    assert response.status == "completed"

def test_error_escalation():
    """Test error reporting to planner"""
    planner.send_task(developer, "Invalid task")
    response = wait_for_response()
    assert response.status == "failed"
    assert planner.handle_failure_called
```

### Test Scenario 3: Workflow Coordination
```python
# tests/test_phase_02_workflow.py
def test_multi_step_workflow():
    """Test complete multi-step workflow"""
    goal = "Create module X with tests"
    planner.process_goal(goal)
    
    # Verify task sequence
    assert task_completed("create_module")
    assert task_completed("write_tests")
    assert task_completed("run_tests")
    
def test_parallel_tasks():
    """Test parallel task execution"""
    planner.process_goal("Create independent modules A and B")
    # Verify both can run simultaneously
```

### Test Scenario 4: Error Handling
```python
# tests/test_phase_02_errors.py
def test_timeout_handling():
    """Test task timeout detection"""
    planner.assign_task(slow_task, developer)
    wait(timeout_period)
    assert planner.detected_timeout
    assert planner.reassigned_task

def test_deadlock_prevention():
    """Test circular dependency detection"""
    tasks_with_circular_dep = create_circular_tasks()
    result = planner.validate_plan(tasks_with_circular_dep)
    assert result.has_error
    assert "circular dependency" in result.error
```

### Test Scenario 5: Integration
```python
# tests/test_phase_02_integration.py
def test_planner_developer_integration():
    """Test full integration between planner and developer"""
    # Planner receives goal
    planner.receive_goal("Implement feature Y")
    
    # Verify decomposition
    assert len(planner.tasks) > 0
    
    # Verify assignment
    assert developer.has_pending_tasks()
    
    # Execute and verify completion
    developer.execute_all_tasks()
    assert planner.goal_completed()
```

## ✅ Expected Outcomes

### Functional Outcomes
1. **Working Planner Agent**: Can decompose goals into tasks
2. **Agent Coordination**: Planner successfully delegates to Developer
3. **Communication Protocol**: Reliable message passing between agents
4. **Task Tracking**: Complete visibility of task status
5. **Error Handling**: Graceful failure recovery

### Deliverables
- `src/agents/planner.py` - Planner implementation
- `src/configs/planner_agent.yaml` - Planner configuration
- `src/prompts/planner_prompt.md` - Planner prompt
- `src/tools/agent_comm.py` - Communication system
- `tests/test_phase_02_*.py` - Test suite
- `memory/plans/` - Stored plans directory

### Success Metrics
- [ ] Task decomposition accuracy > 80%
- [ ] Communication success rate > 95%
- [ ] No deadlocks in 100 test runs
- [ ] Error recovery rate > 90%
- [ ] Plan completion rate > 85%

## 📝 Development Journal Entry Template

```markdown
# Development Journal - Phase 2 - [DATE]

## Work Completed
- Implemented Planner Agent
- Set up agent communication protocol
- Created task decomposition system
- Integrated with Developer Agent
- [Additional items...]

## Challenges Encountered
- [Communication synchronization issues]
- [Task dependency resolution]
- [Solutions implemented...]

## Test Results
- Decomposition tests: X/Y passed
- Communication tests: X/Y passed
- Integration tests: X/Y passed

## Lessons Learned
- Importance of clear task boundaries
- Need for timeout mechanisms
- [Additional insights...]

## Inter-Agent Communication Patterns
- Message format established
- Queue-based communication working
- Error escalation functional

## Next Steps
- Begin Phase 3: Add Code Review
- Optimize task assignment algorithm
- [Additional tasks...]

## Configuration Notes
- Planner config: src/configs/planner_agent.yaml
- Communication timeout: 30 seconds
- Max retry attempts: 3

## Sample Successful Workflow
[Include example of successful goal->tasks->completion]
```

## 🚀 Quick Start Commands

```bash
# Initialize Phase 2
python src/agents/planner.py --init

# Test communication
python tests/test_agent_communication.py

# Run integration test
python tests/test_phase_02_integration.py

# Execute sample workflow
python examples/planner_developer_demo.py
```

## ⚠️ Critical Reminders

1. **Maintain backward compatibility** - Developer Agent must still work
2. **Test communication thoroughly** - This is the foundation for all future phases
3. **Document message formats** - Other phases will use this protocol
4. **Handle timeouts gracefully** - Prevent system hangs
5. **Keep plans in memory** - For debugging and improvement

## 📔 PHASE COMPLETION REQUIREMENT

**YOU MUST WRITE A DEV JOURNAL ENTRY BEFORE ENDING THIS PHASE**

Document the working multi-agent system:
- Communication protocol details
- Message format examples
- Task decomposition patterns
- Integration test results

Save to: `/docs/dev_journals/[date]_phase02_complete.md`