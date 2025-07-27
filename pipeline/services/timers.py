from contextlib import contextmanager
from time import perf_counter

class BaseTimer():

    def __init__(self, allow_print=False):
        self.t0 = None
        self.dt = None
        self.allow_print = allow_print

    def __enter__(self):
        self.t0 = perf_counter()

    def __exit__(self, type=None, value=None, traceback=None):
        self.__dt = (perf_counter() - self.t0) # Store the desire value
        if self.allow_print is True:
            print(f"Scope took {self.dt*1000: 0.1f} milliseconds")
    
    @property
    def expired_milliseconds(self) -> float:
        return self.__dt*1000
    
    @property
    def expired_seconds(self) -> float:
        return self.__dt
   
class APITimer(BaseTimer):

    def __init__(self, allow_print=False):
        super().__init__(allow_print)

class DatabaseTimer(BaseTimer):

    def __init__(self, allow_print=False):
        super().__init__(allow_print)

class PipelineTimer(BaseTimer):

    def __init__(self, allow_print=False):
        super().__init__(allow_print)