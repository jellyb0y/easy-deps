import re
from json import loads
from os import system
import pkg_resources as pkg
from importlib import reload

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

    regexp = re.compile(r'^([a-zA-Z0-9_-]*)(?:@([^#]*))?(?:#(.*))?$')
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
            auth_string = f'{domain_data["user"]}:{domain_data["password"]}@'

        return f'//{auth_string}{domain}/'

    domain_regexp = r'//([^/]*)'
    return re.sub(domain_regexp, auth_provider, source)

def get_requirements(requirements: dict):
    pip_requirements = {}

    for name, value in requirements.items():
        deps_version = value
        source = None
        if isinstance(value, dict):
            deps_version = value['version']
            source = 'source' in value and value['source']

        version = parse_version(deps_version)

        pip_requirements[name] = {
            'version': version,
            'deps_version': deps_version,
            'source': source
        }
        
    return pip_requirements

def get_pip_requirements(dependencies: dict):
    requirements = []
    
    for key, dependency in dependencies.items():            
        version = dependency['version'].replace('\\', '')
        requirements.append(f'{key}{version}')
    
    return requirements

def manage_package(
    command: str,
    name: str,
    package: dict = None,
    auth_data: dict = {}
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
        
        if source:
            try:
                pip_package = pkg.get_distribution(name)
                path_to_config = f'{pip_package.location}/{pip_package._key}/.ezdeps.json'

                try:
                    fh = open(path_to_config, 'r')
                    body = fh.read()
                    config = loads(body)
                    requirements = get_pip_requirements(get_requirements(config['dependencies']))
                except Exception:
                    requirements = ([str(r) for r in pip_package.requires()])

                for requirement in requirements:
                    req_line = requirement.replace('>', r'\>').replace('<', r'\<')
                    if system(f'python3 -m pip install {req_line}'):
                        raise Exception('Error installing pip module')

            except Exception:
                pass
        
        try:
            reload(pkg)
            return pkg.get_distribution(name).version
        except Exception:
            return
