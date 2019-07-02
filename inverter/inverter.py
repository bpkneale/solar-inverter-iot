import json
import os


class InverterApi(object):
    def __init__(self, conf_folder: str):
        with open(os.path.join(conf_folder, "conf.json"), "r") as fh:
            conf = json.load(fh)
        self.base_url = conf["fronius_ip"]  # type: str
        if not self.base_url.startswith("http://"):
            self.base_url = "http://" + self.base_url

    def get_realtime_data(self) -> dict:
        raise NotImplemented
