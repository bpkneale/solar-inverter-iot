import requests
import logging
from .inverter import InverterApi


_logger = logging.getLogger(__name__)


class FroniusInverterApi(InverterApi):
    def __init__(self, base_url: str, device_id: int = 1, scope: dict = None):
        super().__init__(base_url)
        self.device_id = device_id
        data = self.get_api_version()
        self.base_url_with_ver = self.base_url + data["BaseURL"]
        self.scope = scope or {
            "Scope": "Device",
            "DeviceId": self.device_id
        }

    def _get(self, url, params=None) -> requests.Response:
        _logger.debug("[me] -> [%s]" % url)
        resp = requests.get(url, params or {})
        extra = "[no_reason]"
        try:
            extra = resp.json()["Head"]["Status"]["Reason"]
        except KeyError:
            pass
        _logger.debug("[%s] -> [me]: %s" % (url, extra))
        return resp

    def get_api_version(self) -> dict:
        return self._get(self.base_url + "/solar_api/GetAPIVersion.cgi").json()

    def get_realtime_data(self, scope: dict = None):
        params = {"DataCollection": "CommonInverterData"}
        params.update(self.scope)
        params.update(scope or {})
        resp = self._get(self.base_url_with_ver + "GetInverterRealtimeData.cgi", params).json()
        data = {}
        for k, v in resp["Body"]["Data"].items():
            if "Unit" in v.keys() and "Value" in v.keys():
                datak = "%s_%s" % (k, v["Unit"])
                data[datak] = v["Value"]
        return data

    def get_sensor_data(self, scope: dict = None):
        params = {"DataCollection": "NowSensorData"}
        params.update(self.scope)
        params.update(scope or {})
        return self._get(self.base_url_with_ver + "GetSensorRealtimeData.cgi", params).json()

    def get_string_realtime_data(self, scope: dict = None):
        params = {"DataCollection": "NowStringControlData"}
        params.update(self.scope)
        params.update(scope or {})
        return self._get(self.base_url_with_ver + "GetStringRealtimeData.cgi", params).json()


def main():
    import pprint
    logging.basicConfig(level=logging.DEBUG)
    inv = FroniusInverterApi("http://192.168.1.111")
    print(inv.base_url_with_ver)
    pprint.pprint(inv.get_realtime_data())
    pprint.pprint(inv.get_sensor_data())
    pprint.pprint(inv.get_string_realtime_data({"Scope": "System"}))


if __name__ == '__main__':
    main()
