from typing import Container

from simplexss.utils.packages import Package


class Payload(Package):
    TRANSPORTS: Container[str] = set()
