import re
from os import system
from pkg_resources import get_distribution

def parse_version(version: str):
    """
    Returns parsed version from .ezdeps.json
    """

    eq_type = '=='
    if version[0] == '^':
        eq_type = r'\>='
        version = version[1:]

    return eq_type + version

def parse_packages(packages: list):
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

def use_auth(source: str, auth_data: dict = {}):
    def auth_provider(match):
        domain = match.group(1)

        auth_string = ''
        if domain in auth_data:
            domain_data = auth_data[domain]
            auth_string = f'{domain_data["USER"]}:{domain_data["PASSWORD"]}@'

        return f'//{auth_string}{domain}/'

    domain_regexp = r'//([^/]*)'
    return re.sub(domain_regexp, auth_provider, source)

def manage_package(
    command: str,
    name: str,
    package: dict = None,
    auth_data: dict = {},
    deps = True
):
        version = package and package['version']
        source = package and 'source' in package and package['source']
        if source:
            source = use_auth(source, auth_data)

        req_line = name if not version else f'{name}{version}'
        if source:
            req_line = f'--index-url {source} --no-deps {req_line}'
        
        if system(f'python3 -m pip {command} {req_line}'):
            raise Exception('Error installing pip module')
        
        if deps:
            try:
                requirements = ([str(r) for r in get_distribution(name).requires()])

                for requirement in requirements:
                    req_line = requirement.replace('>', r'\>').replace('<', r'\<')
                    if system(f'python3 -m pip install {req_line}'):
                        raise Exception('Error installing pip module')

            except Exception:
                pass
        
        try:
            return get_distribution(name).version
        except Exception:
            return
