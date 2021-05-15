import os
from shutil import rmtree
from .utils.constants import CUR_DIR
from .manager import Manager

def publish(manager: Manager, params):
    repository_name = None
    repository_url = None
    username = None
    password = None

    if 'R' in params: 
        repository_name = params['R'][0]
    elif 'repository' in params:
        repository_name = params['repository'][0]
    
    if 'repository-url' in params:
        repository_url = params['repository-url'][0]
    
    if not (repository_name or repository_url):
        raise Exception('You must provide repository name using `-R` or `--repository`')

    auth_data = manager.auth_data
    common_auth_data = auth_data['@common']
    username = common_auth_data['username']
    password = common_auth_data['password']

    if ((not username or not password) and repository_name in auth_data):
        auth_params = auth_data[repository_name]
        username = auth_params["username"]
        password = auth_params["password"]

    twine_auth = []
    if username:
        twine_auth.append(f'TWINE_USERNAME={username}')
    
    if password:
        twine_auth.append(f'TWINE_PASSWORD={password}')

    if not repository_url:
        params_line = f'--repository {repository_name}'
    else:
        params_line = f'--repository-url {repository_url}'

    os.system(f'{" ".join(twine_auth)} python3 -m twine upload {params_line} dist/*')

    if ('clear' in params or 'C' in params):
        rmtree(f'{CUR_DIR}/build')
        rmtree(f'{CUR_DIR}/dist')
        rmtree(f'{CUR_DIR}/{manager.name}.egg-info')
