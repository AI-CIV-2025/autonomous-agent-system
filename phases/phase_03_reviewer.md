# Phase 3: Add Code Review and Quality Assurance

## 🎯 Objective
Improve code quality and reliability by introducing a Reviewer Agent that critiques and tests the Developer's output, providing an internal "quality gate" before changes are finalized. Establish an internal review loop for software tasks.

## 📋 Complete Task List

### Pre-Build Tasks
- [ ] Research automated code review techniques
- [ ] Research static analysis integration patterns
- [ ] Research testing frameworks and patterns
- [ ] Study code quality metrics
- [ ] Review Phases 1-2 implementation

### Core Implementation Tasks
- [ ] Create Reviewer Agent configuration
- [ ] Implement Reviewer Agent class
- [ ] Design Reviewer prompt template
- [ ] Implement code analysis capabilities
- [ ] Add syntax checking functionality
- [ ] Create bug detection logic
- [ ] Implement style checking
- [ ] Add requirements validation
- [ ] Create feedback generation system
- [ ] Implement revision request protocol
- [ ] Add test execution capability
- [ ] Create approval/rejection mechanism
- [ ] Implement quality metrics tracking
- [ ] Add review history logging

### Integration Tasks
- [ ] Connect Reviewer to workflow pipeline
- [ ] Implement Developer-Reviewer feedback loop
- [ ] Create revision handling in Developer
- [ ] Add Planner notification for reviews
- [ ] Implement review queuing system
- [ ] Add review status tracking

### Testing Tasks
- [ ] Test code analysis accuracy
- [ ] Test bug detection capabilities
- [ ] Test feedback loop functionality
- [ ] Test revision process
- [ ] Test approval workflow
- [ ] Test error escalation
- [ ] Run end-to-end review scenario

### Documentation Tasks
- [ ] Document review criteria
- [ ] Create quality standards guide
- [ ] Write feedback format specification
- [ ] Complete development journal entry

## 🔍 Research Web Searches

1. **"automated code review AI techniques static analysis 2024"**
   - Modern approaches to automated review
   - Integration with AI agents

2. **"code quality metrics Python JavaScript best practices"**
   - Key metrics to track
   - Language-specific considerations

3. **"test driven development automation continuous integration"**
   - Automated testing strategies
   - Test execution patterns

4. **"code review feedback patterns constructive criticism"**
   - Effective feedback generation
   - Clear communication of issues

5. **"bug detection patterns common programming errors"**
   - Common bug patterns to check
   - False positive reduction

## 💻 Code Requirements

### 1. Reviewer Agent Configuration (`src/configs/reviewer_agent.yaml`)
```yaml
agent:
  name: "reviewer_agent"
  role: "Code Reviewer AI"
  description: "Reviews code for quality, bugs, and compliance"
  
tools:
  - filesystem_mcp
  - basic_memory_mcp
  - testing_framework
  
capabilities:
  - analyze_code
  - detect_bugs
  - check_style
  - run_tests
  - provide_feedback
  - approve_changes
  
review_criteria:
  - syntax_validity
  - logic_correctness
  - style_compliance
  - test_coverage
  - documentation_quality
  
thresholds:
  min_test_coverage: 80
  max_complexity: 10
  max_line_length: 100
```

### 2. Reviewer Agent Prompt (`src/prompts/reviewer_prompt.md`)
```markdown
You are a Code Reviewer AI. Your role is to scrutinize code for errors, bugs, and quality issues.

Review Criteria:
1. Syntax and correctness
2. Logic and algorithm efficiency
3. Style and conventions
4. Test coverage
5. Documentation completeness

Feedback Format:
- Be specific about issues
- Provide line numbers when relevant
- Suggest concrete improvements
- Distinguish critical from minor issues

Current Code: {code}
Original Requirements: {requirements}
Test Results: {test_results}
```

