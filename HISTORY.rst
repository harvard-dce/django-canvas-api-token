.. :changelog:

Release History
---------------

0.1.0 (2014-12-17)
++++++++++++++++++

* Birth!

0.1.1 (2014-12-18)
++++++++++++++++++

* fixed ``download_url`` in setup.py

0.1.2 (2015-01-07)
++++++++++++++++++

* fixed bug in utils.canvas_uri use of urlunparse
* added unique index to CanvasApiToken.user_id

0.2.0 (2015-04-28)
++++++++++++++++++

DB storage of canvas developer keys

* New model: CanvasDeveloperKey
* enable admin site
* make CanvasApiToken.user a foreign key into user model
