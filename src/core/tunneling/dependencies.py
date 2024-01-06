from src.utils import di
from .factories import TunnelingServiceFactory

tunneling_service_factory = di.Dependency(TunnelingServiceFactory)
