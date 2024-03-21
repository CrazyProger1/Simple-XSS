import re

HOSTNAME_REGEX = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
DOMAIN_REGEX = re.compile(
    r'^(?!:\/\/)([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
)
URL_REGEX = re.compile(
    r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?'
)
