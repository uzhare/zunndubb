.. {% comment %}

========================
Django App Template
========================
A django app template we use at ikraft_ for almost all of our
projects.

Please add issues for any feedback.

Use it with our django-project-layout_

Note about distributable and reusable apps
==========================================

According to conventions at iKraft_, a distributable app is one that is made available to general public via PyPI, Crate.io or similar python package indexes, while a reusable app is one which can be used between projects by simply copying and pasting the app inside the project of adding it to PYTHONPATH. Therefore, we understand that every distributable app is reusable but not every reusable app is distributable.

The purpose of this app template is to be used in the context of a django project, preferably with django-project-layout_. A django project usually contains a number of apps that are so specific to the project that they will never be distributed. That is the usecase this template targets. The purpose is not to create a distributable apps. 

That said, packaging and creating a distributable a django app based on this templates should be very trivial. Just use the scripts/packageit.py from django-project-layout_

Usage
=====
Use following command to use it in your own project::

    $ cd /path/to/django/project/app_dir
    $ django-admin.py startapp testproject --template=https://github.com/ikraft/django-project-template/zipball/master 

Directory Layout
================
::

    ├── admin.py
    ├── forms.py
    ├── management
    │   └── __ini__.py
    ├── middleware
    │   └── __init__.py
    ├── models.py
    ├── templates
    ├── templatetags
    │   └── __init__.py
    ├── tests.py
    ├── urls.py
    └── views.py


.. _iKraft: http://ikraftsoft.com
.. _django-project-layout: https://github.com/ikraft/django-project-template 

-----

.. note:: This file will become an empty README.rst of the new app. Everything above this will not be included in README.rst

.. {% endcomment %}


