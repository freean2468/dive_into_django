=====
Neil-Auth-SDK
=====

Neil-Auth-SDK is a authentication module for the REST API.

Quick start
-----------

1. Add "auth_sdk" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'auth_sdk',
    ]

2. Include the auth_sdk URLconf in your project urls.py like this::

    path('auth_sdk/', include('auth_sdk.urls')),

3. Run ``python manage.py migrate`` to create the auth_sdk models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a user with auth (you'll need the Admin app enabled).

.. 5. Visit http://127.0.0.1:8000/auth_sdk/ to participate in the poll.