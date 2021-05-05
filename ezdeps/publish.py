import os
from shutil import rmtree
from .utils.constants import CUR_DIR
from .manager import Manager

def publish(manager: Manager, params):
    if 'R' in params: 
        repository_name = params['R'][0]
    elif 'repository' in params:
        repository_name = params['repository'][0]
    else:
        raise Exception('You must provide repository name using `-R` or `--repository`')

    auth_data = manager.auth_data
    if repository_name not in auth_data:
        raise Exception('Repository not found at your `.ezdepsrc` file')

    auth_params = auth_data[repository_name]
    twine_auth = f'TWINE_USERNAME={auth_params["username"]} TWINE_PASSWORD={auth_params["password"]}'

    if 'repository_url' not in params:
        params_line = f'--repository {repository_name}'
    else:
        params_line = f'--repository-url {params["repository_url"]}'

    os.system(f'{twine_auth} python3 -m twine upload {params_line} dist/*')

    if ('clear' in params or 'C' in params):
        rmtree(f'{CUR_DIR}/build')
        rmtree(f'{CUR_DIR}/dist')
        rmtree(f'{CUR_DIR}/{manager.name}.egg-info')
