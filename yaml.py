from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)


def load_yaml(filename):
    path = Path(__file__).parent / filename
    with open(path, 'r') as f:
        return yaml.load(f)


def dump_yaml(data, filename):
    path = Path(__file__).parent / filename
    with open(path, 'w') as f:
        yaml.dump(data, f)


def dump_to_stream(data, stream):
    return yaml.dump(data, stream)
