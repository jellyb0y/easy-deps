from .manager import Manager

def uninstall(manager: Manager, directive_parmas: list, params: dict = None):
    if params:
        raise Exception('Unexpacted params')

    manager.uninstall(directive_parmas)
