from src.utils import di, packages

from .payloads import BasePayload


class PayloadsDependencyContainer(di.DeclarativeContainer):
    payload_base_class: packages.BasePackage = BasePayload
    payload_loader: packages.BasePackageLoader = di.Factory(packages.PackageLoader)
    current_payload: BasePayload