### 3. Reviewer Implementation (`src/agents/reviewer.py`)
```python
import ast
import re
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ReviewFeedback:
    severity: str  # critical, major, minor
    category: str  # bug, style, performance, etc
    line_number: Optional[int]
    message: str
    suggestion: Optional[str]

@dataclass
class ReviewResult:
    approved: bool
    feedback: List[ReviewFeedback]
    metrics: Dict[str, float]
    
class ReviewerAgent:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.review_history = []
        
    def review_code(self, code: str, requirements: str) -> ReviewResult:
        """Perform comprehensive code review"""
        feedback = []
        
        # Syntax check
        syntax_issues = self.check_syntax(code)
        feedback.extend(syntax_issues)
        
        # Logic analysis
        logic_issues = self.analyze_logic(code)
        feedback.extend(logic_issues)
        
        # Style check
        style_issues = self.check_style(code)
        feedback.extend(style_issues)
        
        # Calculate metrics
        metrics = self.calculate_metrics(code)
        
        # Determine approval
        critical_issues = [f for f in feedback if f.severity == "critical"]
        approved = len(critical_issues) == 0
        
        return ReviewResult(approved, feedback, metrics)
    
    def check_syntax(self, code: str) -> List[ReviewFeedback]:
        """Check for syntax errors"""
        feedback = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            feedback.append(ReviewFeedback(
                severity="critical",
                category="syntax",
                line_number=e.lineno,
                message=f"Syntax error: {e.msg}",
                suggestion="Fix syntax before proceeding"
            ))
        return feedback
    
    def run_tests(self, test_file: str) -> Dict:
        """Execute tests and return results"""
        pass
        
    def request_revision(self, task_id: str, feedback: List[ReviewFeedback]):
        """Send revision request to developer"""
        pass
```

### 4. Review Pipeline (`src/tools/review_pipeline.py`)
```python
class ReviewPipeline:
    def __init__(self, planner, developer, reviewer):
        self.planner = planner
        self.developer = developer
        self.reviewer = reviewer
        
    def process_task(self, task):
        """Process task through review pipeline"""
        # Developer implements
        code = self.developer.implement_task(task)
        
        # Reviewer reviews
        review = self.reviewer.review_code(code, task.requirements)
        
        # Handle review result
        if review.approved:
            self.planner.mark_task_complete(task.id)
        else:
            # Request revision
            self.developer.revise_code(code, review.feedback)
            # Re-review
            self.process_task(task)
```

## 🧪 Testing Regime

### Test Scenario 1: Code Analysis
```python
# tests/test_phase_03_analysis.py
def test_syntax_error_detection():
    """Test detection of syntax errors"""
    bad_code = "def func(:\n    pass"
    review = reviewer.review_code(bad_code, "")
    assert not review.approved
    assert any(f.category == "syntax" for f in review.feedback)

def test_logic_error_detection():
    """Test detection of logic errors"""
    code_with_bug = "def divide(a, b):\n    return a / b"  # No zero check
    review = reviewer.review_code(code_with_bug, "Safe division function")
    assert any("zero" in f.message.lower() for f in review.feedback)
```

### Test Scenario 2: Feedback Loop
```python
# tests/test_phase_03_feedback.py
def test_revision_request():
    """Test revision request process"""
    initial_code = create_buggy_code()
    review = reviewer.review_code(initial_code, requirements)
    
    assert not review.approved
    
    # Developer receives feedback
    revised_code = developer.revise_code(initial_code, review.feedback)
    
    # Re-review
    second_review = reviewer.review_code(revised_code, requirements)
    assert second_review.approved

def test_feedback_clarity():
    """Test that feedback is actionable"""
    review = reviewer.review_code(sample_code, requirements)
    for feedback in review.feedback:
        assert feedback.message
        if feedback.severity == "critical":
            assert feedback.suggestion
```

### Test Scenario 3: Quality Metrics
```python
# tests/test_phase_03_metrics.py
def test_complexity_calculation():
    """Test code complexity metrics"""
    complex_code = create_complex_function()
    review = reviewer.review_code(complex_code, "")
    assert "complexity" in review.metrics
    assert review.metrics["complexity"] > 10

def test_coverage_check():
    """Test coverage requirements"""
    code_without_tests = "def func(): pass"
    review = reviewer.review_code(code_without_tests, "Must have tests")
    assert not review.approved
    assert any("test" in f.message.lower() for f in review.feedback)
```

