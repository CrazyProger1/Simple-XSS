from src.utils import di
from .factories import TransportServiceFactory
from .encoders import BaseEncoder, JSONEncoder

transport_service_factory_dependency = di.Dependency(TransportServiceFactory)
encoder_class_dependency = di.Dependency(BaseEncoder, default=JSONEncoder)
