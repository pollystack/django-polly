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

Issue: LLM model not loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Verify that you've downloaded the LLM model using the `download_model` management command.
2. Check that the `AI_MODELS_PATH` in your settings.py points to the correct directory.
3. Ensure you have sufficient disk space and memory to load the model.

Issue: Slow response times from LLM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Consider using a smaller or more efficient LLM model.
2. Increase the resources (CPU/RAM) available to your application.
3. Implement caching for common queries to reduce load on the LLM.

WebSocket Connection Issues
---------------------------

Issue: WebSocket connection fails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Ensure that Daphne is installed and configured correctly.
2. Check that `ASGI_APPLICATION` is set correctly in your settings.py.
3. Verify that your `CHANNEL_LAYERS` configuration is correct.

Issue: Real-time updates not working
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Check your browser console for JavaScript errors.
2. Ensure that your frontend code is correctly connecting to the WebSocket.
3. Verify that your consumer is properly configured to send updates.

Database Issues
---------------

Issue: Database migrations failing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Solution:
1. Ensure you're running the latest version of Django Polly.
2. Try running `python manage.py makemigrations django_polly` before migrating.
3. Check the database logs for any specific error messages.

General Troubleshooting Tips
----------------------------

1. Check the Django Polly logs for any error messages or warnings.
2. Ensure all dependencies are up to date.
3. Verify that your Django and Python versions are compatible with Django Polly.
4. If all else fails, try creating a new virtual environment and reinstalling Django Polly and its dependencies.

If you're still experiencing issues after trying these solutions, please open an issue on the Django Polly GitHub repository with a detailed description of your problem and the steps you've taken to resolve it.
