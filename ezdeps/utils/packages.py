import re
from os import system
from pkg_resources import get_distribution

def parse_version(version: str):
    """
    Returns parsed version from .ezdeps.json
    """

    eq_type = '=='
    if version[0] == '^':
        eq_type = '>='
        version = version[1:]

    return eq_type + version

def parse_packages(packages: str):
    """
    Returns parsed packages from cli
    """

    regexp = re.compile(r'^([a-zA-Z_-]*)(?:@([^#]*))?(?:#(.*))?$')
    parsed_packages = {}

    for package in packages:
        match = regexp.search(package)
        
        if not match:
            raise Exception(f'Cannot parse package `{package}`')

        parsed_packages[match[1]] = {
            'version': match[2] and parse_version(match[2]),
            'source': match[3],
            'deps_version': match[2]
        }

    return parsed_packages

def manage_package(command: str, name: str, package: dict = None):
        version = package and package['version']
        source = package and package['source']

        req_line = name if not version else f'{name}{version}'
        if source:
            req_line = f'--index-url {source} --no-deps {req_line}'
        
        system(f'python3 -m pip {command} {req_line}')
        requirements = ([str(r) for r in get_distribution(name).requires()])

        for requirement in requirements:
            req_line = requirement.replace('>', r'\>')
            system(f'python3 -m pip install {req_line}')

        return get_distribution(name).version
