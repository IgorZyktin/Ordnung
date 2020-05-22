from ordnung.core.vocabulary import get_vocabulary


class Lexis:
    def __init__(self, namespace: str) -> None:
        self.namespace = namespace

    def __getattr__(self, item):
        value = get_vocabulary()[self.namespace].get(item)

        if value is None:
            if str(item).endswith('_'):
                item = item.rstrip('_')
                return get_vocabulary()[self.namespace][item]
            else:
                raise KeyError(item)
        return get_vocabulary()[self.namespace][item]

    def __getitem__(self, item):
        return self.__getattr__(item)
