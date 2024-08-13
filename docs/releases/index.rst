=============
Release Notes
=============

Django Polly follows semantic versioning. This document outlines the changes in each version.

.. toctree::
   :maxdepth: 1

   0.0.5
   0.0.4
   0.0.3
   0.0.2
   0.0.1

0.0.5
-----

*Date: August 12th, 2024*

* Adding images to the documentation
* Update README.rst
* Update version

0.0.4
-----

*Date: August 12th, 2024*

* Publishing workflow to PyPi
* Update topics in setup.py
* Update README.rst
* Update version

0.0.3
-----

*Date: August 12th, 2024*

* Publishing workflow to PyPi
* Update topics in setup.py

0.0.2
-----

*Date: August 12th, 2024*

* Publishing workflow to PyPi

0.0.1
-----

*Date: August 12th, 2024*

We are excited to announce the initial release of Django Polly!

This version introduces the core functionality for integrating Language Learning Models (LLMs) into Django projects.

Features
^^^^^^^^

* LLM Integration:
   * Support for creating and managing LLM instances (Parrots)
   * Integration with various LLM backends
   * Configurable AI model path
* SmartConversations:
   * Framework for AI-powered conversations
   * Support for both synchronous and asynchronous communication styles
* WebSocket Support:
   * Real-time communication capabilities using Django Channels
   * Custom consumers for handling WebSocket connections
* Admin Interface:
   * Django admin integration for managing Parrots and SmartConversations
   * Custom admin actions for LLM management
* Management Commands:
   * `download_model` command for easy LLM model acquisition
* Extensibility:
   * Flexible architecture allowing for custom LLM backends
   * Easy integration with existing Django projects

Compatibility
^^^^^^^^^^^^^

* Python 3.8+
* Django 4.2 and 5.0
* Channels 3.0+

Installation
^^^^^^^^^^^^

You can install Django Polly 0.0.1 using pip:

.. code-block:: bash

    pip install django-polly==0.0.1

Be sure to follow the :doc:`installation guide </installation>` for complete setup instructions.

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

As this is the initial release, there are no upgrade instructions. For new installations, please refer to the :doc:`installation guide </installation>`.

Bug Fixes
^^^^^^^^^

As this is the initial release, there are no bug fixes to report.

Known Issues
^^^^^^^^^^^^

* Performance with very large LLM models may be suboptimal. We recommend using smaller, more efficient models for best results.
* WebSocket connections may require additional configuration in certain deployment environments.

Please report any issues you encounter on our `GitHub issue tracker <https://github.com/pollystack/django-polly/issues>`_.

What's Next
^^^^^^^^^^^

We are actively working on improving Django Polly. Future releases will focus on:

* Performance optimizations for LLM interactions
* Expanded LLM backend support
* Enhanced documentation and tutorials
* Improved error handling and debugging tools

Thank you for using Django Polly! We look forward to your feedback and contributions.