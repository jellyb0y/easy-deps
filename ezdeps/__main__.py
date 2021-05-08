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

write_file = True
if ('J' in params or 'without-json' in params):
    if 'J' in params:
        options = params['J']
        del params['J']
    else:
        options = params['without-json']
        del params['without-json']

    if not isinstance(options, bool):
        directive_params.extend(options)

    write_file = False

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

if write_file:
    manager.write()
