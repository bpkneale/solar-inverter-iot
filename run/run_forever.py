from monitor.monitor import InverterMonitor
from inverter.fronius import FroniusInverterApi
from monitor.publisher import Publisher
import time
import logging
import argparse


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Solar Inverter IoT client")
    parser.add_argument("--secrets", dest='secrets', type=str, help='Path to client secrets (certs, config, etc)',
                        default='secrets')
    args = parser.parse_args()
    api = FroniusInverterApi("http://192.168.1.111")
    pub = Publisher(args.secrets)
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
