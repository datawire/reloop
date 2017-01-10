import click
import yaml

from pathlib import Path


def merge_dicts(base, overrides):

    """Merge an override dictionary over a base dictionary. Particularly useful when the base represents default values
    that are meant to be overridden"""

    res = base.copy()
    res.update(overrides)
    return res


def load_config(path, required=True):
    p = Path(path)
    if not p.exists() and not required:
        return {}
    elif not p.exists() and required:
        click.echo("Fabformer is not initialized!")
        return None
    else:
        with p.open('r') as f:
            return yaml.load(f)
