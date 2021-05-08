from .utils.cli import get_setup_params
from .docs import print_docs
from .manager import Manager

from .install import install
from .uninstall import uninstall
from .update import update
from .build import build
from .publish import publish

setup_params = get_setup_params()
directive = setup_params and setup_params['directive']
directive_params = setup_params and setup_params['directive_params']
params = setup_params and setup_params['params']

if not directive:
    print_docs()
    exit()

file_path = 'f' in params and params['f']
rc_path = 'r' in params and params['r']
manager = Manager(file_path, rc_path)

if directive == 'install':
    install(manager, directive_params, params)
elif directive == 'uninstall':
    uninstall(manager, directive_params, params)
elif directive == 'update':
    update(manager, directive_params, params)
elif directive == 'build':
    build(manager)
    if directive_params == ['publish']:
        publish(manager, params)
elif directive == 'publish':
    publish(manager, params)
else:
    raise Exception(f'Unexpected directive `{directive}`')

if not ('J' in params and 'without-json' in params):
    manager.write()
