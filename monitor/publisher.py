from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import json
import time
from run.log import get_logger
from typing import Tuple


class PublishError(IOError):
    pass


class Publisher(object):
    def __init__(self, secrets_folder: str = "secrets"):
        self._logger = get_logger(__name__)
        self.client, self.thing_name = self.get_client(secrets_folder)

    def publish_data(self, data: dict):
        data["publish_time"] = int(time.time())
        data["event"] = "live_solar_data"
        data["device_id"] = self.thing_name
        self._logger.info("Publishing data: %s" % str(data))
        self.client.publish("fronius/newdata", json.dumps(data), 0)

    def get_client(self, secrets_folder: str) -> Tuple[AWSIoTMQTTClient, str]:
        with open(os.path.join(secrets_folder, "conf.json"), "r") as fh:
            data = json.load(fh)

        endpoint = data["endpoint"]
        thing_name = data["thing_name"]
        secrets = os.listdir(secrets_folder)
        root_ca = next(filter(lambda s: s.endswith(".pem"), secrets))
        private_key = next(filter(lambda s: s.endswith("private.pem.key"), secrets))
        cert = next(filter(lambda s: s.endswith(".pem.crt"), secrets))

        self._logger.info("Connecting with parameters: %s" % str(locals()))

        client = AWSIoTMQTTClient(thing_name)
        client.configureEndpoint(endpoint, 8883)
        client.configureCredentials(os.path.join(secrets_folder, root_ca),
                                    os.path.join(secrets_folder, private_key),
                                    os.path.join(secrets_folder, cert))
        client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        client.configureDrainingFrequency(2)  # Draining: 2 Hz
        client.configureConnectDisconnectTimeout(2)  # 10 sec
        client.configureMQTTOperationTimeout(2)  # 5 sec
        client.connect()
        return client, thing_name
