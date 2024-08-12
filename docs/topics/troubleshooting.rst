Troubleshooting
===============

This guide covers common issues you might encounter when using Django Polly and how to resolve them.

Installation Issues
-------------------

Issue: ImportError when trying to use Django Polly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Ensure Django Polly is installed: `pip install django-polly`
2. Check that 'django_polly' is in INSTALLED_APPS in your Django settings.
3. Run `python manage.py migrate` to apply any pending migrations.

LLM Integration Problems
------------------------

Issue