import json
from http import HTTPStatus
from urllib.request import urlopen

from .utils import ERR_MESSAGE_TEMPLATE, URL_MOSCOW, get_logger

logger = get_logger()


class YandexWeatherAPI:
    """
    Base class for requests
    """

    @staticmethod
    def _do_req(url):
        """Base request method"""
        try:
            with urlopen(url) as req:
                resp = req.read().decode("utf-8")
                resp = json.loads(resp)
            if req.status != HTTPStatus.OK:
                raise Exception(
                    "Error during execute request. {}: {}".format(
                        resp.status, resp.reason
                    )
                )
            return resp
        except Exception as ex:
            logger.error(ex)
            raise Exception(ERR_MESSAGE_TEMPLATE)

    def get_forecasting(self):
        """
        :return: response data as json
        """
        return self._do_req(URL_MOSCOW)
