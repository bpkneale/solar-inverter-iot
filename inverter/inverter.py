
class InverterApi(object):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_realtime_data(self) -> dict:
        raise NotImplemented
