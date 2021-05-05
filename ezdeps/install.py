from .manager import Manager

def install(manager: Manager, directive_params: list, params: dict):
    if not params:
        deps_type = 'default'
        packages = directive_params
    elif directive_params:
        raise Exception('Invalid syntax\nUse `ezdeps -h` to watch command list')
    elif ('S' in params or 'default' in params):
        deps_type = 'default'
        packages = params['S'] if 'S' in params else params['default']
    elif ('D' in params or 'development' in params):
        deps_type = 'development'
        packages = params['D'] if 'D' in params else params['development']
    elif ('A' in params or 'all' in params):
        deps_type = 'all'
        packages = None

        other_params = params['A'] if 'A' in params else params['all']
        if other_params != True:
            raise Exception('Unexpected params')

    if packages == True:
        packages = None

    manager.install(packages, deps_type)
