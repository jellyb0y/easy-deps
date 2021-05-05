import setuptools
import sys
import os
from shutil import copyfile
from .manager import Manager
from .utils.constants import PACKAGE_FILE, CUR_DIR
from .utils.packages import get_pip_requirements

def build(manager: Manager):
    sys.argv = [sys.argv[0], 'sdist', 'bdist_wheel']

    temp_file = f'{CUR_DIR}/{manager.name}/.ezdeps.json'
    copyfile(PACKAGE_FILE, temp_file)

    print(manager.scripts)

    setuptools.setup(
        name=manager.name,
        version=manager.version,
        author='name' in manager.author and manager.author['name'],
        author_email='email' in manager.author and manager.author['email'],
        description=manager.description,
        url=manager.url,
        scripts=manager.scripts,
        long_description=manager.get_documentation(),
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        install_requires=get_pip_requirements(manager.get_requirements('default')),
        include_package_data=manager.include_package_data,
        classifiers=manager.classifiers,
        python_requires=manager.python_requires
    )

    os.remove(temp_file)
