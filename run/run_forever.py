from monitor.monitor import InverterMonitor, GoToSleepError
from inverter.fronius import FroniusInverterApi
from monitor.publisher import Publisher
import time
import logging
import logging.config
import json
import argparse
import signal
import datetime
from run.log import get_logger


WAIT_TIME = 60
LONG_SLEEP_TIME = 10 * 60 * 60  # 10 hours
Terminated = False


def main():
    global Terminated

    _logger = get_logger(__name__)
    parser = argparse.ArgumentParser(description="Solar Inverter IoT client")
    parser.add_argument("--conf", dest='conf', type=str, help='Path to a configuration folder (certs, conf, etc)',
                        default='conf')
    args = parser.parse_args()
    monitor = None

    try:
        with open('logging_config.json', 'r') as fh:
            conf = json.load(fh)
    except IOError:
        pass
    else:
        logging.config.dictConfig(conf)

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

                # Allow ctrl-c to end script
                while True:
                    monitor.join(1.0)

            except GoToSleepError as e:
                _logger.info("Caught: %s" % str(e))

            except Exception:
                _logger.exception("Catching exception (probably IOError?) and waiting %d seconds" % WAIT_TIME)
                time.sleep(WAIT_TIME)

            if datetime.datetime.now().hour >= 19:
                _logger.info("Sleeping for 10 hours overnight")
                time.sleep(LONG_SLEEP_TIME)

    except KeyboardInterrupt:
        pass

    if monitor is not None and monitor.is_alive():
        monitor.stop(2.0)
    if Terminated:
        _logger.info("Terminated signal ended script..")


if __name__ == '__main__':
    main()
