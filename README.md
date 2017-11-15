## django-canvas-api-token

A reusable django app for handling the workflow of generating per-user
Canvas API oauth tokens. The app assumes that your django project is using the
[django_auth_lti](https://github.com/Harvard-University-iCommons/django-auth-lti)
middleware.

Install
-------

    pip install django-canvas-api-token

Setup
-----

1. Add `"canvas_api_token"` to your `INSTALLED_APPS` in django settings
2. Insert the url configuration into your project/app urls.py
    ```
    url(r'^canvas_api_token/', include('canvas_api_token.urls'))
    ```
3. Run `python manage.py migrate` to ensure db tables are initialized.
4. Use the admin site to create a `canvas_dev_key` entry using the `consumer_key` and developer key values from your Canvas consumer where ...

* `client_id` is the integer client id value of your Canvas [developer key](https://canvas.instructure.com/doc/api/file.oauth.html)
* `client_secret` is the random string 'secret' value of your Canvas developer key

#### Example developer_key usage

If you are making use of the [canvas-docker](https://hub.docker.com/r/lbjay/canvas-docker/) image for development it comes
with a pre-loaded developer key. If, in addition, you are using this extension app (django-canvas-api-token) 
within [harvard-dce/dce_course_admin](https://github.com/harvard-dce/dce_course_admin) and using the example consumer key,
the developer key record values would be:

* `client_id=1`
* `client_secret=test_developer_key`
* `consumer_key=dce_course_admin`

## License
django-canvas-api-token is licensed under the BSD license

## Copyright
2017 President and Fellows of Harvard College
