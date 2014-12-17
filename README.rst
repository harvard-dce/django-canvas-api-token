=======================
django-canvas-api-token
=======================

A reusable django app for handling the oauth workflow of generating per-user
Canvas API oauth tokens. The app assumes that your django project is using the
`django_auth_lti <https://github.com/Harvard-University-iCommons/django-auth-lti>`_
middleware.

Install
-------

.. code-block:: bash

    pip install django-canvas-api-token

Setup
-----

1. Add ``"canvas_api_token"`` to your ``INSTALLED_APPS`` settings
2. Insert the url configuration into your project/app urls.py

.. code-block:: python

    url(r'^canvas_api_token/', include('canvas_api_token.urls'))

3. Add a ``LTI_APP_DEVELOPER_KEYS`` entry to your settings that looks like this:

.. code-block:: python

    LTI_APP_DEVELOPER_KEYS = {
        '[oauth-consumer-key]': {
            'client_id': '[client_id]',
            'client_secret': '[client_secret]'
        }
    }

where ...

* ``oauth_consumer_key`` value is the consumer key used when registering your LTI tool in the Canvas account admin
* ``client_id`` is the integer client id value of your Canvas `developer key <https://canvas.instructure.com/doc/api/file.oauth.html>`_
* ``client_secret`` is the random string 'secret' value of your Canvas developer key

License
-------
django-canvas-api-token is licensed under the Apache 2.0 license

Copyright
---------
2014 President and Fellows of Harvard College
