from payload import event_handler, io


@event_handler({'print_ip', })
async def print_ip(server, session, event):
    io.print('IP:', event.data.get('ip', 'unknown'))
