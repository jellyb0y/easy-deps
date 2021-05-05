from .manager import Manager

def update(manager: Manager, directive_parmas: list, params: dict = None):
    if params:
        raise Exception('Unexpacted params')

    manager.update(directive_parmas)
