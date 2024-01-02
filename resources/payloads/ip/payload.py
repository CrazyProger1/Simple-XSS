from src.core.services.payloads import BasePayload


class Payload(BasePayload):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Allows you to find out IP.'
    NAME = 'IP Logger'
    VERSION = '0.1'
    TRANSPORT = {
        'http',
        'websocket'
    }

# from payload import event_handler
#
#
# @event_handler(events={'print_ip', })
# def print_ip(transport, request):
#     print(request.data.get('ip'))
#
