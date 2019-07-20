from inverter.inverter import InverterApi
from .publisher import Publisher, PublishError
import threading
import logging
import time
from typing import List
import sys


class InverterMonitor(threading.Thread):
    def __init__(self, inverter: InverterApi, publisher: Publisher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        self._logger.setLevel(logging.DEBUG)
        self.inverter = inverter
        self.publisher = publisher
        self.run_event = threading.Event()
        self.run_event.set()
        self._data_buffer = []
        self._last_push = 0.0
        self._push_interval = 30.0

    def stop(self, timeout: float):
        self.run_event.clear()
        return self.join(timeout)

    def run(self) -> None:
        while self.run_event.is_set():
            self._one_iter()

    def _one_iter(self):
        data = self.inverter.get_realtime_data()
        if "DAY_ENERGY_Wh" not in data:
            self._logger.warning("Missing expected key! Data: %s" % data)
        self._data_buffer.append(data)

        if time.time() > (self._last_push + self._push_interval):
            avg = self._average_data(self._data_buffer)
            try:
                self.publisher.publish_data(avg)
            except PublishError as e:
                self._logger.warning("Failed to publish data: %s" % str(e))
            else:
                self._data_buffer = []
                self._last_push = time.time()

    @classmethod
    def _average_data(cls, data: List[dict]) -> dict:
        outp = {}
        for k, v in data[0].items():
            outp[k] = sum([d[k] for d in data if k in d]) / len(data)
        outp["data_set"] = len(data)
        return outp
