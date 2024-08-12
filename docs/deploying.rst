Deploying
=========

This guide covers the basics of deploying a Django project with Django Polly in a production environment.

Prerequisites
-------------

- A Django project with Django Polly installed and configured
- A production-ready database (e.g., PostgreSQL)
- An ASGI server (e.g., Daphne or Uvicorn)

Steps for Deployment
--------------------

1. Configure Production Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update your Django settings for production:

.. code-block:: python

    DEBUG = False
    ALLOWED_HOSTS = ['yourdomain.com']

    # Configure database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Configure static files
    STATIC_ROOT = '/path/to/static/'
    STATIC_URL = '/static/'

2. Set Up ASGI Server
^^^^^^^^^^^^^^^^^^^^^

Install an ASGI server like Daphne:

.. code-block:: bash

    pip install daphne

3. Collect Static Files
^^^^^^^^^^^^^^^^^^^^^^^

Run the collectstatic management command:

.. code-block:: bash

    python manage.py collectstatic

4. Set Up a Process Manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use a process manager like Supervisor to manage your ASGI server. Create a configuration file (e.g., `/etc/supervisor/conf.d/django_polly.conf`):

.. code-block:: ini

    [program:django_polly]
    command=/path/to/venv/bin/daphne -p 8001 your_project.asgi:application
    directory=/path/to/your/project
    user=your_user
    autostart=true
    autorestart=true
    redirect_stderr=true

5. Set Up a Reverse Proxy
^^^^^^^^^^^^^^^^^^^^^^^^^

Configure a reverse proxy (e.g., Nginx) to handle static files and forward requests to your ASGI server:

.. code-block:: nginx

    server {
        listen 80;
        server_name yourdomain.com;

        location /static/ {
            alias /path/to/static/;
        }

        location / {
            proxy_pass http://localhost:8001;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

6. SSL/TLS Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

For secure WebSocket connections, configure SSL/TLS on your reverse proxy.

7. Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^

Use environment variables for sensitive information like secret keys and API credentials.

8. Database Migration
^^^^^^^^^^^^^^^^^^^^^

Run database migrations:

.. code-block:: bash

    python manage.py migrate

9. Start Services
^^^^^^^^^^^^^^^^^

Start or restart Supervisor and Nginx:

.. code-block:: bash

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start django_polly
    sudo service nginx restart

Monitoring and Maintenance
--------------------------

- Set up logging to monitor your application's performance and errors.
- Regularly update Django, Django Polly, and other dependencies.
- Implement a backup strategy for your database and user-generated content.

For more advanced deployment scenarios or platform-specific instructions, consult the Django deployment documentation and your hosting provider's guidelines.