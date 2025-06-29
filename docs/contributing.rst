Contributing
============

We welcome contributions to the Options Flow Analyzer project!

Development Setup
-----------------

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

   git clone https://github.com/yourusername/options-flow-analyzer.git
   cd options-flow-analyzer

3. Create a virtual environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install development dependencies:

.. code-block:: bash

   pip install -r requirements-dev.txt

5. Install pre-commit hooks:

.. code-block:: bash

   pre-commit install

Running Tests
-------------

Run the test suite:

.. code-block:: bash

   pytest

Run tests with coverage:

.. code-block:: bash

   pytest --cov=options_flow_analyzer

Code Quality
------------

The project uses several tools to maintain code quality:

* **Black**: Code formatting
* **isort**: Import sorting
* **flake8**: Linting
* **mypy**: Type checking
* **safety**: Security scanning

These tools run automatically via pre-commit hooks and in CI/CD.

Submitting Changes
------------------

1. Create a feature branch:

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. Make your changes and add tests
3. Ensure all tests pass and code quality checks succeed
4. Commit your changes:

.. code-block:: bash

   git commit -m "Add your descriptive commit message"

5. Push to your fork and submit a pull request

Code Style
----------

* Follow PEP 8 style guidelines
* Use type hints for function signatures
* Write docstrings for all public functions and classes
* Keep functions focused and small
* Add tests for new functionality

Documentation
-------------

* Update documentation for any new features
* Use clear, concise language
* Include code examples where helpful
* Build docs locally to verify changes:

.. code-block:: bash

   cd docs
   make html
