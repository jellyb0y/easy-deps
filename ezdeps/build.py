import setuptools
import sys
import os
from shutil import copyfile
from .manager import Manager
from .utils.constants import PACKAGE_FILE, CUR_DIR

def build(manager: Manager):
    sys.argv = [sys.argv[0], 'sdist', 'bdist_wheel']

    temp_file = f'{CUR_DIR}/{manager.name}/.ezdeps.json'
    copyfile(PACKAGE_FILE, temp_file)

    setuptools.setup(
        name=manager.name,
        version=manager.version,
        author='name' in manager.author and manager.author['name'],
        author_email='email' in manager.author and manager.author['email'],
        description=manager.description,
        long_description=manager.get_documentation(),
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(
            exclude=list(manager.dev_dependencies.keys())
        ),
        install_requires=manager.get_only_pip_requirements('peer'),
        include_package_data=manager.include_package_data,
        classifiers=manager.classifiers,
        python_requires=manager.python_requires
    )

    os.remove(temp_file)
