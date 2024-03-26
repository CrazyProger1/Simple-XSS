from simplexss.api import BasePayload


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Stealer'
    VERSION = '0.0.1'

    @property
    def payload(self) -> str:
        return f'{{transport}}\nalert({self.NAME} - V{self.VERSION})'
