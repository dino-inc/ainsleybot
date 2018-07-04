from typing import Callable


# Cheap event emitter
class Event(dict):
    async def __call__(self, fname, *args, **kwargs):
        if fname == "*":
            await self.call_all(*args, **kwargs)
        else:
            f = self.get(fname)
            if callable(f):
                await f(*args, **kwargs)

    async def call_all(self, *args, **kwargs):
        for _, f in self.items():
            if callable(f):
                await f(*args, **kwargs)

    def add_method(self, func: Callable):
        name = func.__name__
        self.update({name: func})

    def remove_method(self, name: str):
        self.update({name: None})
