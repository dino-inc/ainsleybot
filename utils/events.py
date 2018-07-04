from typing import Callable


# Cheap event emitter
class Event(dict):
    def __call__(self, fname, *args, **kwargs):
        if fname == "*":
            self.call_all(*args, **kwargs)
        else:
            f = self.get(fname)
            if callable(f):
                f(*args, **kwargs)

    def call_all(self, *args, **kwargs):
        for _, f in self.items():
            if callable(f):
                f(*args, **kwargs)

    def add_method(self, func: Callable):
        name = func.__name__
        self.update({name: func})

    def remove_method(self, name: str):
        self.update({name: None})
