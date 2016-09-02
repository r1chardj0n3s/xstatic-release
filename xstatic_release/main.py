"""
OpenStack XStatic package release helper
"""

import importlib
import os
import subprocess
import sys


PKG_DIR = 'xstatic/pkg'

CFG_TEMPLATE = '''[metadata]
name = {0.PACKAGE_NAME}
description = {0.DESCRIPTION}
description-file = README.rst
maintainer = {0.MAINTAINER}
maintainer-email = {0.MAINTAINER_EMAIL}
home-page = {0.HOMEPAGE}
keywords = {0.KEYWORDS}
license = {0.LICENSE}
zip_safe = False
namespace_packages =
    xstatic
    xstatic.pkg

[files]
packages =
    xstatic

[bdist_wheel]
universal = True
'''

PY_TEMPLATE = '''from setuptools import setup, find_packages

# The README.txt file should be written in reST so that PyPI can use
# it to generate your project's PyPI page.
long_description = open('README.txt').read()

setup(
    name='{0.PACKAGE_NAME}',
    description="""{0.DESCRIPTION}""",
    long_description=long_description,
    maintainer="{0.MAINTAINER}",
    maintainer_email='{0.MAINTAINER_EMAIL}',
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'wheel'],
    packages=find_packages(),
    include_package_data=True
)
'''

MANIFEST_TEMPLATE = '''include README.txt
recursive-include xstatic *
global-exclude *.pyc
global-exclude *.pyo
global-exclude *.orig
global-exclude *.rej
'''


class XStaticError(Exception):
    pass


def import_xstatic():
    names = [name for name in os.listdir(PKG_DIR)
             if os.path.isdir(os.path.join(PKG_DIR, name))]
    if not names:
        raise XStaticError("no XStatic packages found")
    elif len(names) > 1:
        raise XStaticError("more than one XStatic package found")
    xs = importlib.import_module('xstatic.pkg.{}'.format(names[0]))
    return xs


def get_git_tags():
    return set(
        subprocess.check_output('git tag -l', shell=True).splitlines()
    )


def version_is_tagged(version):
    releases = get_git_tags()
    return version in releases


def write_files(xs):
    for filename, template in (
        ('setup.cfg', CFG_TEMPLATE),
        ('setup.py', PY_TEMPLATE),
        ('MANIFEST.in', MANIFEST_TEMPLATE),
    ):
        with open(filename, 'w') as f:
            f.write(template.format(xs))


def main():
    xs = import_xstatic()
    if version_is_tagged(xs.PACKAGE_VERSION):
        sys.exit(
"""FAIL: Package release {0} already tagged (so is assumed released)
Increment package BUILD in {1}/{2}/__init__.py""".format(
            xs.PACKAGE_VERSION, PKG_DIR, xs.PACKAGE_NAME))
    write_files(xs)
