from .utils.constants import PACKAGE_FILE, RC_FILE
from .utils.merge import merge_dicts
from .utils.packages import parse_packages, parse_version, manage_package

from json import dumps, loads
import re


class Manager():
    file_path: str = None
    name: str = None
    version: str = None
    description: str = None
    dependencies: list = None
    dev_dependencies: list = None
    auth_data: dict = None

    def __init__(self, file_path: str = None, rc_path: str = None):
        self.file_path = file_path or PACKAGE_FILE
        self.parse_project_file()

        self.rc_path = rc_path or RC_FILE
        self.parse_rc_file()

    def parse_project_file(self):
        project = {}

        try:
            fh = open(self.file_path, 'r+')

            try:
                body = fh.read()
                project = loads(body)
            except Exception:
                raise Exception(f'Cannot load `{PACKAGE_FILE}`')

            fh.close()
        except Exception:
            pass

        self.name = 'name' in project and project['name']
        self.version = 'version' in project and project['version']
        self.description = 'description' in project and project['description']
        self.dependencies = project['dependencies'] if 'dependencies' in project else {} 
        self.dev_dependencies = project['dev_dependencies'] if 'dev_dependencies' in project else {}

    def parse_rc_file(self):
        self.auth_data = {}

        try:
            fh = open(self.rc_path, 'r+')

            directive_regexp = re.compile(r'\[([^]]*)\]')
            props_regexp = re.compile(r'([^=]*)=([^\s]*)')
            comments_regexp = r'#.*$'
            active_directive = None

            for line in fh.readlines():
                clear_line = re.sub(comments_regexp, '', line)

                directive_match = directive_regexp.search(clear_line)
                if directive_match:
                    active_directive = directive_match[1]
                    self.auth_data[active_directive] = {}
                
                props_match = props_regexp.search(clear_line)
                if props_match:
                    props_name = props_match[1]
                    props_value = props_match[2]
                    self.auth_data[active_directive][props_name] = props_value

        except Exception:
            pass

    def write(self):
        with open(self.file_path, 'w+') as fh:
            project = {
                'name': self.name,
                'version': self.version,
                'description': self.description,
                'dependencies': self.dependencies,
                'dev_dependencies': self.dev_dependencies
            }

            fh.write(dumps(project, indent=4))
            fh.close()

    def get_requirements(self, is_dev = False):
        requirements = self.dependencies if not is_dev else self.dev_dependencies
        pip_requirements = {}

        for name, value in requirements.items():
            deps_version = value if isinstance(value, str) else value['version']

            if isinstance(value, dict):
                version = parse_version(deps_version)
                source = value['source']
            else:
                version = parse_version(deps_version)
                source = None

            pip_requirements[name] = {
                'version': version,
                'deps_version': deps_version,
                'source': source
            }
            
        return pip_requirements

    def update_packages(self, packages: dict, is_dev = False):
        new_packages = {}
        
        for name, package in packages.items():
            source = package['source']
            deps_version = package['deps_version'] 

            if source:
                new_packages[name] = {
                    'source': source,
                    'version': deps_version,
                }
            else:
                new_packages[name] = deps_version

        if is_dev:
            self.dev_dependencies = merge_dicts(self.dev_dependencies, new_packages)
        else:
            self.dependencies = merge_dicts(self.dependencies, new_packages)

    def install(self, packages: list = [], is_dev = False):
        if packages:
            requirements = parse_packages(packages)
        else:
            requirements = self.get_requirements(is_dev)
        
        for name, requirement in requirements.items():
            new_version = manage_package('install', name, requirement, auth_data=self.auth_data)
            if not requirement['deps_version']:
                requirement['deps_version'] = new_version

        if packages:
            self.update_packages(requirements, is_dev)

    def uninstall(self, packages):
        for package in packages:
            if package in self.dependencies:
                del self.dependencies[package]
            
            if package in self.dev_dependencies:
                del self.dev_dependencies[package]

            manage_package('uninstall -y', package, auth_data=self.auth_data)

    def update(self, packages):
        packages = parse_packages(packages)
        requirements = self.get_requirements()
        requirements_dev = self.get_requirements(is_dev=True)

        for name, package in packages.items():
            if (name not in requirements and name not in requirements_dev):
                raise Exception('Dependency not found')                

            new_version = manage_package('install --upgrade', name, package, auth_data=self.auth_data)

            if name in requirements:
                requirements_dev[name]['deps_version'] = new_version
            
            if name in requirements_dev:
                requirements[name]['deps_version'] = new_version

        self.update_packages(requirements)
        self.update_packages(requirements_dev, True)
