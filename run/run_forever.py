from monitor.monitor import InverterMonitor
from inverter.fronius import FroniusInverterApi
from monitor.publisher import Publisher
import time
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    api = FroniusInverterApi("http://192.168.1.111")
    pub = Publisher()
    monitor = InverterMonitor(api, pub)
    monitor.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    monitor.stop(2.0)


if __name__ == '__main__':
    main()
