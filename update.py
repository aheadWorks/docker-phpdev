#!/usr/bin/env python3
"""
Run to generate Dockerfiles for desired PHP versions
"""
from pathlib import Path
from shutil import copyfile
from distutils.version import StrictVersion


head = """#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.py"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#
"""

files_to_copy = ("nginx.conf", "entrypoint.py")

php_versions = {
    "7.4": files_to_copy,
    "7.3": files_to_copy,
    "7.2": files_to_copy,
    "7.1": files_to_copy,
    "7.0": files_to_copy,
    "5.6": files_to_copy
}

with open('Dockerfile.template') as df:
    contents = df.read()

    for ver, files in php_versions.items():

        for xdebug in ["", "1"]:
            path = (Path() / (ver + ("-xdebug" if xdebug else "")))
            path.mkdir(exist_ok=True)

            # Install old XDebug for PHP 5.6 family
            xdv = ''
            if StrictVersion(ver) <= StrictVersion('5.6.99') and xdebug:
                xdv = '-2.5.5'

            new_content = contents\
                .replace('%%PHP_VERSION%%', ver)\
                .replace('%%WITH_XDEBUG%%', xdebug)\
                .replace('%%XDEBUG_VERSION%%', xdv)



            (path / 'Dockerfile').write_text(head + new_content)
            for p in Path().glob('*'):
                if p.name in files:
                    copyfile(p, path / p.name)