### Test Scenario 4: Integration
```python
# tests/test_phase_03_integration.py
def test_full_review_pipeline():
    """Test complete review pipeline"""
    # Planner assigns task
    task = planner.create_task("Implement calculator")
    
    # Developer implements
    code = developer.implement_task(task)
    
    # Reviewer reviews
    review = reviewer.review_code(code, task.requirements)
    
    # Handle feedback loop
    while not review.approved:
        code = developer.revise_code(code, review.feedback)
        review = reviewer.review_code(code, task.requirements)
    
    assert review.approved
    assert task.status == "completed"
```

### Test Scenario 5: Edge Cases
```python
# tests/test_phase_03_edge_cases.py
def test_empty_code_handling():
    """Test review of empty code"""
    review = reviewer.review_code("", "Implement function")
    assert not review.approved
    assert any("empty" in f.message.lower() for f in review.feedback)

def test_perfect_code():
    """Test approval of good code"""
    perfect_code = load_perfect_sample()
    review = reviewer.review_code(perfect_code, "Sample requirements")
    assert review.approved
    assert len(review.feedback) == 0 or all(f.severity == "minor" for f in review.feedback)
```

## ✅ Expected Outcomes

### Functional Outcomes
1. **Working Reviewer Agent**: Comprehensive code review capability
2. **Quality Gates**: Prevents bad code from being finalized
3. **Feedback Loop**: Effective Developer-Reviewer interaction
4. **Metrics Tracking**: Quantitative code quality measurement
5. **Improved Output**: Higher quality code after review

### Deliverables
- `src/agents/reviewer.py` - Reviewer implementation
- `src/configs/reviewer_agent.yaml` - Reviewer configuration
- `src/prompts/reviewer_prompt.md` - Reviewer prompt
- `src/tools/review_pipeline.py` - Review pipeline
- `tests/test_phase_03_*.py` - Test suite
- `memory/reviews/` - Review history directory

### Success Metrics
- [ ] Bug detection rate > 85%
- [ ] False positive rate < 10%
- [ ] Average revision cycles < 3
- [ ] Code quality improvement > 30%
- [ ] Review completion time < 60 seconds

## 📝 Development Journal Entry Template

```markdown
# Development Journal - Phase 3 - [DATE]

## Work Completed
- Implemented Reviewer Agent
- Set up review pipeline
- Created feedback system
- Integrated with Developer and Planner
- [Additional items...]

## Challenges Encountered
- Balancing thoroughness vs speed
- Reducing false positives
- Making feedback actionable
- [Solutions...]

## Test Results
- Code analysis: X/Y passed
- Feedback loop: X/Y passed
- Integration: X/Y passed

## Quality Improvements Observed
- Bug reduction: X%
- Code quality score increase: Y points
- Average revisions needed: Z

## Lessons Learned
- Importance of clear feedback
- Need for configurable thresholds
- [Additional insights...]

## Next Steps
- Begin Phase 4: Persistent Memory
- Fine-tune review criteria
- [Additional tasks...]

## Sample Review Session
[Include example of code->review->revision->approval]
```

## 🚀 Quick Start Commands

```bash
# Initialize Phase 3
python src/agents/reviewer.py --init

# Test review functionality
python tests/test_reviewer_analysis.py

# Run review pipeline
python examples/review_pipeline_demo.py

# Check review metrics
python tools/review_metrics.py --summary
```

## ⚠️ Critical Reminders

1. **Don't break existing workflow** - Planner-Developer must still work
2. **Make feedback actionable** - Vague feedback helps no one
3. **Balance strictness** - Too strict blocks progress
4. **Document review criteria** - Consistency is key
5. **Log all reviews** - For learning and improvement
## 📔 PHASE COMPLETION REQUIREMENT

**YOU MUST WRITE A DEV JOURNAL ENTRY BEFORE ENDING THIS PHASE**

Critical items to document:
- Working configurations and setup commands
- Integration points with previous phases
- Test results and what's verified working
- Any challenges solved and solutions
- Clear next steps for the next phase

Save to: `/docs/dev_journals/[date]_phaseXX_complete.md`

After writing, you can clear context knowing the next session will have everything needed.
