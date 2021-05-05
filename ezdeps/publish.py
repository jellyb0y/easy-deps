import os
from shutil import rmtree
from .utils.constants import CUR_DIR
from .manager import Manager

def publish(manager: Manager, params):
    clear_after = False
    if ('clear' in params or 'C' in params):
        clear_after = True
        if 'clear' in params:
            del params['clear']
        else:
            del params['C']

    params_array = []
    for key, values in params.items():
        if len(key) == 1:
            params_array.append(f'-{key}')
        else:
            params_array.append(f'--{key}')

        params_array.extend(values)

    params_line = ' '.join(params_array)
    os.system(f'twine upload {params_line} dist/*')

    if clear_after:
        rmtree(f'{CUR_DIR}/build')
        rmtree(f'{CUR_DIR}/dist')
        rmtree(f'{CUR_DIR}/{manager.name}.egg-info')
