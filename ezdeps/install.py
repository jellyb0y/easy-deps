from .manager import Manager

def install(manager: Manager, directive_parmas: list, params: dict):
    is_dev = 'D' in params
    packages = params['D'] if is_dev else directive_parmas
    manager.install(packages, is_dev)
