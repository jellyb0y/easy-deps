import sys
import re

def get_setup_params():
    """
    Returns setup params
    """

    if len(sys.argv) == 1:
        # There is no setup params
        return None
    
    directive: str = None
    directive_parmas = []
    params = {}

    param_name = None
    regexp = re.compile(r'-([a-zA-Z])$|--([^-][a-zA-Z_-]*)$')

    for arg in sys.argv[1:]:
        match = regexp.search(arg)

        if match:
            param_name = match[1] or match[2]
            params[param_name] = True
        elif param_name:
            if params[param_name] == True:
                params[param_name] = []

            params[param_name].append(arg)
        else:
            if directive:
                if params:
                    raise Exception(f'Unexpected directive `{arg}`')
                else:
                    directive_parmas.append(arg)
            else:
                directive = arg

    return {
        'directive': directive,
        'directive_params': directive_parmas,
        'params': params,
    }
