def merge_dicts(dict1: dict, dict2: dict):
    new_dict = { **dict1, **dict2 }
    union_keys = set(dict1.keys()) & set(dict2.keys())

    for key in union_keys:
        dict1_value = dict1[key]
        dict2_value = dict2[key]
        
        if isinstance(dict1_value, dict) and isinstance(dict2_value, dict):
            new_dict[key] = merge_dicts(dict1_value, dict2_value)
        elif dict2_value is None:
            del new_dict[key]

    return new_dict
