from simplexss.core.containers import CoreContainer
from simplexss.utils.di import inject
from simplexss.utils.arguments import BaseSchemedArgumentParser


@inject
def parse_arguments(parser: BaseSchemedArgumentParser = CoreContainer.arguments_parser, ):
    return parser.parse_schemed_args()
