Steps to release a package
--------------------------

For a first release:

1. `pip install xstatic-release`,
2. Add "dist", ".eggs" & "MANIFEST" to your .gitignore

For every release:

1. Update data and metadata in the xstatic/pkg/*MODULE_NAME* tree
2. Run `xstatic-release` to update `setup.cfg` (and generate missing files
   if needed)
3. Commit
4. Submit to gerrit for review
5. After the patch merges, git tag it with *PACKAGE_VERSION* and push that tag
   as per https://wiki.openstack.org/wiki/StableBranchRelease#Tag
6. Release package with "python setup.py sdist", "python setup.py bdist_wheel"


Releases
--------

- 1.2.0 Remove use of setuptools_scm and revert to more typical xstatic setup.py
- 1.1.3 Correct naming of summary -> description fields
- 1.1.2 First usable public release
