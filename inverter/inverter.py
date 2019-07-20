import json
import os
from run.log import get_logger


class InverterApi(object):
    def __init__(self, conf_folder: str):
        self._logger = get_logger(__name__)
        with open(os.path.join(conf_folder, "conf.json"), "r") as fh:
            conf = json.load(fh)
        self.base_url = conf["fronius_ip"]  # type: str
        if not self.base_url.startswith("http://"):
            self.base_url = "http://" + self.base_url

    def get_realtime_data(self) -> dict:
        raise NotImplemented
