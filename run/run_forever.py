from monitor.monitor import InverterMonitor
from inverter.fronius import FroniusInverterApi
from monitor.publisher import Publisher
import time
import logging
import argparse
import signal


WAIT_TIME = 60
Terminated = False


def main():
    global Terminated

    logging.basicConfig(level=logging.DEBUG)
    _logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="Solar Inverter IoT client")
    parser.add_argument("--conf", dest='conf', type=str, help='Path to a configuration folder (certs, conf, etc)',
                        default='conf')
    args = parser.parse_args()
    monitor = None
    try:
        while not Terminated:
            try:
                api = FroniusInverterApi(args.conf)
                pub = Publisher(args.conf)

                monitor = InverterMonitor(api, pub)
                monitor.start()

                def sigterm_handler(_signo, _stack_frame):
                    global Terminated
                    _logger.warning("sigterm_handler executed, %s, %s" % (_signo, _stack_frame))
                    Terminated = True
                    monitor.stop(0.0)

                signal.signal(signal.SIGTERM, sigterm_handler)
                monitor.join()

            except Exception:
                _logger.exception("Catching exception (probably IOError?) and waiting %d seconds" % WAIT_TIME)
                time.sleep(WAIT_TIME)

    except KeyboardInterrupt:
        pass

    if monitor is not None and monitor.is_alive():
        monitor.stop(2.0)
    if Terminated:
        _logger.info("Terminated signal ended script..")


if __name__ == '__main__':
    main()
