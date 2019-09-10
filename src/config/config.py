import yaml
import sys


class Config(object):
    """
    YAML config parser
    """
    def __init__(self, cpath=None):
        if len(sys.argv) > 1 is not None and sys.argv[1].endswith(".yaml"):
            self.cpath = sys.argv[1]
        elif cpath:
            self.cpath = cpath
        else:
            self.cpath = "./config.yaml"

        with open(self.cpath, "r") as yf:
            self.conf = yaml.safe_load(yf)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, item):
        keys = item.split(".")
        current = self.conf
        for key in keys:
            if '=' in key:
                # search for certain element in list of dictionaries
                assert isinstance(current, list)
                k, v = key.split("=")[:2]
                try:
                    current = list(filter(lambda x: x[k.strip()] == v.strip(), current))[0]
                except IndexError:
                    return {}
            else:
                current = current[int(key)] if isinstance(current, list) else current[key]
        return current

    def update(self):
        with open(self.cpath, "w") as yf:
            yaml.safe_dump(self.conf, yf)

    def set(self, key, value):
        keys = key.split(".")
        k1, k2 = ".".join(keys[:-1]), keys[-1]
        addr = self.get(k1)
        addr[k2] = value


if __name__ == '__main__':
    c = Config()

    # basic dict query
    print(c["example.config"])  # will return list

    # dict + list query
    print(c["example.config.0"])  # if the type of ".config" is list next key is casted to int

    # filtering list of dict by key
    print(c["filtered_config.name=something1"])

    # updating
    c["filtered_config.name=something1.value"] = 11  # set value in memory
    c.update()  # update the file
