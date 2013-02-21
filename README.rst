Model databank
==============

Models, scenarios and results data bank for water management purposes.

General requirements
--------------------

- models: 
    - metadata
    - configuration
    - distributed file system storage

- regions:
    - configurable region properties

- scenarios:
    - result metadata
    - states 
    - should be shareable among users

- rights and permissions:
    - scenario owners
    - model owners
    - owners can transfer scenarios and models to other users

- projects:
    wrapping models and scenarios per owner into a project

- various requirements:
    - import scenarios and results (?)
    - aggregations and aggregated results
    
- distributed file system (DFS:
    - models
    - results and states
    - aggregated results

General considerations
----------------------

- admin
    - for scenario and model editing
    - adding user and permissions
    - admin engine: django, custom

- model storage
    - relational (django ORM, SQLAlchemy, own)
    - MongoDB
    - file-based

- metadata
    - metadata in json or xml or nosql (mongodb) or in relational database
    - file based: version-control in theory possible
