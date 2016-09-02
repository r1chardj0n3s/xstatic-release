"""
OpenStack xstatic package release helper
"""

import importlib
import os
import subprocess
import sys


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


def main():
    xs = name = None
    for name in os.listdir('xstatic/pkg'):
        if os.path.isdir('xstatic/pkg/' + name):
            if xs is not None:
                sys.exit('More than one xstatic.pkg package found.')
            xs = importlib.import_module('xstatic.pkg.' + name)

    if xs is None:
        sys.exit('No xstatic.pkg package found.')

    releases = set(
        subprocess.check_output('git tag -l', shell=True).splitlines()
    )
    if xs.PACKAGE_VERSION in releases:
        sys.exit('''\
FAIL: Package release {} already tagged (so is assumed released)
Increment package BUILD in xstatic/pkg/{}/__init__.py'''.format(
            xs.PACKAGE_VERSION, name))

    with open('setup.cfg', 'w') as f:
        f.write(CFG_TEMPLATE.format(xs))

    with open('setup.py', 'w') as f:
        f.write(PY_TEMPLATE.format(xs))

    with open('MANIFEST.in', 'w') as f:
        f.write(MANIFEST_TEMPLATE)
