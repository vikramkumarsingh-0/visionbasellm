# 🤝 Contributing to Vision-Based Web Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Security Issues](#security-issues)

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility for mistakes

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of web automation
- Familiarity with Playwright and YOLOv8 (helpful but not required)

### Areas to Contribute

- 🐛 **Bug Fixes**: Fix issues in existing code
- ✨ **New Features**: Add new capabilities
- 📚 **Documentation**: Improve docs and examples
- 🧪 **Testing**: Add or improve tests
- 🔒 **Security**: Enhance security features
- 🌐 **Browser Support**: Improve browser compatibility
- 🎨 **UI/UX**: Improve user experience

---

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/vision-based-web-automation.git
cd vision-based-web-automation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black isort flake8 mypy

# Install browsers
playwright install chromium firefox webkit
```

### 4. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# (Optional: Add GROQ_API_KEY for Groq LLM)
```

### 5. Verify Setup

```bash
# Run tests
pytest test_simple.py

# Run security tests
pytest test_security.py -v

# Test all browsers
python test_all_browsers.py
```

---

## 🛠️ How to Contribute

### 1. Find an Issue

- Check [GitHub Issues](https://github.com/yourusername/vision-based-web-automation/issues)
- Look for `good first issue` or `help wanted` labels
- Or create a new issue to discuss your idea

### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-number-description
```

### 3. Make Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new features
- Update documentation

### 4. Test Your Changes

```bash
# Run all tests
pytest

# Run specific tests
pytest test_security.py -v

# Check code style
black . --check
isort . --check
flake8 .

# Type checking
mypy core/
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new browser detection feature"

# Or for bug fixes
git commit -m "fix: resolve issue with element matching"
```

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks
- `security:` - Security improvements

### 6. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

---

## 📝 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 100 characters

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports
isort .

# Check with flake8
flake8 .
```

### Naming Conventions

```python
# Classes: PascalCase
class BrowserEngine:
    pass

# Functions/methods: snake_case
def execute_task():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private methods: _leading_underscore
def _internal_method():
    pass
```

### Documentation

```python
def execute_task(url: str, task: str) -> dict:
    """
    Execute an automation task on a webpage.
    
    Args:
        url: The target webpage URL
        task: Natural language description of the task
        
    Returns:
        Dictionary containing execution results with keys:
        - status: 'success' or 'failure'
        - actions_taken: List of actions performed
        - error: Error message if failed
        
    Raises:
        ValueError: If URL is invalid
        SecurityError: If task contains malicious patterns
    """
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional

def process_elements(
    elements: List[Dict[str, any]], 
    threshold: float = 0.5
) -> Optional[Dict[str, any]]:
    """Process detected elements."""
    pass
```

---

## 🧪 Testing Guidelines

### Test Structure

```python
# test_feature.py
import pytest
from automation_agent import AutomationAgent

class TestFeature:
    """Test suite for new feature."""
    
    def setup_method(self):
        """Setup before each test."""
        self.agent = AutomationAgent()
    
    def test_basic_functionality(self):
        """Test basic feature functionality."""
        result = self.agent.execute_task(url, task)
        assert result['status'] == 'success'
    
    def test_edge_case(self):
        """Test edge case handling."""
        result = self.agent.execute_task(url, invalid_task)
        assert result['status'] == 'failure'
```

### Test Coverage

- Aim for 80%+ code coverage
- Test happy paths and edge cases
- Test error handling
- Test security features

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest test_security.py -v

# Run specific test
pytest test_security.py::test_prompt_injection -v
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Security considerations addressed

## Related Issues
Fixes #123
```

### Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: Get approval from maintainer
5. **Merge**: Maintainer merges PR

### After Merge

- Your contribution will be included in the next release
- You'll be added to the contributors list
- Thank you! 🎉

---

## 🔒 Security Issues

### Reporting Security Vulnerabilities

**DO NOT** open a public issue for security vulnerabilities.

Instead:

1. Email: security@example.com
2. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Security Contributions

- Review [SECURITY.md](SECURITY.md) for security architecture
- Check [ATTACK_PATTERNS.md](ATTACK_PATTERNS.md) for known patterns
- Run security tests: `pytest test_security.py -v`
- Follow [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md)

---

## 📚 Additional Resources

### Documentation

- [README.md](README.md) - Main documentation
- [GITHUB_SHOWCASE.md](GITHUB_SHOWCASE.md) - Complete showcase
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All docs
- [MULTI_BROWSER_GUIDE.md](MULTI_BROWSER_GUIDE.md) - Browser guide
- [INTELLIGENT_PLANNER_README.md](INTELLIGENT_PLANNER_README.md) - Planning guide

### Code Examples

- [example_usage.py](example_usage.py) - Basic examples
- [example_advanced_usage.py](example_advanced_usage.py) - Advanced examples
- [example_multi_browser.py](example_multi_browser.py) - Browser examples

### Architecture

- [MULTI_BROWSER_ARCHITECTURE.md](MULTI_BROWSER_ARCHITECTURE.md) - Architecture
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Roadmap

---

## 💡 Tips for Contributors

### Good First Issues

Look for issues labeled:
- `good first issue` - Easy for newcomers
- `help wanted` - Need community help
- `documentation` - Doc improvements
- `bug` - Bug fixes

### Communication

- Be clear and concise
- Ask questions if unclear
- Provide context in issues/PRs
- Be patient and respectful

### Best Practices

- **Small PRs**: Easier to review
- **One feature per PR**: Keep focused
- **Test thoroughly**: Prevent regressions
- **Document changes**: Help others understand

---

## 🎯 Contribution Ideas

### Easy

- Fix typos in documentation
- Add code examples
- Improve error messages
- Add unit tests

### Medium

- Add new browser features
- Improve element detection
- Enhance security patterns
- Add monitoring metrics

### Advanced

- Implement new AI models
- Add distributed processing
- Improve self-learning pipeline
- Add cloud deployment templates

---

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for making this project better! 🚀

---

## 📞 Questions?

- 💬 [GitHub Discussions](https://github.com/yourusername/vision-based-web-automation/discussions)
- 📧 Email: contribute@example.com
- 🐛 [GitHub Issues](https://github.com/yourusername/vision-based-web-automation/issues)

---

<div align="center">

**Happy Contributing! 🎉**

[Back to README](README.md) | [Code of Conduct](#code-of-conduct) | [Development Setup](#development-setup)

</div>
