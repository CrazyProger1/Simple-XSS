from ..sessions import BaseSession


class HTTPSession(BaseSession):
    def __repr__(self):
        return f'<HTTP Session: {self.host}:{self.port}>'
