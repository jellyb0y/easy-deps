import os

def publish(params):
    params_array = []
    for key, values in params.items():
        if len(key) == 1:
            params_array.append(f'-{key}')
        else:
            params_array.append(f'--{key}')

        params_array.extend(values)

    params_line = ' '.join(params_array)
    os.system(f'twine upload {params_line} dist/*')
