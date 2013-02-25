git-annex for version-control of model data
###########################################

git-annex
---------

From their `website <http://git-annex.branchable.com/>`_: git-annex allows 
managing files with git, without checking the file contents into git. While 
that may seem paradoxical, it is useful when dealing with files larger than 
git can currently easily handle, whether due to limitations in memory, time, 
or disk space.

In particular, git-annex's location tracking allows having many repositories 
with a partial set of files.

considerations for our use case
-------------------------------

git-annex can be used to diff model description files (.mdu or other) while 
keeping the related files in a connected separate git annex repo, linking the
data files to a cloud solution, like S3, own solution, etc.. That way we won't 
have to store big binary files in your main repo. Git itself is not very 
adequate for that. 


git-annex advantages
--------------------

- no need to develop custom tool

- built on top of git

- actively developped

- only checkout the needed model related files


git-annex disadvantages
-----------------------

- still under development, but is usable already on UNIX-like systems

- windows support is being worked on, but at this stage  


git-annex challenges
--------------------

- connecting .mdu (or other file descriptor) with the right *.asc, *.rgb, *.grd
  files


