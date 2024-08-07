from setuptools import setup, find_packages

setup(
    name='django-polly',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='AGPL-3.0',
    description='A Django app for building parrot configurations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pollystack/django-polly',
    author='Pollystack Team',
    author_email='info@pollystack.com',
    # ... other parameters ...
    install_requires=[
        'Django>=3.2',
        'django-json-widget',
        'djangorestframework',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: LLM Management',
    ],
)