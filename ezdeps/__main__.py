from .utils.cli import get_setup_params
from .docs import print_docs
from .manager import Manager

from .install import install
from .uninstall import uninstall
from .update import update

setup_params = get_setup_params()
directive = setup_params and setup_params['directive']
directive_parmas = setup_params and setup_params['directive_parmas']
params = setup_params and setup_params['params']

if not directive:
    print_docs()
    exit()

file_path = 'f' in params and params['f']
rc_path = 'r' in params and params['r']
manager = Manager(file_path, rc_path)

if directive == 'install':
    install(manager, directive_parmas, params)
elif directive == 'uninstall':
    uninstall(manager, directive_parmas)
elif directive == 'update':
    update(manager, directive_parmas)
elif directive == 'publish':
    pass
else:
    raise Exception(f'Unexpected directive `{directive}`')

manager.write()
