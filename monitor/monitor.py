from inverter.inverter import InverterApi
from .publisher import Publisher, PublishError
import threading
import time
import datetime
from typing import List
from run.log import get_logger


class GoToSleepError(IOError):
    pass


class InverterMonitor(threading.Thread):
    def __init__(self, inverter: InverterApi, publisher: Publisher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = get_logger(__name__)
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
        # Not very robust for sites other than Perth, or potential time zone changes in future
        if datetime.datetime.now().hour >= 19:
            raise GoToSleepError("Solar generation probably zero after 7pm, going in for the long sleep")

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
