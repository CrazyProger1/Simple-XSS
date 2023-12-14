from payload import event_handler


@event_handler(events={'print_ip', })
def print_ip(transport, request):
    print(request.data.get('ip'))
