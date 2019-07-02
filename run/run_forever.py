from monitor.monitor import InverterMonitor
from inverter.fronius import FroniusInverterApi
from monitor.publisher import Publisher
import time
import logging
import argparse


WAIT_TIME = 60


def main():
    logging.basicConfig(level=logging.INFO)
    _logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="Solar Inverter IoT client")
    parser.add_argument("--conf", dest='conf', type=str, help='Path to a configuration folder (certs, conf, etc)',
                        default='conf')
    args = parser.parse_args()
    monitor = None
    try:
        while True:
            try:
                api = FroniusInverterApi(args.conf)
                pub = Publisher(args.conf)
                monitor = InverterMonitor(api, pub)
                monitor.start()
                while True:
                    time.sleep(10)
            except Exception:
                _logger.exception("Catching exception (probably IOError?) and waiting %d seconds" % WAIT_TIME)
                time.sleep(WAIT_TIME)
    except KeyboardInterrupt:
        pass

    if monitor is not None:
        monitor.stop(2.0)


if __name__ == '__main__':
    main()
