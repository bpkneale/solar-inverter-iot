import json
import os
import logging
import sys


class InverterApi(object):
    def __init__(self, conf_folder: str):
        with open(os.path.join(conf_folder, "conf.json"), "r") as fh:
            conf = json.load(fh)
        self.base_url = conf["fronius_ip"]  # type: str
        if not self.base_url.startswith("http://"):
            self.base_url = "http://" + self.base_url

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        self._logger.setLevel(logging.DEBUG)

    def get_realtime_data(self) -> dict:
        raise NotImplemented
