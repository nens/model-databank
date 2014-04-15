Changelog of model-databank
===================================================


0.5 (unreleased)
----------------

- Upgraded for use in Django 1.5.

- Fix file list.

- Create a bare repository when creating a new repository.

- Restrict uploading a new model by requiring a permission.

- Add last update date as column to repo list.

- Use "Model Databank" as first committer.
  
- Add sqlite to large files.


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
