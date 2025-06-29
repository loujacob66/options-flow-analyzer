Installation
============

Requirements
------------

* Python 3.8 or higher
* pip package manager

Installing from Source
----------------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/yourusername/options-flow-analyzer.git
   cd options-flow-analyzer

2. Install dependencies:

.. code-block:: bash

   pip install -r requirements.txt

3. (Optional) Install development dependencies:

.. code-block:: bash

   pip install -r requirements-dev.txt

Development Setup
-----------------

For development, install pre-commit hooks:

.. code-block:: bash

   pre-commit install

This will run code quality checks before each commit.

Verification
------------

Verify the installation by running:

.. code-block:: bash

   python -m options_flow_analyzer --version
