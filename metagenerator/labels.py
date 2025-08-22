from typing import Any

def __flatten_dict(
        d: dict,
        parent_key : str = ''
    ) -> dict:
    """
    Flatten a nested dictionary.
    """
    items = {}
    for k, v in d.items():
        new_key = f'{parent_key}.{k}' if parent_key else k
        if isinstance(v, dict):
            items.update(__flatten_dict(v, new_key))
        else:
            items[new_key] = v
    return items

def __to_string(
        v: Any
    ) -> str:
    """
    Provide a string representation of objects that is adequate for labels.
    """
    if list == type(v):
        return str(v).replace(' ','').replace('\'','\\"')
    else:
        return str(v)

def labels_from_manifest(
        generator_name: str,
        generator_info: dict
    ) -> list[str]:
    """
    Create list of labels for container from manifest
    """
    info = generator_info.copy()

    try:
        generator_tag = info.pop('version')
    except KeyError:
        raise RuntimeError('version not specified in generator manifest')

    fd = __flatten_dict(info, f'{generator_name}.{generator_tag}')

    return [f'{k}={__to_string(v)}' for k, v in fd.items()]
