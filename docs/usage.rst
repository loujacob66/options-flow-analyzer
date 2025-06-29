Usage
=====

Command Line Interface
----------------------

The Options Flow Analyzer provides a command-line interface for easy usage:

.. code-block:: bash

python -m options_flow_analyzer [OPTIONS]

Available Options
-----------------

* ``--help``: Show help message and exit
* ``--version``: Show version information
* ``--config FILE``: Specify configuration file path
* ``--verbose``: Enable verbose logging

Examples
--------

Basic usage:

.. code-block:: bash

   python -m options_flow_analyzer

With configuration file:

.. code-block:: bash

   python -m options_flow_analyzer --config config.yaml

Verbose output:

.. code-block:: bash

   python -m options_flow_analyzer --verbose

Configuration
-------------

The analyzer can be configured using a YAML configuration file. Example:

.. code-block:: yaml

   # config.yaml
   market_data:
     source: "your_data_source"
     api_key: "your_api_key"
   
   analysis:
     timeframe: "1d"
     filters:
       - volume_threshold: 1000
       - price_range: [0.50, 10.00]

Python API
----------

You can also use the analyzer programmatically:

.. code-block:: python

from options_flow_analyzer import analyzer
   
   analyzer_instance = analyzer.OptionsAnalyzer()
   results = analyzer_instance.analyze()
   print(results)
