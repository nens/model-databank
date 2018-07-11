Changelog of model-databank
===================================================


0.18 (unreleased)
-----------------

- Added pagination for commits/files page.

- Added a limit to the max number of commits shown for a ReferenceModel


0.17 (2017-07-27)
-----------------

- Fix bug in ``process_uploaded_model_files`` management command (caused by
  upgrading Django to 1.11.x -> template.render() expects a dict as argument,
  not a Context instance).


0.16 (2017-07-21)
-----------------

- Require login for page views. Handle permissions via the 3Di permissions
  backend.

- Run tests on Jenkins with Jenkinsfile and docker-compose.


0.15 (2017-06-21)
-----------------

- Upgrade bootstrap.py, use ez_setup.py and pin zc.buildout to 2.9.3.

- Handle access permission by the 3Di permission API (change_model permission
  required).


0.14 (2017-02-14)
-----------------

- Fix /api/models endpoint.


0.13 (2016-11-15)
-----------------

- Upgrade to Django 1.10.3.


0.12 (2016-04-20)
-----------------

- Add search field to ModelReference and ModelUpload admin pages.

- Update bootstrap.py, zc.buildout and zc.recipe.egg.

- Pin Django to 1.5: same as threedi-msr.


0.11 (2014-08-25)
-----------------

- Store model type in database to make it easier to add a model type.


0.10 (2014-05-15)
-----------------

- Remove uploaded zipfiles after 14 days and other small fixes to that script.


0.9 (2014-05-15)
----------------

- Remove uploaded zipfiles after 30 days.


0.8 (2014-05-01)
----------------

- Improve processed zip filename.


0.7 (2014-04-29)
----------------

- Add check for duplicate ftp upload.


0.6 (2014-04-28)
----------------

- Fix anonymous user bug.


0.5 (2014-04-24)
----------------

- Upgraded for use in Django 1.5.

- Fix file list.

- Create a bare repository when creating a new repository.

- Restrict uploading a new model by requiring a permission.

- Add last update date as column to repo list.

- Use "Model Databank" as first committer.

- Add sqlite to large files.

- Add organisations to models.

- Create an upload directory for manually uploading models.

- Add slug and ssh url to api list view.

- Improve copyright year.


0.4 (2013-07-08)
----------------

- Add ModelReference.description field to accomodate for
  ModelUpload.description field.

- Remove ModelReference.comment field.


0.3 (2013-06-12)
----------------

- Add api.html template.


0.2 (2013-06-12)
----------------

- Add API for model reference list.

- Fix installation of django-rest-framework.


0.1 (2013-06-12)
----------------

- Initial project structure created with nensskel 1.32.
