# Contributing to Options Flow Analyzer

Thank you for your interest in contributing to Options Flow Analyzer! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/options-flow-analyzer.git
   cd options-flow-analyzer
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run tests** to make sure everything works:
   ```bash
   python -m pytest tests/
   ```

## Development Workflow

1. **Create a new branch** for your feature/bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the project structure:
   - `options_analyzer/` - Main package code
   - `tests/` - Test files
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   python -m pytest tests/ -v
   python -m options_analyzer demo SPY  # Test CLI
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

5. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

- **Python Version**: Support Python 3.8+
- **Code Style**: Follow PEP 8 guidelines
- **Documentation**: Add docstrings for new functions/classes
- **Testing**: Add tests for new features

## Areas for Contribution

### High Priority
- [ ] Additional data providers (Alpha Vantage, CBOE, etc.)
- [ ] Enhanced sweep detection algorithms
- [ ] Real-time data streaming
- [ ] Options Greeks calculations
- [ ] Export functionality (CSV, JSON)

### Medium Priority
- [ ] Web dashboard (Flask/FastAPI)
- [ ] Database integration
- [ ] Backtesting capabilities
- [ ] Custom alerts system
- [ ] Performance optimizations

### Documentation
- [ ] API documentation
- [ ] Usage examples
- [ ] Video tutorials
- [ ] Trading strategy guides

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages

## Feature Requests

For feature requests, please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Provide examples if possible

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
