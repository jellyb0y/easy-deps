from .manager import Manager

def install(manager: Manager, directive_parmas: list, params: dict):
    deps_type = 'all'
    packages = directive_parmas
    
    if directive_parmas and params:
        raise Exception('Invalid syntax\nUse `ezdeps -h` to watch command list')

    if 'default' in params:
        deps_type = 'default'
        packages = 'D' in params in params['deps']
    elif ('D' in params or 'development' in params):
        deps_type = 'development'
        packages = params['D'] if 'D' in params else params['development']
    elif ('P' in params or 'peer' in params):
        deps_type = 'peer'
        packages = params['P'] if 'P' in params else params['peer']
    elif ('A' in params or 'all' in params):
        deps_type = 'all'

    if packages == True:
        packages = None

    manager.install(packages, deps_type)
