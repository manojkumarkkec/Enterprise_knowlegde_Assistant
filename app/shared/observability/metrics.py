import time


class Metrics:


    def __init__(self):

        self.data = {}



    def start(
        self,
        name:str,
    ):

        self.data[name] = (
            time.perf_counter()
        )



    def end(
        self,
        name:str,
    ):

        if name not in self.data:
            return 0


        latency = (
            time.perf_counter()
            -
            self.data[name]
        )


        return round(
            latency,
            3,
        )