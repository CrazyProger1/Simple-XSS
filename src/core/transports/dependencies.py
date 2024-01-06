from src.utils import di
from .factories import TransportServiceFactory

transport_service_factory = di.Dependency(TransportServiceFactory)
